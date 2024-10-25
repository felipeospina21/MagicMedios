import os
import time

from dotenv import load_dotenv

from get_data import Get_Data
from utils import measures


def get_data(suppliers_dict, prs, references):
    data = Get_Data("promo_op", prs, references, measures)
    data.execute_driver("https://www.promoopcioncolombia.co/")
    header_xpath = "//table[@class='table table-hover table-responsive']/tbody[1]"
    # header_xpath = "//td[@class='table-responsive']"
    load_dotenv()
    password = os.environ.get("PROMO_OP_PASSWORD")

    psw_input = data.get_element_with_xpath("//input[@id='psw']")
    data.send_keys(psw_input, password)

    try:
        time.sleep(5)
        data.accept_alert_popup()
        time.sleep(5)
        data.stop_loading()
    except Exception as e:
        print(f"Error de tipo {e.__class__} al tratar de hacer click en alert_popup")

    for ref in suppliers_dict["promo_op"]:
        try:
            ref_idx = data.get_original_ref_list_idx(ref)
            search_input = data.get_element_with_xpath("//input[@id='q']")
            data.send_keys(search_input, ref)
            data.click_first_result("//a[@class='img-responsive ']")
            time.sleep(1)
            colors_q = data.get_elements_len_with_xpath(
                "//table[@class='table table-striped']/tbody[1]/child::tr"
            )
            data.create_quantity_table(ref_idx)
            title_text = data.get_title_with_xpath(f"{header_xpath}/tr[1]/td[1]/h6[1]")
            subtitle_text = data.get_subtitle_with_xpath(f"{header_xpath}/tr[2]/td[1]")
            data.create_title(title_text, ref_idx, ref_idx + 1, ref)
            data.create_subtitle(subtitle_text, ref_idx)

            desc_list = data.get_description(f"{header_xpath}/child::tr")
            data.create_description_promo_op(desc_list, ref_idx)
            stock_table = data.create_stock_table(colors_q, ref_idx)
            colors_elements = data.get_elements_with_xpath(
                "//ul[@class='colors']/child::li"
            )
            colors_stock = []
            img_path = "//div[@id='img-list-1']/div[1]/img"

            # Color Unico
            if len(colors_elements) == 0:
                stock = data.get_element_with_xpath(
                    "//table[@class='table table-striped']/tbody[1]/tr[2]/td[4]"
                ).text
                colors_stock.append({"title": "Color Único", "stock": stock})
                img_src = data.get_img(img_path)
                data.create_img(img_src, ref_idx, 8, ref)

            # Varios Colores
            else:
                data.click_first_result("//ul[@class='colors']/li[1]")
                img_src = data.get_img(img_path)

                data.create_img(img_src, ref_idx, 8, ref)
                for color in colors_elements:
                    title = data.get_element_attribute(color, "title")
                    color_rgb = color.value_of_css_property("background-color")
                    colors_stock.append({"title": title, "color_rgb": color_rgb})

                for i in range(0, colors_q - 1):
                    color_element = data.get_element_with_xpath(
                        f"//table[@class='table table-striped']/tbody[1]/tr[{i+2}]/td[2]/li[1]"
                    )
                    color = data.get_element_css_property(
                        color_element, "background-color"
                    )
                    stock = data.get_element_with_xpath(
                        f"//table[@class='table table-striped']/tbody[1]/tr[{i+2}]/td[4]"
                    ).text

                    for element in colors_stock:
                        if element.get("color_rgb") == color:
                            element.update({"stock": stock})

            for ref_idx, element in enumerate(colors_stock):
                color = element.get("title")
                stock = element.get("stock")
                data.fill_stock_table(stock_table, color, stock, ref_idx + 1)

        except Exception as e:
            raise Exception(e)

    data.close_driver()
