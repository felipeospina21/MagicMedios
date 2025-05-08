import asyncio
import re
import subprocess
from io import BytesIO
from typing import Any, Callable, Coroutine, Dict, Tuple

from playwright._impl._errors import Error as PlaywrightError
from playwright.async_api import Browser, Page, async_playwright

from app import App
from constants import urls
from entities.entities import TaskResult
from presentation import Presentation
from suppliers import catalogospromo, cdopromo, mppromos, nwpromo, promoop

MAX_CONCURRENT_TASKS = 2  # Configurable

semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)

type Data = Dict[str, str | BytesIO]

type Task = Callable[
    [Page, Any, str],
    Coroutine[Any, Any, TaskResult],
]

type EmptyTask = Callable[[], None]


def get_ref_and_url(ref: str) -> Tuple[str, str, Task]:
    if re.search("^CP|^cp]", ref):
        return (
            ref,
            urls["cp"],
            catalogospromo.extract_data,
        )

    elif re.search("^MP|^mp]", ref):
        return (
            ref,
            urls["mp"],
            mppromos.extract_data,
        )
    elif re.search("^PO|^po]", ref):
        return (
            ref,
            urls["po"],
            promoop.extract_data,
        )
    elif re.search("^CD|^cd", ref):
        return (
            ref,
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


async def scrape_product(browser: Browser, ref: str) -> TaskResult:
    ref, url, task = get_ref_and_url(ref.upper())

    async with semaphore:  # Limit concurrency
        context = await browser.new_context()
        if url == "api":
            data, not_found = await task(None, context, ref)
            await context.close()
            return data, not_found

        else:
            page = await context.new_page()
            await page.goto(url)

            data = await task(page, context, ref)
            await context.close()
            return data


async def scrape(ref_list: list[str], headless_flag=True) -> list[TaskResult] | None:
    async with async_playwright() as p:
        # loop to install browser and try again if not found
        for _ in range(2):
            try:
                browser = await p.chromium.launch(headless=headless_flag)
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


async def run_scraper_task(
    app: App, presentation: Presentation, references: list[str]
) -> list[str]:
    task_result = await scrape(references, app.args.headless)
    not_found_refs = []
    if task_result:
        for idx, [ref_data, not_found] in enumerate(task_result):
            if not_found:
                not_found_refs.append(not_found)
                continue

            # FIX: append retry references instead of overwrite
            presentation.create_title(
                ref_data["title"], idx, count=idx + 1, ref=ref_data["ref"]
            )
            if "subtitle" in ref_data:
                presentation.create_subtitle(ref_data["subtitle"], idx)

            presentation.create_description(ref_data["description"], idx)
            presentation.create_img(ref_data["image"], idx)
            presentation.create_quantity_table(idx)
            presentation.create_inventory_table(ref_data["color_inventory"], idx)

    return not_found_refs
