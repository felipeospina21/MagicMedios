import re
# from pptx import Presentation
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