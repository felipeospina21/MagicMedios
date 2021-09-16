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
        data.get_title(header_xpath, 0, 4, count, ref, idx)
        data.get_description("//div[@id='short_description_content']/child::div", ref, idx)
        data.get_inventory("//table[@class='table-bordered']/tbody[1]/child::tr", "//table[@class='table-bordered']/tbody[1]", ref, idx)
        data.get_img("//img[@id='bigpic']", ref, idx)

    data.close_driver()