from utils import get_api_data, measures
from get_data import Get_Data
from dotenv import load_dotenv
import os
import time

load_dotenv()
auth_token = os.environ.get("API_TOKEN")


def get_cdo_promo_data(suppliers_dict, prs, references):
    data = Get_Data("cdo_promo", prs, references, measures)
    data.execute_driver("https://colombia.cdopromocionales.com/")

    for ref in suppliers_dict["cdo_promo"]:
        idx = data.get_original_ref_list_idx(ref)
        data.create_quantity_table(ref, idx)
        count = idx + 1
        url = f"http://api.colombia.cdopromocionales.com/v1/products/{ref}?auth_token={auth_token}"
        try:
            result = get_api_data(url)
            try:
                title = result["name"]
                data.create_title(title, idx, count, ref)
            except Exception as e:
                print(
                    f"No se pudo obtener el titulo de la ref {ref}// Error de tipo {e.__class__}"
                )
            try:
                desc = result["description"]
                data.create_subtitle(desc, idx)
            except Exception as e:
                print(
                    f"No se pudo obtener la descripción de la ref {ref}// Error de tipo {e.__class__}"
                )
            try:
                colors = result["variants"]
                q_colores = len(colors)
                data.create_stock_table_api(q_colores, colors, idx, ref)
            except Exception as e:
                print(
                    f"No se pudo obtener el inventario de la ref {ref}// Error de tipo {e.__class__}"
                )
            try:
                img_src = colors[0]["detail_picture"]["medium"]
                data.create_img(img_src, idx, 0, 0, ref)
            except Exception as e:
                print(
                    f"No se pudo obtener la imagen de la ref {ref}// Error de tipo {e.__class__}"
                )

        except Exception as e:
            print(
                f"Error al obtener la información de la ref {ref} // Error {e.__class__}"
            )

        search_input = data.get_element_with_xpath("//input[@id='search_full_text']")
        data.send_keys(search_input, ref)
        data.click_first_result("//div[@class='variant-container']/a[1]")
        time.sleep(1)
        packing = data.get_description("//div[@class='packing']", ref)
        data.create_description(packing, idx, ref)
        print_methods_q = data.get_elements_len_with_xpath(
            "//div[@class='printing']/ul[1]/child::li"
        )
        printing_methods = ["Métodos de impresión:"]
        for i in range(1, print_methods_q + 1):
            img_element = data.get_element_with_xpath(
                f"//div[@class='printing']/ul[1]/li[{i}]/img[1]"
            )
            img_title = data.get_element_attribute(img_element, "title")
            printing_methods.append(img_title)

        data.create_printing_info(printing_methods, idx)
