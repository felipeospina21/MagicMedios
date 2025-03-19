import asyncio
from io import BytesIO
import re
from typing import Any, Dict, NotRequired, Optional, Tuple, TypedDict

import requests
from playwright.async_api import async_playwright, Browser, Page

MAX_CONCURRENT_TASKS = 5  # Configurable

semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)

SUPPLIER_URLS = {
    "cp": "https://www.catalogospromocionales.com/",
    "mp": "https://www.marpicopromocionales.com/",
}

type Data = Dict[str, str | BytesIO]


class ProductData(TypedDict):
    ref: str
    title: str
    description: list[str]
    image: NotRequired[BytesIO]


def get_ref_and_url(ref: str) -> Tuple[str, str]:
    if re.search("^CP|^cp]", ref):
        return ref.upper().split("CP", 1)[1], "https://www.catalogospromocionales.com/"

    elif re.search("^MP|^mp]", ref):
        return ref.upper().split("MP", 1)[1], "https://www.marpicopromocionales.com/"
    # elif re.search("^PO|^po]", ref):
    #     split_ref = ref.split("PO", 1)
    #     suppliers_dict["promo_op"].append(split_ref[1])
    # elif re.search("^CD|^cd", ref):
    #     split_ref = ref.split("CD", 1)
    #     suppliers_dict["cdo_promo"].append(split_ref[1])
    # elif re.search("^NW|^nw", ref):
    return "", ""


async def search_product(
    page: Page, product_code: str, retries: int = 3, delay: int = 2
) -> bool:
    """Attempts to search for a product, retrying if necessary."""
    for attempt in range(retries):
        input: bool = await wait_for_selector_with_retry(
            page, "#productos", retries=3, delay=0
        )
        if input:
            await asyncio.sleep(2)
            await page.locator("#productos").fill(product_code)
            await page.locator("#productos").press("Enter")

        found: bool = await wait_for_selector_with_retry(
            page, ".img-producto", retries=3, delay=0
        )
        if found:
            return True

        await asyncio.sleep(delay)

    return False


async def wait_for_selector_with_retry(
    page: Page, selector: str, timeout: int = 5000, retries: int = 3, delay: int = 2
) -> bool:
    """Retries waiting for a selector multiple times before failing."""
    for attempt in range(1, retries + 1):
        try:
            await page.wait_for_selector(selector, timeout=timeout)
            print(f"wating for selector {selector}, {attempt}/{retries}")
            return True
        except Exception:
            if attempt < retries - 1:
                await asyncio.sleep(delay)
            else:
                return False
    return False


async def scrape_product(browser: Browser, ref: str):

    product_ref, url = get_ref_and_url(ref.upper())
    async with semaphore:  # Limit concurrency
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(url)
        await page.wait_for_load_state(
            "domcontentloaded"
        )  # Waits for network to be idle
        data = await extract_data(page, context, product_ref)
        await context.close()
        return {ref: data}


async def extract_data(page, context, ref) -> ProductData:
    print(f"Processing: {ref}")

    found: bool = await search_product(page, ref, delay=0)
    if not found:
        await context.close()
        return {
            "ref": ref,
            "title": "",
            "description": [],
        }

    await page.click(".img-producto")

    found = await wait_for_selector_with_retry(page, "#img_01", timeout=5000)
    if not found:
        await context.close()
        return {
            "ref": ref,
            "title": "",
            "description": [],
        }

    product_name: str = await page.locator(".hola").inner_text()
    product_image_url: Optional[str] = await page.locator(
        "#img_01"
    ).first.get_attribute("src")
    info_text_arr = product_name.split("\n\n")
    title = info_text_arr[0]
    desc_list = info_text_arr[2:]

    if not product_image_url:
        await context.close()
        return {
            "ref": ref,
            "title": title,
            "description": desc_list,
        }

    response = requests.get(product_image_url)
    image_data = BytesIO(response.content)

    await context.close()
    return {"ref": ref, "title": title, "description": desc_list, "image": image_data}


async def scrape(ref_list):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        tasks = [scrape_product(browser, ref) for ref in ref_list]
        results = await asyncio.gather(*tasks)
        await browser.close()
        return {k: v for r in results if r for k, v in r.items()}
