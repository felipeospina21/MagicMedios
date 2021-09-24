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
    data.search_ref(password,'psw')
    time.sleep(3)
    data.accept_alert_popup()
    for ref in suppliers_dict['promo_op']:
        idx = data.get_original_ref_list_idx(ref)
        count = idx + 1
        data.search_ref(ref,'q')
        data.click_first_result("//a[@class='img-responsive']", ref)
        data.create_quantity_table(ref, idx)
        # data.get_title(header_xpath,2, 3, count, ref)
        title_text = data.get_title_with_xpath(f"{header_xpath}/h6[1]", ref)
        subtitle_text = data.get_subtitle_with_xpath(header_xpath, ref)
        data.create_title(title_text, idx, count, ref)
        data.create_subtitle(subtitle_text, idx, ref)
        desc_list = data.get_description("//table[@class='table-hover table-responsive']/tbody[1]/child::tr", ref)
        data.create_description(desc_list, idx, ref)
        stock = data.get_promo_op_stock("//div[@id='ex']/h6[2]", ref).split(" ")
        data.create_promo_op_stock(stock[1], idx, ref)
        img_src = data.get_img("//div[@id='imgItem']/img", ref)
        data.create_img(img_src, idx, 8, 8, ref)
        
    data.close_driver()