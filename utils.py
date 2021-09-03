def create_supplier_ref_list(ref,suppliers_list):
    if ref[0:2] == "cp":
        suppliers_list['cp_refs'].append(ref)
    elif ref[0:2] == "va":
        suppliers_list['va_refs'].append(ref)
    else:
        suppliers_list['prov3_refs'].append(ref)
    
    return suppliers_list

def scrapp_supplier_data(suppliers_list):
    if len(suppliers_list['cp_refs']) != 0:
        print('scrapp cp data')
    if len(suppliers_list['va_refs']) != 0:
        print('scrapp va data')
    if len(suppliers_list['prov3_refs']) != 0:
        print('scrapp prov3 data')
    if len(suppliers_list['prov4_refs']) != 0:
        print('scrapp prov4 data')