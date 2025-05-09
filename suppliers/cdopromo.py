import json
import os
from io import BytesIO

import requests

from entities.entities import Color_Inventory, TaskResult
from entities.variant import Product, Variant
from log import logger


def get_api_data(url: str, ref: str) -> Product | None:
    try:
        response = requests.get(url)
        content = response.content
        return json.loads(content)
    except Exception:
        print(f"referencia {ref} no encontrada en la api del proveedor CDO")
        logger.error(f"{ref}-not found in api {Exception}")


async def extract_data(_: None, original_ref: str) -> TaskResult:
    ref = original_ref.upper().split("CD", 1)[1]
    print(f"Processing: {ref}")

    auth_token = os.environ.get("API_TOKEN")
    if auth_token == "":
        logger.error("No se encontro token para la api de CDO")
        print("No se encontro token para la api de CDO")

    url = f"http://api.colombia.cdopromocionales.com/v2/products/{ref}?auth_token={auth_token}"
    result = get_api_data(url, ref)
    if not result:
        return {
            "ref": ref,
            "title": "",
            "subtitle": "",
            "description": [],
            "image": None,
            "color_inventory": [],
        }, None

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

    return {
        "ref": ref,
        "title": title,
        "subtitle": subtitle,
        "description": description,
        "image": image_data,
        "color_inventory": color_inventory,
    }, None
