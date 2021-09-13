
from get_data import Get_Data

def get_cat_promo_data(suppliers_dict, prs, references):
    data = Get_Data('https://www.catalogospromocionales.com/', 'cat_promo', prs, references)
    header_xpath = "//div[@class='hola']"
    # count = 1
    for ref in suppliers_dict['cat_promo']:
        count = references.index(ref) + 1
        data.search_ref(ref,'productos')
        data.click_first_result("//div[@id='backTable']/div[1]/div[1]/a[1]", ref)
        data.get_title(header_xpath,0, None, count, ref)
        data.get_description(f"{header_xpath}/p[2]", ref)
        data.get_package_info(ref)
        data.get_inventory("//tr[@class='titlesRow']/following-sibling::tr", "//table[@class='tableInfoProd']", ref)
        data.get_img("//img[@id='img_01']", ref)
        # count+=1

    data.close_driver()