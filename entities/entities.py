from typing import TypedDict


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
