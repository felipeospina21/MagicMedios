import asyncio
import getpass
import locale
import time
from datetime import datetime

from dotenv import load_dotenv
from pptx import Presentation

from new_quotation import New_Quotation


async def main():
    # Variables
    start_time = time.time()
    username = getpass.getuser()
    load_dotenv()
    hoy = datetime.now()
    prs = Presentation("./plantillas/cotizacion.pptm")
    title_slide_layout = prs.slide_layouts[6]
    locale.setlocale(locale.LC_TIME, "")

    print("-------------****-------------- ")
    suppliers: dict[str, list[str]] = {
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
    await quotation.scrapp_data(suppliers_list, suppliers)
    quotation.create_commercial_policy()
    quotation.save()
    quotation.create_new_consecutive()

    total_time = "{:.2f}".format((time.time() - start_time) / 60)
    print(f"\n-------- Proceso Finalizado en {total_time} minutos --------")


asyncio.run(main())
