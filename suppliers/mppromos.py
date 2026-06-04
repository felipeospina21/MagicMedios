import asyncio
import os
from dotenv import load_dotenv
from io import BytesIO
from typing import Tuple

from playwright.async_api import Locator, Page

from entities.entities import TaskResult
from log import logger
from utils import (
    get_all_selectors_with_retry,
    get_image_url,
    get_inventory,
    request_with_retry,
    search_product,
    get_selector_with_retry,
)

_logged_in_pages: set[int] = set()


async def login(page: Page, ref: str):
    load_dotenv()
    username = os.environ.get("MP_USERNAME")
    password = os.environ.get("MP_PASSWORD")
    if not password or not username:
        print("mp user/password not found")
        return

    login_btn = await get_selector_with_retry(page, 'button:has-text("Login")', ref)
    if login_btn:
        await login_btn.click()

    user_input = page.get_by_label("Nombre de Usuario")

    if user_input:
        await user_input.fill(username)
    else:
        print("no user input")

    password_input = await get_selector_with_retry(page, "#floatingPassword", ref)
    if password_input:
        await password_input.fill(password)
    else:
        print("no password input")

    accept_btn = await get_selector_with_retry(page, 'button:has-text("Ingresar")', ref)
    if accept_btn:
        await accept_btn.click()
    else:
        print("no ingresar button")

    await asyncio.sleep(3)


async def get_description(page: Page, ref: str) -> Tuple[str, str, list[str]]:
    title = ""
    subtitle = ""
    description = []

    sections = await get_all_selectors_with_retry(
        page, "//div[@class='card-body']", ref, timeout=30000
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


async def close_modal(page: Page) -> None:
    page.set_default_timeout(10000)
    try:
        modal: Locator = page.locator("#modalPromoNovedades")
        if modal:
            btn: Locator = modal.get_by_label("Close")
            if btn:
                await btn.click()
    except Exception:
        logger.error("No modal in MP page")


async def extract_data(page: Page, original_ref: str) -> TaskResult:
    ref = original_ref.upper().split("MP", 1)[1]
    print(f"Procesando ref: {ref}")

    page_key = id(page)
    if page_key not in _logged_in_pages:
        await close_modal(page)
        await login(page, ref)
        _logged_in_pages.add(page_key)

    await search_product(
        page, ref, selector="#input-buscar-menu", delay=2, retries=5, timeout=90000
    )
    selector = "//a[@class='col-md-3 text-decoration-none text-dark ng-star-inserted']"
    try:
        link = page.locator(selector)
        await link.wait_for(state="visible", timeout=60000)
        await link.scroll_into_view_if_needed()
        await link.click(timeout=60000)
        await page.click(selector)
    except Exception:
        logger.error(f"{ref}: {selector} couldn't be clicked")

    product_image_url = await get_image_url(page, "#imagen-material-0", ref)
    title, subtitle, description = await get_description(page, ref)
    xpath = "//tbody[@class='text-center text-pequeno-x1 align-middle']/child::tr"
    color_inventory = await get_inventory(
        page, xpath, ref, color_cell_index=4, inventory_cell_index=7
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

    response = await request_with_retry(product_image_url, ref, "image download")
    if not response:
        return {
            "ref": ref,
            "title": title,
            "description": description,
            "image": None,
            "color_inventory": color_inventory,
            "subtitle": subtitle,
        }, None
    image_data = BytesIO(response.content)

    return {
        "ref": ref,
        "title": title,
        "description": description,
        "image": image_data,
        "color_inventory": color_inventory,
        "subtitle": subtitle,
    }, None
