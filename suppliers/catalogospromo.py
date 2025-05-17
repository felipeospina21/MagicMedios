import asyncio
from io import BytesIO
from typing import Tuple

import requests
from playwright.async_api import Locator, Page

from entities.entities import ProductData, TaskResult
from log import logger
from utils import (
    get_all_selectors_with_retry,
    get_image_url,
    get_inventory,
    get_selector_with_retry,
    search_product,
)


async def search_product_link(
    product_containers: list[Locator], ref: str
) -> Locator | None:
    for product in product_containers:
        title = await product.locator(".ref.textoColor").inner_text()
        if title.lower() == ref.lower():
            return product.locator(".img-producto")


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


async def not_found(original_ref: str, ref: str, msg: str) -> TaskResult:
    logger.error(f"{ref} {msg}")
    data: ProductData = {
        "ref": ref,
        "image": None,
        "title": "",
        "description": [],
        "color_inventory": [],
    }
    return data, original_ref


async def extract_data(page: Page, original_ref: str) -> TaskResult:
    ref = original_ref.upper().split("CP", 1)[1]
    print(f"Processing: {ref}")

    for _ in range(4):
        await search_product(
            page, ref, selector="#productos", timeout=10000, retries=5, delay=3
        )

        product_containers = await get_all_selectors_with_retry(
            page, ".itemProducto-", ref, timeout=10000, retries=5, delay=1
        )
        if not product_containers:
            continue

        product_link = await search_product_link(product_containers, ref)
        if not product_link:
            continue

        await asyncio.sleep(2)
        await product_link.click()
        break

    title, description = await get_description(page, ref)
    if not title or len(title) == 0:
        return await not_found(original_ref, ref, "title not found")

    xpath = "//tr[@class='titlesRow']/following-sibling::tr[not(@class='hideInfo')]"
    color_inventory = await get_inventory(
        page, xpath, ref, color_cell_index=0, inventory_cell_index=3
    )

    product_image_url = await get_image_url(page, "#img_01", ref)
    if not product_image_url:
        return {
            "ref": ref,
            "title": title,
            "description": description,
            "image": None,
            "color_inventory": color_inventory,
        }, None

    response = requests.get(product_image_url)
    image_data = BytesIO(response.content)

    return {
        "ref": ref,
        "title": title,
        "description": description,
        "image": image_data,
        "color_inventory": color_inventory,
    }, None
