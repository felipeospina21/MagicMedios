import re
import requests
import json
from pptx.util import Pt, Cm
from pptx.enum.text import PP_ALIGN

# def create_supplier_ref_list(ref,suppliers_dict):
#     if re.search('-', ref):
#         suppliers_dict['cat_promo'].append(ref)
#     elif re.search('^[^NWnw]', ref) and re.search('^[a-zA-Z]{2}[0-9]{4}$|^[a-zA-Z]{3}[0-9]{3}$', ref):
#         suppliers_dict['mp_promo'].append(ref)
#     elif re.search(' +', ref):
#         suppliers_dict['promo_op'].append(ref)
#     elif re.search('^NW|^nw', ref):
#         suppliers_dict['nw_promo'].append(ref)
    
#     return suppliers_dict

def create_supplier_ref_list(ref,suppliers_dict):
    if re.search('^CP|^cp]', ref):
        split_ref = ref.split("CP")
        suppliers_dict['cat_promo'].append(split_ref[1])
    elif re.search('^MP|^mp]', ref):
        split_ref = ref.split("MP")
        suppliers_dict['mp_promo'].append(split_ref[1])
    elif re.search('^PO|^po]', ref):
        split_ref = ref.split("PO")
        suppliers_dict['promo_op'].append(split_ref[1])
    elif re.search('^CD|^cd', ref):
        split_ref = ref.split("CD")
        suppliers_dict['cdo_promo'].append(split_ref[1])
    elif re.search('^NW|^nw', ref):
        suppliers_dict['nw_promo'].append(ref)
    
    return suppliers_dict

def text_frame_paragraph(text_frame, text, font_size, bold=False ):
    tf = text_frame.add_paragraph()
    tf.text = text
    tf.font.size = Pt(font_size)
    tf.font.bold = bold
    tf.space_before = Cm(0)
    if text_frame == "tf_footer":
        text.alignment = PP_ALIGN.CENTER

def get_api_data(url):
    response = requests.get(url)
    content = response.content
    return json.loads(content)

measures = {
        "lf_1": 0.8,
        "lf_2": 8.5,
        "lf_3": 3,
        "t_1" : 4,
        "t_2" : 4.5,
        "t_3" : 6,
        "t_4" : 9,
        "t_5" : 12,
        "t_6" : 15,
        "w_1" : 17.4,
        "w_2" : 6,
        "w_3" : 9.9,
        "h_1" : 1,
        "h_2" : 2,
        "h_3" : 5,
        "h_4" : 8.5,
        "h_5" : 7.1,

        "lf_4": 12,
        "t_0": -0.5,
        "w_4": 6.6,
        "h_6": 6,

        "lf_5": 1,
        "t_7": 2.5,
        "w_5": 6.4,
}