import asyncio
from io import BytesIO
from typing import Tuple

from playwright.async_api import Locator, Page

from entities.entities import ProductData, TaskResult
from log import logger
from utils import (
    get_all_selectors_with_retry,
    get_image_url,
    get_inventory,
    get_selector_with_retry,
    search_product,
    request_with_retry,
)


async def search_product_link(
    product_containers: list[Locator], ref: str
) -> Locator | None:
    for product in product_containers:
        title = await product.locator(
            "//div[@class='product-card__body']/span[@class='product-card__sku']"
        ).inner_text()
        title = title.removeprefix("SKU: ").strip()

        if title.lower() == ref.lower():
            return product.locator(".product-card__image")


async def get_description(page: Page, ref: str) -> Tuple[str, list[str]]:
    title = ""
    descTexts = []
    titleElement = await get_selector_with_retry(page, ".product-info__title", ref)
    descriptionElement = await get_selector_with_retry(
        page, ".product-description-content", ref
    )

    if titleElement and descriptionElement:
        title = await titleElement.inner_text()
        description = await descriptionElement.inner_text()
        descTexts = description.split("\n")

    return title, descTexts


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
    print(f"Procesando ref: {ref}")

    for _ in range(1):
        await search_product(
            page,
            ref,
            selector="input[placeholder='Buscar productos...']",
            timeout=10000,
            retries=5,
            delay=3,
        )

        product_containers = await get_all_selectors_with_retry(
            page, ".product-card", ref, timeout=10000, retries=5, delay=1
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
    description.pop()
    if not title or len(title) == 0:
        return await not_found(original_ref, ref, "title not found")

    xpath = "//tr[@class=' ']"
    color_inventory = await get_inventory(
        page, xpath, ref, color_cell_index=0, inventory_cell_index=5
    )

    product_image_url = await get_image_url(
        page, "//div[@class='product-gallery__image']/img[1]", ref
    )
    if not product_image_url:
        return {
            "ref": ref,
            "title": title,
            "description": description,
            "image": None,
            "color_inventory": color_inventory,
        }, None

    response = await request_with_retry(product_image_url, ref, "image download")
    if not response:
        return {
            "ref": ref,
            "title": title,
            "description": description,
            "image": None,
            "color_inventory": color_inventory,
        }, None
    image_data = BytesIO(response.content)

    return {
        "ref": ref,
        "title": title,
        "description": description,
        "image": image_data,
        "color_inventory": color_inventory,
    }, None
