import asyncio
from io import BytesIO
import time
from typing import Optional, Tuple

import requests
from entities.entities import Color_Inventory, ProductData
from playwright.async_api import Page

from get_data import Get_Data
from utils import (
    get_all_selectors_with_retry,
    get_selector_with_retry,
    measures,
    wait_for_selector_with_retry,
)


def crawl(suppliers_dict, prs, references):
    data = Get_Data("mp_promo", prs, references, measures)
    data.execute_driver("https://www.marpicopromocionales.com/")
    for ref in suppliers_dict["mp_promo"]:
        try:
            idx = data.get_original_ref_list_idx(ref)
            search_input = data.get_element_with_xpath(
                "//input[@id='input-buscar-menu']"
            )
            data.send_keys(search_input, ref)
            time.sleep(5)
            data.click_first_result(
                "//a[@class='col-md-3 text-decoration-none text-dark ng-star-inserted']"
            )

            header = data.get_title_with_xpath("//div[@class='card-body']").splitlines()
            reference = header[0]
            title = header[1]

            desc = data.get_title_with_xpath(
                "//div[@class='card-body']/p[@class='ng-star-inserted']"
            )

            desc_list = data.get_description(
                "//div[@class='card-body']/div[1]/child::li"
            )

            number_of_colors = data.get_elements_len_with_xpath(
                "//tbody[@class='text-center text-pequeno-x1 align-middle']/child::tr"
            )

            img_src = data.get_img("//img[@id='imagen-material-0']")

        except Exception as e:
            raise Exception(e)

        try:
            data.create_quantity_table(idx)
            data.create_title(f"{reference} {title}", idx, idx + 1, ref)
            data.create_subtitle(desc, idx)
            data.create_description(desc_list, idx)
            data.create_inventory_table(
                number_of_colors,
                "//tbody[@class='text-center text-pequeno-x1 align-middle']",
                idx,
            )
            data.create_img(img_src, idx, 7.4, ref)

        except Exception as e:
            raise Exception(e)

        print(f"✓ {ref}")
    print(f"✓ referencias mp")
    data.close_driver()


async def search_product(
    page: Page, product_code: str, retries: int = 3, delay: int = 2
) -> bool:
    """Attempts to search for a product, retrying if necessary."""
    for attempt in range(retries):
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


async def get_image_url(page: Page) -> Optional[str]:
    img = await get_selector_with_retry(page, "#imagen-material-0", 1000)
    product_image_url: Optional[str]
    if img:
        product_image_url = await page.locator(
            "#imagen-material-0"
        ).first.get_attribute("src")
    else:
        product_image_url = None

    return product_image_url


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


async def get_inventory(page: Page) -> list[Color_Inventory]:
    color_inventory: list[Color_Inventory] = []
    xpath = "//tbody[@class='text-center text-pequeno-x1 align-middle']/child::tr"
    color_elements = await get_all_selectors_with_retry(page, xpath)
    if color_elements:
        for element in color_elements:
            if await element.is_visible():
                cells = await element.locator("td").all()
                cell_texts = [await cell.inner_text() for cell in cells]
                color = cell_texts[2]
                inventory = cell_texts[5]
                color_inventory.append({"color": color, "inventory": inventory})
            else:
                print(f"{element} not visible")

    return color_inventory


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

    product_image_url = await get_image_url(page)
    title, subtitle, description = await get_description(page)
    color_inventory = await get_inventory(page)

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
