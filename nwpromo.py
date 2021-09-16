from get_data import Get_Data
from utils import measures
import time

def get_nw_promo_data(suppliers_dict, prs, references):
    data = Get_Data('https://promocionalesnw.com/', 'nw_promo', prs, references, measures)
    header_xpath = "//div[@class='pb-center-column  col-xs-12 col-sm-6 col-md-6']"
    for ref in suppliers_dict['nw_promo']:
        idx = data.get_original_ref_list_idx(ref)
        count = idx + 1
        data.check_pop_up()
        data.search_ref(ref,'search_query_top')
        time.sleep(2)
        data.click_first_result("//a[@class='product_image']", ref, idx)
        data.create_quantity_table(ref, idx)
        
        header_text = data.get_title_and_subtitle(header_xpath, 0, 4, ref)
        data.create_title(header_text[0], idx, count, ref)
        data.create_subtitle(header_text[1], idx, count, ref)
        desc_list = data.get_description("//div[@id='short_description_content']/child::div", ref)
        data.create_description(desc_list, idx, ref)
        colors_list = data.get_inventory("//table[@class='table-bordered']/tbody[1]/child::tr", ref)
        data.create_inventory_table(colors_list[2], colors_list[0], colors_list[1], "//table[@class='table-bordered']/tbody[1]", idx, ref)

        img_response = data.get_img("//img[@id='bigpic']", ref)
        data.create_img(img_response, idx, ref)

    data.close_driver()