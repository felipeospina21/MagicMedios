from get_data import Get_Data

def get_mp_promo_data(suppliers_dict, document):
    data = Get_Data('https://www.mppromocionales.com/', 'mp_promo', document)
    count = 1
    for ref in suppliers_dict['mp_promo']:
        # data.zoom_out_window()
        data.search_ref(ref,'mat-input-0')
        data.get_title_mppromo(count, ref)
        data.get_description("//ul[@class='g-mb-16 g-ml-20 g-pl-0 g-font-size-14']/child::li", ref)

        data.get_inventory("//mat-table[@class='w-100 inventory-tabla mat-table']/child::mat-row", "//mat-table[@class='w-100 inventory-tabla mat-table']")
        data.get_img("//img[@class='ng-star-inserted']", ref)
        count+=1

    data.close_driver()

