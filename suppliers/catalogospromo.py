import asyncio
from io import BytesIO
from typing import Any, Tuple

import requests
from playwright.async_api import Locator, Page

from entities.entities import ProductData
from log import logger
from utils import (get_all_selectors_with_retry, get_image_url, get_inventory,
                   get_selector_with_retry, wait_for_selector_with_retry)


async def search_product_link(
    product_containers: list[Locator], ref: str
) -> Locator | None:
    for product in product_containers:
        title = await product.locator(".ref.textoColor").inner_text()
        if title.lower() == ref.lower():
            return product.locator(".img-producto")


async def search_product(
    page: Page, product_code: str, retries: int = 3, delay: int = 2
) -> list[Locator] | None:
    """Attempts to search for a product, retrying if necessary."""
    for _ in range(retries):
        input: bool = await wait_for_selector_with_retry(
            page, "#productos", product_code, retries=3, delay=0
        )
        if input:
            await asyncio.sleep(2)
            await page.locator("#productos").fill(product_code)
            await page.locator("#productos").press("Enter")

        product_containers = await get_all_selectors_with_retry(
            page, ".itemProducto-", product_code, retries=3, delay=0
        )
        if product_containers:
            return product_containers

        await asyncio.sleep(delay)

    return None


async def get_description(page: Page, ref: str) -> Tuple[str, list[str]]:
    title = ""
    description = []

    section = await get_selector_with_retry(page, ".hola", ref)
    if section:
        product_name = await section.inner_text()
        info_text_arr = product_name.split("\n\n")
        title = info_text_arr[0]
        description = info_text_arr[2:]

    return title, description


async def not_found(ref: str, msg: str, context) -> ProductData:
    logger.error(f"{ref} {msg}")
    await context.close()
    return {
        "ref": ref,
        "image": None,
        "title": "",
        "description": [],
        "color_inventory": [],
    }


async def extract_data(page: Page, context: Any, ref: str) -> ProductData:
    print(f"Processing: {ref}")

    product_containers = await search_product(page, ref, retries=5)
    if not product_containers:
        return await not_found(ref, "not found", context)

    product_link = await search_product_link(product_containers, ref)
    if not product_link:
        return await not_found(ref, "link not found", context)

    await product_link.click()
    product_image_url = await get_image_url(page, "#img_01", ref)
    title, description = await get_description(page, ref)
    xpath = "//tr[@class='titlesRow']/following-sibling::tr[not(@class='hideInfo')]"
    color_inventory = await get_inventory(
        page, xpath, ref, color_cell_index=0, inventory_cell_index=3
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
