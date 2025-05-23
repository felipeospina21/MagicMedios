from typing import TypedDict


measures: dict[str, float] = {
    "lf_1": 0.8,
    "lf_2": 8.5,
    "lf_3": 3,
    "lf_4": 12,
    "lf_5": 1,
    "lf_6": 1.5,
    "t_0": -0.5,
    "t_1": 3.5,
    "t_2": 4,
    "t_3": 5.5,
    "t_4": 8.5,
    "t_5": 11.5,
    "t_6": 14.5,
    "t_7": 2.5,
    "w_1": 17.4,
    "w_2": 6,
    "w_3": 8,
    "w_4": 6.6,
    "w_5": 6.4,
    "h_1": 1,
    "h_2": 2,
    "h_3": 5,
    "h_4": 8.5,
    "h_5": 8,
    "h_6": 6,
    "cell_font": 7,
    "cell_font_2": 11,
}


class URLS(TypedDict):
    cp: str
    mp: str
    po: str
    cd: str
    nw: str


urls: URLS = {
    "cp": "https://www.catalogospromocionales.com/",
    "mp": "https://www.marpicopromocionales.com/",
    "po": "https://www.promoopcioncolombia.co/",
    "cd": "api",
    "nw": "https://promocionalesnw.com/",
}
