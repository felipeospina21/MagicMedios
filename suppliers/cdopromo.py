from logging import log
import logging
import os
import time

from get_data import Get_Data
from utils import get_api_data, measures

def crawl(suppliers_dict, prs, references):
    auth_token = os.environ.get("API_TOKEN")
    if auth_token == "":
      logging.error("No se encontro token para la api de CDO", exc_info=True)
      print("No se encontro token para la api de CDO")
      exit()
    data = Get_Data("cdo_promo", prs, references, measures)
    data.execute_driver("https://colombia.cdopromocionales.com/")

    for ref in suppliers_dict["cdo_promo"]:
        idx = data.get_original_ref_list_idx(ref)
        data.create_quantity_table(idx)
        count = idx + 1
        url = f"http://api.colombia.cdopromocionales.com/v1/products/{ref}?auth_token={auth_token}"
        try:
            result = get_api_data(url)
            title = result["name"]
            desc = result["description"]
            colors = result["variants"]
            q_colores = len(colors)
            img_src = colors[0]["detail_picture"]["medium"]

            # NOTE: This data can't be received from the API
            search_input = data.get_element_with_xpath(
                "//input[@id='search_full_text']"
            )
            data.send_keys(search_input, ref)
            time.sleep(2)
            data.click_first_result("//div[@class='variant-container']/a[1]")
            time.sleep(1)
            packing = data.get_description("//div[@class='packing']")

            # NOTE: gets the print method icons to then get its text
            printing_methods_list = ["Métodos de impresión:"]
            number_of_print_methods = data.get_elements_len_with_xpath(
                "//div[@class='printing']/ul[1]/child::li"
            )
            for i in range(1, number_of_print_methods + 1):
                img_element = data.get_element_with_xpath(
                    f"//div[@class='printing']/ul[1]/li[{i}]/img[1]"
                )
                img_title = data.get_element_attribute(img_element, "title")
                printing_methods_list.append(img_title)

            # creates slide
            data.create_title(title, idx, count, ref)
            data.create_subtitle(desc, idx)
            data.create_stock_table_api(q_colores, colors, idx)
            data.create_img(img_src, idx, 0, ref)
            data.create_description(packing, idx)
            data.create_printing_info(printing_methods_list, idx)
        except Exception as e:
            data.error_logging(e)
            raise SystemExit("Error: ",e)

