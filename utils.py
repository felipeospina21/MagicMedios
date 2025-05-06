import asyncio
from typing import Optional

from playwright.async_api import Locator, Page

from entities.entities import Color_Inventory
from log import logger


async def wait_for_selector_with_retry(
    page: Page,
    selector: str,
    ref: str,
    timeout: int = 5000,
    retries: int = 3,
    delay: int = 2,
) -> bool:
    """Retries waiting for a selector multiple times before failing."""
    for attempt in range(1, retries + 1):
        try:
            logger.info(f"{ref}: wating for selector {selector}, {attempt}/{retries}")
            element = page.locator(selector)
            await element.wait_for(timeout=timeout)
            return True
        except:
            if attempt < retries - 1:
                await asyncio.sleep(delay)
            else:
                return False
    return False


async def get_selector_with_retry(
    page: Page,
    selector: str,
    ref: str,
    timeout: int = 5000,
    retries: int = 3,
    delay: int = 2,
) -> Locator | None:
    """Retries waiting for a selector multiple times before failing."""
    for attempt in range(1, retries + 1):
        try:
            logger.info(f"{ref}: wating for selector {selector}, {attempt}/{retries}")
            element = page.locator(selector)
            await element.wait_for(timeout=timeout)
            return element
        except Exception:
            if attempt < retries - 1:
                await asyncio.sleep(delay)
            else:
                return None


async def get_all_selectors_with_retry(
    page: Page,
    selector: str,
    ref: str,
    timeout: int = 1000,
    retries: int = 3,
    delay: int = 0,
) -> list[Locator] | None:
    """Retries waiting for a selector multiple times before failing."""
    for attempt in range(1, retries + 1):
        try:
            logger.info(f"{ref}: wating for selectors {selector}, {attempt}/{retries}")
            elements = await page.locator(selector).all()
            for element in elements:
                await element.wait_for(timeout=timeout)
            return elements
        except Exception:
            if attempt < retries - 1:
                await asyncio.sleep(delay)
            else:
                return None


async def get_image_url(page: Page, locator: str, ref: str) -> Optional[str]:
    img = await get_selector_with_retry(page, locator, ref, 1000)
    product_image_url: Optional[str]
    if img:
        product_image_url = await page.locator(locator).first.get_attribute("src")
    else:
        product_image_url = None

    return product_image_url


async def get_inventory(
    page: Page,
    selector: str,
    ref: str,
    color_cell_index: int,
    inventory_cell_index: int,
) -> list[Color_Inventory]:
    color_inventory: list[Color_Inventory] = []
    color_elements = await get_all_selectors_with_retry(page, selector, ref)
    if color_elements:
        for element in color_elements:
            if await element.is_visible():
                cells = await element.locator("td").all()
                if len(cells) > 0:
                    cell_texts = [await cell.inner_text() for cell in cells]
                    color = cell_texts[color_cell_index]
                    inventory = cell_texts[inventory_cell_index]
                    color_inventory.append({"color": color, "inventory": inventory})
            else:
                logger.info(f"{element} not visible")

    return color_inventory


def humanize_text(text: str) -> str:
    return text.upper().replace("-", " ")


def remove_prefix(text: str, prefix: str) -> str:
    return text[len(prefix) :] if text.startswith(prefix) else text
