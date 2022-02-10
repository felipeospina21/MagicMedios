from get_data import Get_Data
from utils import measures
import time


def get_mp_promo_data(suppliers_dict, prs, references):
    data = Get_Data("mp_promo", prs, references, measures)
    data.execute_driver("https://www.mppromocionales.com/")
    for ref in suppliers_dict["mp_promo"]:
        try:
            idx = data.get_original_ref_list_idx(ref)
            print(idx)
            count = idx + 1
            # data.search_ref(ref,'mat-input-0')
            search_input = data.get_element_with_xpath("//input[@id='mat-input-0']")
            data.send_keys(search_input, ref)
            time.sleep(3)
            data.create_quantity_table(ref, idx)
            title_text = data.get_title_with_xpath(
                "//h1[@class='g-font-size-20 g-font-weight-600']", ref
            )
            subtitle_text = data.get_subtitle_with_xpath(
                "//div[@class='g-font-size-18 g-mb-15']", ref
            )
            data.create_title(title_text, idx, count, ref)
            data.create_subtitle(subtitle_text, idx)

            desc_list = data.get_description(
                "//ul[@class='g-mb-16 g-ml-20 g-pl-0 g-font-size-14']/child::li", ref
            )
            data.create_description(desc_list, idx, ref)
            colors_len = data.get_elements_len_with_xpath(
                "//mat-table[@class='w-100 inventory-tabla mat-table']/child::mat-row"
            )
            data.create_inventory_table(
                colors_len,
                "//mat-table[@class='w-100 inventory-tabla mat-table']",
                idx,
                ref,
            )

            img_src = data.get_img("//img[@class='ng-star-inserted']", ref)
            data.create_img(img_src, idx, 10.39, 7.4, ref)
        except:
            print(f"\nNo se pudo obtener la información del a ref {ref}")

    data.close_driver()
