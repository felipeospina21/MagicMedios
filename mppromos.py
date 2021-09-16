from get_data import Get_Data
from utils import measures
import time

def get_mp_promo_data(suppliers_dict, prs, references):
    data = Get_Data('mp_promo', prs, references, measures)
    data.execute_driver('https://www.mppromocionales.com/')
    for ref in suppliers_dict['mp_promo']:
        idx = data.get_original_ref_list_idx(ref)
        count = idx + 1
        data.search_ref(ref,'mat-input-0')
        time.sleep(3)
        data.create_quantity_table(ref, idx)
        title_text = data.get_title_with_xpath("//h1[@class='g-font-size-20 g-font-weight-600']", ref)
        subtitle_text = data.get_subtitle_with_xpath("//div[@class='g-font-size-18 g-mb-15']", ref)
        data.create_title(title_text, idx, count, ref)
        data.create_subtitle(subtitle_text, idx, ref)
        
        desc_list = data.get_description("//ul[@class='g-mb-16 g-ml-20 g-pl-0 g-font-size-14']/child::li", ref)
        data.create_description(desc_list, idx, ref)
        colors_list = data.get_inventory("//mat-table[@class='w-100 inventory-tabla mat-table']/child::mat-row", ref)
        data.create_inventory_table(colors_list[2], colors_list[0], colors_list[1], "//mat-table[@class='w-100 inventory-tabla mat-table']", idx, ref)

        img_src = data.get_img("//img[@class='ng-star-inserted']", ref)
        data.create_img(img_src, idx, ref)


    data.close_driver()

