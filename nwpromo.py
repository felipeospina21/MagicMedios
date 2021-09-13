from get_data import Get_Data

def get_nw_promo_data(suppliers_dict, prs, references):
    data = Get_Data('https://promocionalesnw.com/', 'nw_promo', prs, references)
    header_xpath = "//div[@class='pb-center-column  col-xs-12 col-sm-6 col-md-6']"
    count = 1
    for ref in suppliers_dict['mp_promo']:
        data.check_pop_up()
        data.search_ref(ref,'search_query_top')
        data.click_first_result("//a[@class='product_image']")
        data.get_title(header_xpath, 0, 4, count, ref)
        data.get_description("//div[@id='short_description_content']/child::div", ref)
        data.get_inventory("//table[@class='table-bordered']/tbody[1]/child::tr", "//table[@class='table-bordered']/tbody[1]")
        data.get_img("//img[@id='bigpic']", ref)
        count+=1

    data.close_driver()