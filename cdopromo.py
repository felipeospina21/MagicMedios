from utils import get_api_data, measures
from get_data import Get_Data
from dotenv import load_dotenv
import os

load_dotenv()
auth_token = os.environ.get("api-token")

def get_cdo_promo_data(suppliers_dict, prs, references):
    data = Get_Data('cdo_promo', prs, references, measures)
    for ref in suppliers_dict['cdo_promo']:
        idx = data.get_original_ref_list_idx(ref)
        count = idx + 1
        url = f"http://api.argentina.cdo.dev.yellowspot.com.ar/v1/products/{ref}?auth_token={auth_token}"
        result = get_api_data(url)
        title = result["name"]
        desc = result["description"]
        colors = result["variants"]
        img_src = colors[0]["picture"]["medium"]
        q_colores = len(colors)
        data.create_title(title, idx, count, ref)
        data.create_quantity_table(ref, idx)
        data.create_subtitle(desc, idx, ref)
        data.create_img(img_src, idx, ref)
        
        # for i, variant in enumerate(colors):
        # color = variant["color"]
        # stock = str(variant["stock_available"])
        
        data.create_stock_table_api(q_colores, colors, idx, ref)



