from selenium.webdriver.common.by import By
from get_data import Get_Data
from utils import measures
import time

def get_cat_promo_data(suppliers_dict, prs, references):
    data = Get_Data("cat_promo", prs, references, measures)
    data.execute_driver("https://www.catalogospromocionales.com/")

    for ref in suppliers_dict["cat_promo"]:
        try:
            idx = data.get_original_ref_list_idx(ref)
            count = idx + 1
            search_input = data.driver.find_element(By.ID, "productos")
            data.stop_loading()
            data.send_keys(search_input, ref)
            productos=data.driver.find_elements(By.CLASS_NAME, "img-producto")
            for i in range(0, len(productos)):
                result_ref = data.driver.find_elements(By.CLASS_NAME, "ref")[i]
                if ref == result_ref.text.upper():
                    productos[i].click()
                    time.sleep(5)
                    data.create_quantity_table(ref, idx)

                    info_container = data.driver.find_element(By.CLASS_NAME, "hola")
                    info_text_arr = info_container.text.split("\n")
                    title = info_text_arr[0]
                    desc_list = info_text_arr[2:]

                    data.create_title(title, idx, count, ref)
                    data.create_desc(desc_list, idx, ref)

                    # pack_info_table = data.driver.find_element(By.CLASS_NAME, "table-list")
                    # pack_info_arr = pack_info_table.text.split("\n")
                    # pack_info_row1 = pack_info_arr[0].split(":")
                    # pack_info_row2 = pack_info_arr[1].split(":")
                    # data.create_package_info(
                    #     pack_info_row1[0],
                    #     pack_info_row1[1],
                    #     pack_info_row2[0],
                    #     pack_info_row2[1],
                    #     idx,
                    #     ref,
                    # )

                    colors_len = data.get_elements_len_with_xpath(
                        "//tr[@class='titlesRow']/following-sibling::tr[not(@class='hideInfo')]"
                    )
                    data.create_inventory_table(
                        colors_len, "//table[@class='tableInfoProd']", idx, ref
                    )

                    img_src = data.get_img("//img[@id='img_01']", ref)
                    data.create_img(img_src, idx, 8, 8, ref)
                    break
        except:
            print(f"\nNo se pudo obtener la información del a ref {ref}")

    data.close_driver()



