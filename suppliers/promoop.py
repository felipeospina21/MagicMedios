import asyncio
import os
from io import BytesIO
from typing import Any, Dict, Tuple

import requests
from dotenv import load_dotenv
from playwright.async_api import Page

from constants import urls
from entities.entities import TaskResult
from utils import (get_all_selectors_with_retry, get_image_url, get_inventory,
                   get_selector_with_retry, humanize_text, remove_prefix,
                   wait_for_selector_with_retry)


async def login(page: Page, ref: str):
    load_dotenv()
    password = os.environ.get("PROMO_OP_PASSWORD")
    if not password:
        print(f"promo opcion password not found")
        return

    input = await get_selector_with_retry(page, "#psw", ref)
    if input:
        await input.fill(password)
        await input.press("Enter")


async def get_description(
    page: Page, header_xpath: str, ref: str
) -> Tuple[str, str, list[str]]:
    title = ""
    subtitle = ""
    description = []
    content_table = await get_selector_with_retry(page, header_xpath, ref)
    if content_table:
        text = await content_table.inner_text()
        rows = text.split("\n")
        title = rows[0]
        subtitle = rows[2]
        description = rows[3:]

    return title, subtitle, description


async def search_product(
    page: Page, product_code: str, retries: int = 3, delay: int = 2
) -> bool:
    """Attempts to search for a product, retrying if necessary."""
    for _ in range(retries):
        input: bool = await wait_for_selector_with_retry(
            page, "#q", product_code, retries=3, delay=0
        )
        if input:
            await asyncio.sleep(2)
            await page.locator("#q").fill(product_code)
            await page.locator("#q").press("Enter")

        found: bool = await wait_for_selector_with_retry(
            page, "//a[@class='img-responsive ']", product_code, retries=3, delay=0
        )
        if found:
            return True

        await asyncio.sleep(delay)

    return False


async def get_colors_map(page: Page, ref: str) -> Dict[str, str]:
    colors = {}
    color_element = await get_all_selectors_with_retry(
        page, "//ul[@class='colors']/child::li", ref
    )
    if color_element:
        for color in color_element:
            id = await color.get_attribute("id")
            t = await color.get_attribute("title")
            name = t.capitalize() if t else ""
            color_ref = humanize_text(remove_prefix(id, "product_color_")) if id else ""
            colors[color_ref] = name

    return colors


async def extract_data(page: Page, context: Any, original_ref: str) -> TaskResult:
    ref = original_ref.upper().split("PO", 1)[1]
    print(f"Processing: {ref}")

    await login(page, ref)
    await asyncio.sleep(3)

    found: bool = await search_product(page, ref, delay=0)
    if not found:
        await context.close()
        return {
            "ref": ref,
            "image": None,
            "title": "",
            "description": [],
            "color_inventory": [],
        }, original_ref

    await page.click("//a[@class='img-responsive ']")

    partial_image_url = await get_image_url(
        page, "//div[@id='img-list-1']/div[1]/img[1]", ref
    )
    product_image_url = f"{urls["po"]}/{partial_image_url}"
    header_xpath = "//table[@class='table table-hover table-responsive']/tbody[1]"
    title, subtitle, description = await get_description(page, header_xpath, ref)
    xpath = "//table[@class='table table-striped']/tbody[1]/child::tr"
    color_inventory = await get_inventory(
        page, xpath, ref, color_cell_index=2, inventory_cell_index=3
    )
    colors_map = await get_colors_map(page, ref)

    # reassign color key value
    for item in color_inventory:
        ref = item["color"]
        if ref in colors_map:
            item["color"] = colors_map[ref]

    if not product_image_url:
        await context.close()
        return {
            "ref": ref,
            "title": title,
            "subtitle": subtitle,
            "description": description,
            "image": None,
            "color_inventory": color_inventory,
        }, None

    response = requests.get(product_image_url)
    image_data = BytesIO(response.content)

    await context.close()
    return {
        "ref": ref,
        "title": title,
        "subtitle": subtitle,
        "description": description,
        "image": image_data,
        "color_inventory": color_inventory,
    }, None
