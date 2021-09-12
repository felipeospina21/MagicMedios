import re
from pptx import Presentation
from pptx.util import Pt, Cm

def create_supplier_ref_list(ref,suppliers_dict):
    if re.search('-', ref):
        suppliers_dict['cat_promo'].append(ref)
    elif re.search('^[^NWnw]', ref) and re.search('^[a-zA-Z]{2}[0-9]{4}$|^[a-zA-Z]{3}[0-9]{3}$', ref):
        suppliers_dict['mp_promo'].append(ref)
    elif re.search(' +', ref):
        suppliers_dict['promo_op'].append(ref)
    elif re.search('^NW|^nw', ref):
        suppliers_dict['nw_promo'].append(ref)
    
    return suppliers_dict

def text_frame_paragraph(text_frame, text, font_size, bold=False ):
    tf = text_frame.add_paragraph()
    tf.text = text
    tf.font.size = Pt(font_size)
    tf.font.bold = bold