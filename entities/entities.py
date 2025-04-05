from io import BytesIO
from typing import NotRequired, TypedDict


class Client(TypedDict):
    name: str
    company: str


class Representative(TypedDict):
    name: str
    phone: str
    email: str


class Contact(TypedDict):
    address: str
    phone: str
    email: str
    web: str


class Color_Inventory(TypedDict):
    color: str
    inventory: str


class ProductData(TypedDict):
    ref: str
    title: str
    description: list[str]
    color_inventory: list[Color_Inventory]
    image: NotRequired[BytesIO]
