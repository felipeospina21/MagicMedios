import json
import re

import requests
from pptx.enum.text import PP_ALIGN
from pptx.util import Cm, Pt


def create_supplier_ref_list(
    ref, suppliers_dict: dict[str, list[str]]
) -> dict[str, list[str]]:
    if re.search("^CP|^cp]", ref):
        split_ref = ref.split("CP", 1)
        suppliers_dict["cat_promo"].append(split_ref[1])
    elif re.search("^MP|^mp]", ref):
        split_ref = ref.split("MP", 1)
        suppliers_dict["mp_promo"].append(split_ref[1])
    elif re.search("^PO|^po]", ref):
        split_ref = ref.split("PO", 1)
        suppliers_dict["promo_op"].append(split_ref[1])
    elif re.search("^CD|^cd", ref):
        split_ref = ref.split("CD", 1)
        suppliers_dict["cdo_promo"].append(split_ref[1])
    elif re.search("^NW|^nw", ref):
        suppliers_dict["nw_promo"].append(ref)
    else:
        print(
            f"\nNo se pudo identificar la referencia {ref}, favor validar el prefijo ingresado"
        )

    return suppliers_dict


def text_frame_paragraph(text_frame, text, font_size, bold=False, centered=False):
    tf = text_frame.add_paragraph()
    tf.text = text
    tf.font.size = Pt(font_size)
    tf.font.bold = bold
    tf.space_before = Cm(0)
    if centered:
        tf.alignment = PP_ALIGN.CENTER


def get_api_data(url):
    response = requests.get(url)
    content = response.content
    return json.loads(content)


measures = {
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
