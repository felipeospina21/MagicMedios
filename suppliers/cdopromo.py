import json
import os
from io import BytesIO
from typing import Any

import requests
from playwright.async_api import Page

from entities.entities import Color_Inventory, TaskResult
from entities.variant import Product, Variant
from log import logger


def get_api_data(url):
    response = requests.get(url)
    content = response.content
    return json.loads(content)


async def extract_data(page: Page, context: Any, ref: str) -> TaskResult:
    print(f"Processing: {ref}")

    auth_token = os.environ.get("API_TOKEN")
    if auth_token == "":
        logger.error("No se encontro token para la api de CDO")
        print("No se encontro token para la api de CDO")

    url = f"http://api.colombia.cdopromocionales.com/v2/products/{ref}?auth_token={auth_token}"
    result: Product = get_api_data(url)
    title = result["name"]
    subtitle = result["description"]
    variants: list[Variant] = result["variants"]
    icons = result["icons"]
    description = []
    for icon in icons:
        description.append(icon["label"])

    product_image_url = variants[0]["detail_picture"]["medium"]
    color_inventory: list[Color_Inventory] = []
    for variant in variants:
        color_inventory.append(
            {
                "color": variant["color"]["name"],
                "inventory": str(variant["stock_existent"]),
            }
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
