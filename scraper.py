import asyncio
import random
import re
import subprocess
from io import BytesIO
from typing import Any, Awaitable, Callable, Coroutine, Dict, Optional, Tuple

from playwright._impl._errors import Error as PlaywrightError
from playwright.async_api import (Browser, BrowserContext, Page,
                                  async_playwright)

from app import App
from constants import urls
from entities.entities import TaskResult
from log import logger
from presentation import Presentation
from suppliers import catalogospromo, cdopromo, mppromos, nwpromo, promoop

MAX_CONCURRENT_TASKS = 3  # Configurable

semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)

type Data = Dict[str, str | BytesIO]

type Task = Callable[
    [Page, str],
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


async def scrape_product(
    page: Page, context: BrowserContext, ref: str
) -> TaskResult | None:
    ref, url, task = get_ref_and_url(ref.upper().strip())

    async with semaphore:  # Limit concurrency
        if url == "api":
            data, not_found = await task(page, ref)
            return data, not_found

        else:
            for attempt in range(3):
                try:
                    await page.goto(url, wait_until="domcontentloaded")
                    break
                except Exception as e:
                    if "ERR_HTTP2_PROTOCOL_ERROR" in str(e):
                        logger.error(f"Encountered HTTP2 error, retrying {attempt+1}")
                        await asyncio.sleep(2)
                    else:
                        logger.error(f"{ref}: {Exception}")
                        await context.close()
                        return

            await asyncio.sleep(random.uniform(0.5, 1.2))
            data = await task(page, ref)
            return data


async def run_with_concurrency(
    limit: int,
    items: list[str],
    task_factory: Callable[[str], Awaitable[Optional[TaskResult]]],
) -> list[TaskResult]:
    results: list[TaskResult] = []
    semaphore = asyncio.Semaphore(limit)

    async def sem_task(item: str):
        async with semaphore:
            return await task_factory(item)

    for coro in asyncio.as_completed([sem_task(item) for item in items]):
        result = await coro
        if result:
            results.append(result)
    return results


async def scrape_all(
    browser: Browser, product_codes: list[str], concurrency: int
) -> list[TaskResult]:
    context = await browser.new_context()
    effective_concurrency = min(concurrency, len(product_codes))
    page_queue: asyncio.Queue[Page] = asyncio.Queue()
    pages: list[Page] = [await context.new_page() for _ in range(effective_concurrency)]
    for p in pages:
        page_queue.put_nowait(p)

    async def task_factory(code: str) -> Optional[TaskResult]:
        page = await page_queue.get()
        try:
            result = await scrape_product(page, context, code)
            return result
        finally:
            page_queue.put_nowait(page)

    results = await run_with_concurrency(
        effective_concurrency, product_codes, task_factory
    )

    await context.close()
    return results


async def scrape(ref_list: list[str], headless_flag=True) -> list[TaskResult] | None:
    async with async_playwright() as p:
        # loop to install browser and try again if not found
        for _ in range(2):
            try:
                browser = await p.chromium.launch(headless=headless_flag)
                results = await scrape_all(browser, ref_list, MAX_CONCURRENT_TASKS)
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
