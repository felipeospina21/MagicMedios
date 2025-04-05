import asyncio
from io import BytesIO
from playwright.async_api import Page
from typing import Any, Optional

import requests
from entities.entities import ProductData
from utils import wait_for_selector_with_retry


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


async def extract_data(page: Page, context: Any, ref: str) -> ProductData:
    print(f"Processing: {ref}")

    found: bool = await search_product(page, ref, delay=0)
    if not found:
        await context.close()
        return {
            "ref": ref,
            "title": "",
            "description": [],
            "color_inventory": [],
        }

    await page.click(".img-producto")

    found = await wait_for_selector_with_retry(page, "#img_01", timeout=5000)
    if not found:
        await context.close()
        return {
            "ref": ref,
            "title": "",
            "description": [],
            "color_inventory": [],
        }

    product_name: str = await page.locator(".hola").inner_text()
    product_image_url: Optional[str] = await page.locator(
        "#img_01"
    ).first.get_attribute("src")
    info_text_arr = product_name.split("\n\n")
    title = info_text_arr[0]
    desc_list = info_text_arr[2:]
    color_inventory = []
    try:
        xpath = "//tr[@class='titlesRow']/following-sibling::tr[not(@class='hideInfo')]"
        color_elements = await page.locator(xpath).all()
        for element in color_elements:
            if await element.is_visible():
                cells = await element.locator("td").all()
                cell_texts = [await cell.inner_text() for cell in cells]
                color = cell_texts[0]
                inventory = cell_texts[3]
                color_inventory.append({"color": color, "inventory": inventory})
            else:
                print("not visible")

    except Exception as e:
        raise SystemExit("Error: ", e)

    if not product_image_url:
        await context.close()
        return {
            "ref": ref,
            "title": title,
            "description": desc_list,
            "color_inventory": color_inventory,
        }

    response = requests.get(product_image_url)
    image_data = BytesIO(response.content)

    await context.close()
    return {
        "ref": ref,
        "title": title,
        "description": desc_list,
        "image": image_data,
        "color_inventory": color_inventory,
    }
