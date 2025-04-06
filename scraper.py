import asyncio
from io import BytesIO
import re
from typing import Any, Callable, Coroutine, Dict, Tuple

from entities.entities import ProductData
from playwright.async_api import async_playwright, Browser, Page
from suppliers import catalogospromo, mppromos, promoop, cdopromo, nwpromo

MAX_CONCURRENT_TASKS = 5  # Configurable

semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)

SUPPLIER_URLS = {
    "cp": "https://www.catalogospromocionales.com/",
    "mp": "https://www.marpicopromocionales.com/",
    "po": "https://www.promoopcioncolombia.co/",
}

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
            "https://www.catalogospromocionales.com/",
            catalogospromo.extract_data,
        )

    elif re.search("^MP|^mp]", ref):
        return (
            ref.upper().split("MP", 1)[1],
            "https://www.marpicopromocionales.com/",
            mppromos.extract_data,
        )
    elif re.search("^PO|^po]", ref):
        return (
            ref.upper().split("PO", 1)[1],
            "https://www.promoopcioncolombia.co/",
            promoop.extract_data,
        )
    elif re.search("^CD|^cd", ref):
        return (
            ref.upper().split("CD", 1)[1],
            "api",
            cdopromo.extract_data,
        )
    # elif re.search("^NW|^nw", ref):
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


async def scrape(ref_list):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        tasks = [scrape_product(browser, ref) for ref in ref_list]
        results = await asyncio.gather(*tasks)
        await browser.close()

        return results
