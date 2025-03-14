import time

from get_data import Get_Data
from utils import measures


def get_nw_promo_data(suppliers_dict, prs, references):
    data = Get_Data("nw_promo", prs, references, measures)
    data.execute_driver("https://promocionalesnw.com/")
    header_xpath = "//div[@class='pb-center-column  col-xs-12 col-sm-6 col-md-6']"
    for ref in suppliers_dict["nw_promo"]:
        try:
            idx = data.get_original_ref_list_idx(ref)
            count = idx + 1
            # data.check_pop_up()
            search_input = data.get_element_with_xpath(
                "//input[@id='search_query_top']"
            )
            data.send_keys(search_input, ref)
            time.sleep(10)
            data.click_first_result("//a[@class='product_image']")
            data.create_quantity_table(idx)

            header_text = data.get_title_and_subtitle(header_xpath, 0, 4)
            data.create_title(header_text[0], idx, count, ref)
            data.create_subtitle(header_text[1], idx)
            desc_list = data.get_description(
                "//div[@id='short_description_content']/child::p[1]"
            )
            data.create_description(desc_list, idx)
            colors_len = data.get_elements_len_with_xpath(
                "//table[@class='table-bordered']/tbody[1]/child::tr"
            )
            data.create_inventory_table(
                colors_len, "//table[@class='table-bordered']/tbody[1]", idx
            )

            img_src = data.get_img("//img[@id='bigpic']")
            data.create_img(img_src, idx, 8, ref)
        except Exception as e:
            raise Exception(e)

        print(f"✓ {ref}")
    print(f"✓ referencias nw promo")
    data.close_driver()
