from pptx import Presentation
from datetime import datetime
from dotenv import load_dotenv
import locale
import time
import getpass

from new_quotation import New_Quotation

# Variables
start_time = time.time()
username = getpass.getuser()
load_dotenv()
hoy = datetime.now()
prs = Presentation("./plantillas/cotizacion.pptm")
title_slide_layout = prs.slide_layouts[6]
locale.setlocale(locale.LC_TIME, "")

print("-------------****-------------- ")
suppliers = {
    "cat_promo": [],
    "mp_promo": [],
    "promo_op": [],
    "nw_promo": [],
    "cdo_promo": [],
    "best_stock": [],
}

quotation = New_Quotation(prs, title_slide_layout, username)
quotation.set_slides()
quotation.add_header(hoy)
quotation.add_client_name()
suppliers_list = quotation.create_suppliers_ref_list(suppliers)
quotation.scrapp_data(suppliers_list, suppliers)
quotation.create_commercial_policy()
quotation.save()
quotation.create_new_consecutive()

total_time = "{:.2f}".format((time.time() - start_time) / 60)
print(f"-------- Proceso Finalizado en {total_time} minutos --------")