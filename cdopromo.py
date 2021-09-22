from utils import get_api_data, measures
from get_data import Get_Data
from dotenv import load_dotenv
import os

load_dotenv()
auth_token = os.environ.get("API_TOKEN")

def get_cdo_promo_data(suppliers_dict, prs, references):
    data = Get_Data('cdo_promo', prs, references, measures)
    for ref in suppliers_dict['cdo_promo']:
        print(ref)
        idx = data.get_original_ref_list_idx(ref)
        count = idx + 1
        url = f"http://api.colombia.cdopromocionales.com/v1/products/{ref}?auth_token={auth_token}"
        result = get_api_data(url)
        data.create_quantity_table(ref, idx)
        try:
            title = result["name"]
            data.create_title(title, idx, count, ref)
        except Exception as e:
            print(f'No se pudo obtener el titulo de la ref {ref}// Error de tipo {e.__class__}')
        try:
            desc = result["description"]
            data.create_subtitle(desc, idx, ref)
        except Exception as e:
            print(f'No se pudo obtener la descripción de la ref {ref}// Error de tipo {e.__class__}')
        try:
            colors = result["variants"]
            q_colores = len(colors)
            data.create_stock_table_api(q_colores, colors, idx, ref)
        except Exception as e:
            print(f'No se pudo obtener el inventario de la ref {ref}// Error de tipo {e.__class__}')
        try:
            img_src = colors[0]["detail_picture"]["medium"]
            data.create_img(img_src, idx, 0, 0, ref)
        except Exception as e:
            print(f'No se pudo obtener la imagen de la ref {ref}// Error de tipo {e.__class__}')
        
        
        
        
        
        
        
        


