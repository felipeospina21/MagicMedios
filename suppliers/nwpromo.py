import asyncio
from io import BytesIO
from typing import Any, Tuple

import requests
from playwright.async_api import Page

from entities.entities import ProductData
from utils import (get_all_selectors_with_retry, get_image_url, get_inventory,
                   get_selector_with_retry, wait_for_selector_with_retry)

# def get_nw_promo_data(suppliers_dict, prs, references):
#     data = Get_Data("nw_promo", prs, references, measures)
#     data.execute_driver("https://promocionalesnw.com/")
#     header_xpath = "//div[@class='pb-center-column  col-xs-12 col-sm-6 col-md-6']"
#     for ref in suppliers_dict["nw_promo"]:
#         try:
#             idx = data.get_original_ref_list_idx(ref)
#             count = idx + 1
#             # data.check_pop_up()
#             search_input = data.get_element_with_xpath(
#                 "//input[@id='search_query_top']"
#             )
#             data.send_keys(search_input, ref)
#             time.sleep(10)
#             data.click_first_result("//a[@class='product_image']")
#             data.create_quantity_table(idx)
#
#             # header_text = data.get_title_and_subtitle(header_xpath, 0, 4)
#             # data.create_title(header_text[0], idx, count, ref)
#             # data.create_subtitle(header_text[1], idx)
#             # desc_list = data.get_description(
#             #     "//div[@id='short_description_content']/child::p[1]"
#             # )
#             # data.create_description(desc_list, idx)
#             colors_len = data.get_elements_len_with_xpath(
#                 "//table[@class='table-bordered']/tbody[1]/child::tr"
#             )
#             data.create_inventory_table(
#                 colors_len, "//table[@class='table-bordered']/tbody[1]", idx
#             )
#
#             img_src = data.get_img("//img[@id='bigpic']")
#             data.create_img(img_src, idx, 8, ref)
#         except Exception as e:
#             raise Exception(e)
#
#         print(f"✓ {ref}")
#     print(f"✓ referencias nw promo")
#     data.close_driver()


async def get_title_and_subtitle(page: Page, ref: str) -> Tuple[str, str]:
    title = ""
    subtitle = ""
    content = await get_selector_with_retry(
        page, "//div[@class='pb-center-column  col-xs-12 col-sm-6 col-md-6']", ref
    )
    if content:
        text = await content.inner_text()
        rows = text.split("\n")
        title = rows[0]
        subtitle = rows[4]

    return title, subtitle


async def get_description(page: Page, ref: str) -> list[str]:
    description = []
    content = await get_all_selectors_with_retry(
        page, "//div[@id='short_description_content']/child::p[1]", ref
    )
    if content:
        for element in content:
            text = await element.inner_text()
            description.append(text)

    return description


async def search_product(
    page: Page, product_code: str, retries: int = 3, delay: int = 2
) -> bool:
    """Attempts to search for a product, retrying if necessary."""
    for _ in range(retries):
        locator = "#search"
        input: bool = await wait_for_selector_with_retry(
            page, locator, product_code, retries=3, delay=0
        )
        if input:
            await asyncio.sleep(2)
            await page.locator(locator).fill(product_code)
            await page.locator(locator).press("Enter")

        found: bool = await wait_for_selector_with_retry(
            page, "//a[@class='product_image']", product_code, retries=3, delay=0
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
            "image": None,
            "title": "",
            "description": [],
            "color_inventory": [],
        }

    await page.click("//a[@class='product_image']")

    product_image_url = await get_image_url(page, "//img[@id='bigpic']", ref)
    title, subtitle = await get_title_and_subtitle(page, ref)
    description = await get_description(page, ref)
    xpath = "//table[@class='table-bordered']/tbody[1]"
    color_inventory = await get_inventory(
        page, xpath, ref, color_cell_index=0, inventory_cell_index=4
    )

    if not product_image_url:
        await context.close()
        return {
            "ref": ref,
            "title": title,
            "subtitle": subtitle,
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
        "subtitle": subtitle,
        "description": description,
        "image": image_data,
        "color_inventory": color_inventory,
    }
