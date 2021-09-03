from catalogospromo import catalogos_promo

def create_supplier_ref_list(ref,suppliers_dict):
    if ref[0:2] == "cp":
        suppliers_dict['cp_refs'].append(ref)
    elif ref[0:2] == "va":
        suppliers_dict['va_refs'].append(ref)
    else:
        suppliers_dict['prov3_refs'].append(ref)
    
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