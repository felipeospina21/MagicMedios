from get_data import Get_Data
from utils import measures
import time


def get_nw_promo_data(suppliers_dict, prs, references):
    data = Get_Data("nw_promo", prs, references, measures)
    data.execute_driver("https://promocionalesnw.com/")
    header_xpath = "//div[@class='pb-center-column  col-xs-12 col-sm-6 col-md-6']"
    for ref in suppliers_dict["nw_promo"]:
        try:
            idx = data.get_original_ref_list_idx(ref)
            count = idx + 1
            data.check_pop_up()
            # data.search_ref(ref,'search_query_top')
            search_input = data.get_element_with_xpath(
                "//input[@id='search_query_top']"
            )
            data.send_keys(search_input, ref)
            time.sleep(10)
            data.click_first_result("//a[@class='product_image']")
            data.create_quantity_table(ref, idx)

            header_text = data.get_title_and_subtitle(header_xpath, 0, 4, ref)
            data.create_title(header_text[0], idx, count, ref)
            data.create_subtitle(header_text[1], idx)
            desc_list = data.get_description(
                "//div[@id='short_description_content']/child::p[1]", ref
            )
            data.create_description(desc_list, idx, ref)
            colors_len = data.get_elements_len_with_xpath(
                "//table[@class='table-bordered']/tbody[1]/child::tr"
            )
            data.create_inventory_table(
                colors_len, "//table[@class='table-bordered']/tbody[1]", idx, ref
            )

            img_src = data.get_img("//img[@id='bigpic']", ref)
            data.create_img(img_src, idx, 8, 8, ref)
        except:
            print(f"\nNo se pudo obtener la información del a ref {ref}")
    data.close_driver()
