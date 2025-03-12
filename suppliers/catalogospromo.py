import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        except Exception as e:
            print(f"search item {ref} not fount")
            raise Exception(e)

        productos = data.retry(3, "img-producto", ref)

        for i in range(0, len(productos)):
            try:
                result_ref = data.retry(3, "ref", ref)[i]
            except Exception as e:
                raise Exception(e)

            if ref == result_ref.text.upper():
                producto = data.driver.find_elements(By.CLASS_NAME, "img-producto")[i]
                producto.click()
                time.sleep(5)

                try:
                    info_container = data.driver.find_element(By.CLASS_NAME, "hola")
                    info_text_arr = info_container.text.split("\n")
                    title = info_text_arr[0]
                    desc_list = info_text_arr[2:]
                except Exception as e:
                    raise Exception(e)

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

        print(f"✓ {ref}")
    print(f"✓ referencias catalogos")
    data.close_driver()
