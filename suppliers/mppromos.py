from io import BytesIO
from typing import Tuple

import requests
from playwright.async_api import Page

from entities.entities import TaskResult
from log import logger
from utils import (get_all_selectors_with_retry, get_image_url, get_inventory,
                   search_product)


async def get_description(page: Page, ref: str) -> Tuple[str, str, list[str]]:
    title = ""
    subtitle = ""
    description = []

    sections = await get_all_selectors_with_retry(
        page, "//div[@class='card-body']", ref
    )
    if sections and len(sections) > 1:
        content_section = sections[1]

        if await content_section.is_visible():
            text = await content_section.inner_text()
            split_text = text.splitlines()
            title = split_text[0]
            subtitle = split_text[2]
            description = split_text[4:-2]

    else:
        logger.error(f"{ref}: description not found")

    return title, subtitle, description


async def extract_data(page: Page, original_ref: str) -> TaskResult:
    ref = original_ref.upper().split("MP", 1)[1]
    print(f"Processing: {ref}")

    await search_product(page, ref, selector="#input-buscar-menu", delay=2, retries=5)
    selector = "//a[@class='col-md-3 text-decoration-none text-dark ng-star-inserted']"
    try:
        await page.wait_for_selector(selector)
        await page.click(selector)
    except:
        logger.error(f"{ref}: {selector} couldn't be clicked")

    product_image_url = await get_image_url(page, "#imagen-material-0", ref)
    title, subtitle, description = await get_description(page, ref)
    xpath = "//tbody[@class='text-center text-pequeno-x1 align-middle']/child::tr"
    color_inventory = await get_inventory(
        page, xpath, ref, color_cell_index=2, inventory_cell_index=5
    )

    if not product_image_url:
        return {
            "ref": ref,
            "image": None,
            "title": title,
            "description": description,
            "color_inventory": color_inventory,
            "subtitle": subtitle,
        }, None

    response = requests.get(product_image_url)
    image_data = BytesIO(response.content)

    return {
        "ref": ref,
        "title": title,
        "description": description,
        "image": image_data,
        "color_inventory": color_inventory,
        "subtitle": subtitle,
    }, None
