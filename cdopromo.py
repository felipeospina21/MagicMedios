from utils import get_api_data, text_frame_paragraph, measures
from pptx.util import Cm, Pt
from pptx.dml.color import RGBColor
import requests



url = "http://api.argentina.cdo.dev.yellowspot.com.ar/v1/products/G213?auth_token=Ny8WOEdrmCwBJ3-U-oOYtg"

def get_cdo_promo_data(suppliers_dict, prs, references, measures):
    data = get_api_data(url)
    title = data["name"]
    desc = data["description"]
    for variant in data["variants"]:
        color = variant["color"]
        stock = variant["stock_available"]
        price = variant["net_price"]
        img_src = variant["picture"]["medium"]




print(measures)