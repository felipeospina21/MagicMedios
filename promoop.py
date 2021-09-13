from get_data import Get_Data

def get_promo_op__data(suppliers_dict, prs, references):
    data = Get_Data('https://www.promoopcioncolombia.co/', 'promo_op', prs, references)
    header_xpath = "//td[@class='table-responsive']"
    count = 1
    for ref in suppliers_dict['promo_op']:
        data.search_ref(ref,'q')
        data.click_first_result("//a[@class='img-responsive']", ref)
        data.get_title(header_xpath,2, 3, count, ref)
        data.get_description("//table[@class='table-hover table-responsive']/tbody[1]/child::tr", ref)
        data.get_img("//div[@id='imgItem']/img", ref)
        count+=1

    data.close_driver()