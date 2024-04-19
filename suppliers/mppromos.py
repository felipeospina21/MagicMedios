import time

from get_data import Get_Data
from utils import measures


def get_mp_promo_data(suppliers_dict, prs, references):
    data = Get_Data("mp_promo", prs, references, measures)
    data.execute_driver("https://www.marpicopromocionales.com/")
    for ref in suppliers_dict["mp_promo"]:
        try:
            idx = data.get_original_ref_list_idx(ref)
            count = idx + 1
            search_input = data.get_element_with_xpath(
                "//input[@id='input-buscar-menu']"
            )
            data.send_keys(search_input, ref)
            time.sleep(5)
            data.click_first_result(
                "//a[@class='col-md-3 text-decoration-none text-dark ng-star-inserted']"
            )
            data.create_quantity_table(idx)

            header = data.get_title_with_xpath("//div[@class='card-body']").splitlines()
            reference = header[0]
            title = header[1]

            desc = data.get_title_with_xpath(
                "//div[@class='card-body']/p[@class='ng-star-inserted']"
            )

            data.create_title(f"{reference} {title}", idx, count, ref)
            data.create_subtitle(desc, idx)

            desc_list = data.get_description(
                "//div[@class='card-body']/div[1]/child::li"
            )
            data.create_description(desc_list, idx)

            colors_len = data.get_elements_len_with_xpath(
                "//tbody[@class='text-center text-pequeno-x1 align-middle']/child::tr"
            )
            data.create_inventory_table(
                colors_len,
                "//tbody[@class='text-center text-pequeno-x1 align-middle']",
                idx,
            )
            #
            img_src = data.get_img("//img[@id='imagen-material-0']")
            data.create_img(img_src, idx, 7.4, ref)
        except Exception as e:
            print(f"\nNo se pudo obtener la información del a ref {ref}")
            raise Exception(e)

    data.close_driver()
