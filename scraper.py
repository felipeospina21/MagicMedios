import asyncio
import re
import subprocess
from io import BytesIO
from typing import Any, Callable, Coroutine, Dict, Tuple

from playwright._impl._errors import Error as PlaywrightError
from playwright.async_api import Browser, Page, async_playwright

from constants import urls
from entities.entities import ProductData
from suppliers import catalogospromo, cdopromo, mppromos, nwpromo, promoop

MAX_CONCURRENT_TASKS = 5  # Configurable

semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)

type Data = Dict[str, str | BytesIO]

type Task = Callable[
    [Page, Any, str],
    Coroutine[Any, Any, ProductData],
]

type EmptyTask = Callable[[], None]


def get_ref_and_url(ref: str) -> Tuple[str, str, Task]:
    if re.search("^CP|^cp]", ref):
        return (
            ref.upper().split("CP", 1)[1],
            urls["cp"],
            catalogospromo.extract_data,
        )

    elif re.search("^MP|^mp]", ref):
        return (
            ref.upper().split("MP", 1)[1],
            urls["mp"],
            mppromos.extract_data,
        )
    elif re.search("^PO|^po]", ref):
        return (
            ref.upper().split("PO", 1)[1],
            urls["po"],
            promoop.extract_data,
        )
    elif re.search("^CD|^cd", ref):
        return (
            ref.upper().split("CD", 1)[1],
            urls["cd"],
            cdopromo.extract_data,
        )
    elif re.search("^NW|^nw", ref):
        return (
            ref,
            urls["nw"],
            nwpromo.extract_data,
        )
    raise Exception(
        f"Error: {ref} no pudo ser asociada a ningun proveedor, verificar prefijo"
    )


async def scrape_product(browser: Browser, ref: str) -> ProductData:
    product_ref, url, task = get_ref_and_url(ref.upper())

    async with semaphore:  # Limit concurrency
        context = await browser.new_context()
        if url == "api":
            data = await task(None, context, product_ref)
            await context.close()
            return data

        else:
            page = await context.new_page()
            await page.goto(url)

            data = await task(page, context, product_ref)
            await context.close()
            return data


async def scrape(ref_list) -> list[ProductData] | None:
    async with async_playwright() as p:
        # loop to install browser and try again if not found
        for _ in range(2):
            try:
                browser = await p.chromium.launch(headless=True)
                tasks = [scrape_product(browser, ref) for ref in ref_list]
                results = await asyncio.gather(*tasks)
                await browser.close()
                return results

            except PlaywrightError as e:
                if "Executable doesn't exist" in str(e):
                    print("Browser not found. Installing...")
                    subprocess.run(
                        ["python", "-m", "playwright", "install", "chromium"],
                        check=True,
                    )
                else:
                    raise
