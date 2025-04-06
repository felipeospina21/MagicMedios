import asyncio
from io import BytesIO
from typing import Tuple

import requests
from entities.entities import ProductData
from playwright.async_api import Page

from utils import (
    get_all_selectors_with_retry,
    get_inventory,
    wait_for_selector_with_retry,
    get_image_url,
)


async def search_product(
    page: Page, product_code: str, retries: int = 3, delay: int = 2
) -> bool:
    """Attempts to search for a product, retrying if necessary."""
    for _ in range(retries):
        input: bool = await wait_for_selector_with_retry(
            page, "#input-buscar-menu", retries=3, delay=0
        )
        if input:
            await asyncio.sleep(2)
            await page.locator("#input-buscar-menu").fill(product_code)
            await page.locator("#input-buscar-menu").press("Enter")

        links = await page.locator("a").all()
        if len(links) > 0:
            return True

        await asyncio.sleep(delay)

    return False


async def get_description(page: Page) -> Tuple[str, str, list[str]]:
    title = ""
    subtitle = ""
    description = []

    sections = await get_all_selectors_with_retry(page, "//div[@class='card-body']")
    if sections:
        content_section = sections[1]

        if await content_section.is_visible():
            text = await content_section.inner_text()
            split_text = text.splitlines()
            title = split_text[0]
            subtitle = split_text[2]
            description = split_text[4:-2]

    return title, subtitle, description


async def extract_data(page: Page, context, ref: str) -> ProductData:
    print(f"Processing: {ref}")

    found: bool = await search_product(page, ref, delay=0)
    if not found:
        await context.close()
        return {
            "ref": ref,
            "title": "",
            "image": None,
            "description": [],
            "color_inventory": [],
        }

    await page.click(
        "//a[@class='col-md-3 text-decoration-none text-dark ng-star-inserted']"
    )

    product_image_url = await get_image_url(page, "#imagen-material-0")
    title, subtitle, description = await get_description(page)
    xpath = "//tbody[@class='text-center text-pequeno-x1 align-middle']/child::tr"
    color_inventory = await get_inventory(
        page, xpath, color_cell_index=2, inventory_cell_index=5
    )

    if not product_image_url:
        await context.close()
        return {
            "ref": ref,
            "image": None,
            "title": title,
            "description": description,
            "color_inventory": color_inventory,
            "subtitle": subtitle,
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
        "subtitle": subtitle,
    }
