import time

from get_data import Get_Data
from utils import measures


def crawl(suppliers_dict, prs, references):
    data = Get_Data("mp_promo", prs, references, measures)
    data.execute_driver("https://www.marpicopromocionales.com/")
    for ref in suppliers_dict["mp_promo"]:
        try:
            idx = data.get_original_ref_list_idx(ref)
            search_input = data.get_element_with_xpath(
                "//input[@id='input-buscar-menu']"
            )
            data.send_keys(search_input, ref)
            time.sleep(5)
            data.click_first_result(
                "//a[@class='col-md-3 text-decoration-none text-dark ng-star-inserted']"
            )

            header = data.get_title_with_xpath("//div[@class='card-body']").splitlines()
            reference = header[0]
            title = header[1]

            desc = data.get_title_with_xpath(
                "//div[@class='card-body']/p[@class='ng-star-inserted']"
            )

            desc_list = data.get_description(
                "//div[@class='card-body']/div[1]/child::li"
            )

            number_of_colors = data.get_elements_len_with_xpath(
                "//tbody[@class='text-center text-pequeno-x1 align-middle']/child::tr"
            )

            img_src = data.get_img("//img[@id='imagen-material-0']")

        except Exception as e:
            raise Exception(e)

        try:
            data.create_quantity_table(idx)
            data.create_title(f"{reference} {title}", idx, idx + 1, ref)
            data.create_subtitle(desc, idx)
            data.create_description(desc_list, idx)
            data.create_inventory_table(
                number_of_colors,
                "//tbody[@class='text-center text-pequeno-x1 align-middle']",
                idx,
            )
            data.create_img(img_src, idx, 7.4, ref)

        except Exception as e:
            raise Exception(e)

    data.close_driver()
