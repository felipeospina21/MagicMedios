from get_data import Get_Data
from utils import measures
from dotenv import load_dotenv
import os
import time

def get_promo_op__data(suppliers_dict, prs, references):
    data = Get_Data('promo_op', prs, references, measures)
    data.execute_driver('https://www.promoopcioncolombia.co/')
    header_xpath = "//td[@class='table-responsive']"
    load_dotenv()
    password = os.environ.get("PROMO_OP_PASSWORD")
   
    psw_input = data.get_element_with_xpath("//input[@id='psw']")
    data.send_keys(psw_input, password)

    try:
        time.sleep(3)
        data.accept_alert_popup()
        time.sleep(3)
        data.stop_loading()
    except Exception as e:
            print(f"Error de tipo {e.__class__} al tratar de hacer click en alert_popup")

    for ref in suppliers_dict['promo_op']:
        try:
            idx = data.get_original_ref_list_idx(ref)
            count = idx + 1
            search_input = data.get_element_with_xpath("//input[@id='q']")
            data.send_keys(search_input, ref)
            colors_q = data.get_elements_len_with_xpath("//div[@class='col-sm-9']/child::div[@class='col-md-6']")
            data.click_first_result("//a[@class='img-responsive']", ref)
            data.create_quantity_table(ref, idx)
            title_text = data.get_title_with_xpath(f"{header_xpath}/h6[1]", ref)
            subtitle_text = data.get_subtitle_with_xpath(header_xpath, ref)
            data.create_title(title_text, idx, count, ref)
            data.create_subtitle(subtitle_text, idx, ref)
            desc_list = data.get_description("//table[@class='table-hover table-responsive']/tbody[1]/child::tr", ref)
            data.create_description_promo_op(desc_list, idx, ref)
            img_src = data.get_img("//div[@id='imgItem']/img", ref)
            data.create_img(img_src, idx, 8, 8, ref)
            stock_table = data.create_stock_table(colors_q+1, idx, ref)
            stock = data.get_element_with_xpath("//div[@id='ex']/h6[2]").text.split()[1]
            color = data.get_element_with_xpath(f"{header_xpath}/h6[1]").text
            data.fill_stock_table(stock_table, color, stock, 1)
            data.previous_page()

            for i in range(2, colors_q + 1):
                result_ref = data.get_title_with_xpath(f"//div[@class='page-header2']/div[2]/div[2]/div[@class='col-md-6'][{i}]/div[1]/div[2]/div[1]/small[1]/strong[1]", ref).split()
                check_ref = f"{result_ref[0]} {result_ref[1]}".upper()    
                if ref == check_ref:
                    data.click_first_result(f"//div[@class='page-header2']/div[2]/div[2]/div[@class='col-md-6'][{i}]/div[1]/div[1]/a[1]", ref)
                    time.sleep(1)
                    stock = data.get_element_with_xpath("//div[@id='ex']/h6[2]").text.split()[1]
                    color = data.get_element_with_xpath(f"{header_xpath}/h6[1]").text
                    data.fill_stock_table(stock_table, color, stock, i)
                    data.previous_page()
                    time.sleep(1)
                else:
                    data.fill_stock_table(stock_table, "", "", i)
        except:
            print(f"\nNo se pudo obtener la información del a ref {ref}")
            
     
        
    data.close_driver()