from get_data import Get_Data
from utils import measures
import time

def get_mp_promo_data(suppliers_dict, prs, references):
    data = Get_Data('https://www.mppromocionales.com/', 'mp_promo', prs, references, measures)
    for ref in suppliers_dict['mp_promo']:
        idx = data.get_original_ref_list_idx(ref)
        count = idx + 1
        data.search_ref(ref,'mat-input-0')
        time.sleep(3)
        data.create_quantity_table(ref, idx)
        data.get_title_with_xpath("//h1[@class='g-font-size-20 g-font-weight-600']", "//div[@class='g-font-size-18 g-mb-15']",count, ref, idx)
        data.get_description("//ul[@class='g-mb-16 g-ml-20 g-pl-0 g-font-size-14']/child::li", ref, idx)
        data.get_inventory("//mat-table[@class='w-100 inventory-tabla mat-table']/child::mat-row", "//mat-table[@class='w-100 inventory-tabla mat-table']", ref, idx)
        data.get_img("//img[@class='ng-star-inserted']", ref, idx)


    data.close_driver()

