import time

from selenium.webdriver.common.by import By

from get_data import Get_Data
from utils import measures


def crawl(suppliers_dict, prs, references):
    data = Get_Data("cat_promo", prs, references, measures)
    data.execute_driver("https://www.catalogospromocionales.com/")

    for ref in suppliers_dict["cat_promo"]:
        try:
            idx = data.get_original_ref_list_idx(ref)
            count = idx + 1
            search_input = data.driver.find_element(By.ID, "productos")
            data.stop_loading()
            data.send_keys(search_input, ref)
            i = 1
            # TODO: add retry variables to replace 3
            # TODO: move this to a global function to be reused (def retry ..)
            while i <= 3:
                productos = data.driver.find_elements(By.CLASS_NAME, "img-producto")
                if len(productos) > 0:
                    break

                i += 1

            productos = data.driver.find_elements(By.CLASS_NAME, "img-producto")
            for i in range(0, len(productos)):
                result_ref = data.driver.find_elements(By.CLASS_NAME, "ref")[i]
                if ref == result_ref.text.upper():
                    productos[i].click()
                    time.sleep(5)

                    info_container = data.driver.find_element(By.CLASS_NAME, "hola")
                    info_text_arr = info_container.text.split("\n")
                    title = info_text_arr[0]
                    desc_list = info_text_arr[2:]

                    number_of_colors = data.get_elements_len_with_xpath(
                        "//tr[@class='titlesRow']/following-sibling::tr[not(@class='hideInfo')]"
                    )
                    img_src = data.get_img("//img[@id='img_01']")

                    data.create_quantity_table(idx)
                    data.create_title(title, idx, count, ref)
                    data.create_desc(desc_list, idx)
                    data.create_inventory_table(
                        number_of_colors, "//table[@class='tableInfoProd']", idx
                    )
                    data.create_img(img_src, idx, 8, ref)

                    break
        except Exception as e:
            raise Exception(e)

    data.close_driver()
