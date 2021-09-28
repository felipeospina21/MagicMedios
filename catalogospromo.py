
from get_data import Get_Data
from utils import measures
import time

def get_cat_promo_data(suppliers_dict, prs, references):
    data = Get_Data('cat_promo', prs, references, measures)
    data.execute_driver('https://www.catalogospromocionales.com/')
    header_xpath = "//div[@class='hola']"
    for ref in suppliers_dict['cat_promo']:
        try:
            idx = data.get_original_ref_list_idx(ref)
            count = idx + 1
            # data.search_ref(ref,'productos')
            search_input = data.get_element_with_xpath("//input[@id='productos']")
            
            data.stop_loading()
            data.send_keys(search_input, ref)
            data.click_first_result("//div[@id='backTable']/div[1]/div[1]/a[1]", ref)
            time.sleep(1)
            data.create_quantity_table(ref, idx)
            
            header_text = data.get_title_and_subtitle(header_xpath, 0, 0, ref)
            data.create_title(header_text[0], idx, count, ref)
            desc_list = data.get_description(f"{header_xpath}/p[2]", ref)
            data.create_description(desc_list, idx, ref)
            pack_info_list = data.get_package_info(ref)
            data.create_package_info(pack_info_list[0], pack_info_list[1], pack_info_list[2], pack_info_list[3], idx, ref)
            
            colors_len = data.get_elements_len_with_xpath("//tr[@class='titlesRow']/following-sibling::tr")
            data.create_inventory_table(colors_len, "//table[@class='tableInfoProd']", idx, ref)
            
            img_src = data.get_img("//img[@id='img_01']", ref)
            data.create_img(img_src, idx, 8, 8, ref)
        except:
            print(f"\nNo se pudo obtener la información del a ref {ref}")

    data.close_driver()