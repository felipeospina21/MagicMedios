
from get_data import Get_Data
from utils import measures

def get_cat_promo_data(suppliers_dict, prs, references):
    data = Get_Data('https://www.catalogospromocionales.com/', 'cat_promo', prs, references, measures)
    header_xpath = "//div[@class='hola']"
    for ref in suppliers_dict['cat_promo']:
        idx = data.get_original_ref_list_idx(ref)
        count = idx + 1
        data.search_ref(ref,'productos')
        data.click_first_result("//div[@id='backTable']/div[1]/div[1]/a[1]", ref)
        data.create_quantity_table(ref, idx)
        data.get_title(header_xpath,0, None, count, ref, idx)
        data.get_description(f"{header_xpath}/p[2]", ref, idx)
        data.get_package_info(ref, idx)
        data.get_inventory("//tr[@class='titlesRow']/following-sibling::tr", "//table[@class='tableInfoProd']", ref, idx)
        data.get_img("//img[@id='img_01']", ref, idx)

    data.close_driver()