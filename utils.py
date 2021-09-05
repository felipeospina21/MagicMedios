import re
from catalogospromo import catalogos_promo

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

def scrapp_supplier_data(suppliers_dict, document):
    if len(suppliers_dict['cp_refs']) != 0:
        catalogos_promo(suppliers_dict['cp_refs'], document)

    if len(suppliers_dict['va_refs']) != 0:
        print('scrapp va data')
    if len(suppliers_dict['prov3_refs']) != 0:
        print('scrapp prov3 data')
    if len(suppliers_dict['prov4_refs']) != 0:
        print('scrapp prov4 data')