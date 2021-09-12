import re

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
