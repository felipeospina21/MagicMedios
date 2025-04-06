from typing import TypedDict, List


class Category(TypedDict):
    id: int
    name: str


class Icon(TypedDict):
    id: int
    label: str
    short_name: str
    picture: str


class Picture(TypedDict):
    small: str
    medium: str
    original: str


class Color(TypedDict):
    id: int
    name: str
    hex_code: str
    picture: str


class Variant(TypedDict):
    id: int
    novedad: bool
    stock_available: int
    stock_existent: int
    list_price: str
    net_price: str
    picture: Picture
    detail_picture: Picture
    color: Color


class Packing(TypedDict):
    width: str
    height: str
    depth: str
    volume: str
    quantity: int
    weight: str


class Product(TypedDict):
    id: int
    code: str
    name: str
    description: str
    categories: List[Category]
    packing: Packing
    icons: List[Icon]
    variants: List[Variant]
