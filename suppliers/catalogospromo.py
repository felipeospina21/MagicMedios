import asyncio
from io import BytesIO
from playwright.async_api import Page
from typing import Any, Tuple

import requests
from entities.entities import ProductData
from utils import (
    get_inventory,
    get_selector_with_retry,
    wait_for_selector_with_retry,
    get_image_url,
)


async def search_product(
    page: Page, product_code: str, retries: int = 3, delay: int = 2
) -> bool:
    """Attempts to search for a product, retrying if necessary."""
    for _ in range(retries):
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


async def get_description(page: Page) -> Tuple[str, list[str]]:
    title = ""
    description = []

    section = await get_selector_with_retry(page, ".hola")
    if section:
        product_name = await section.inner_text()
        info_text_arr = product_name.split("\n\n")
        title = info_text_arr[0]
        description = info_text_arr[2:]

    return title, description


async def extract_data(page: Page, context: Any, ref: str) -> ProductData:
    print(f"Processing: {ref}")

    found: bool = await search_product(page, ref, delay=0)
    if not found:
        await context.close()
        return {
            "ref": ref,
            "image": None,
            "title": "",
            "description": [],
            "color_inventory": [],
        }

    await page.click(".img-producto")

    product_image_url = await get_image_url(page, "#img_01")
    title, description = await get_description(page)
    xpath = "//tr[@class='titlesRow']/following-sibling::tr[not(@class='hideInfo')]"
    color_inventory = await get_inventory(
        page, xpath, color_cell_index=0, inventory_cell_index=3
    )

    if not product_image_url:
        await context.close()
        return {
            "ref": ref,
            "title": title,
            "description": description,
            "image": None,
            "color_inventory": color_inventory,
        }

    response = requests.get(product_image_url)
    image_data = BytesIO(response.content)

    await context.close()
    return {
        "ref": ref,
        "title": title,
        "description": description,
        "image": image_data,
        "color_inventory": color_inventory,
    }
