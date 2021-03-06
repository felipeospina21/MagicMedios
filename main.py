from utils import create_supplier_ref_list, text_frame_paragraph
from catalogospromo import get_cat_promo_data
from mppromos import get_mp_promo_data
from nwpromo import get_nw_promo_data
from promoop import get_promo_op__data
from cdopromo import get_cdo_promo_data
from pptx import Presentation
from pptx.util import Cm
from pptx.enum.text import PP_ALIGN
from datetime import datetime
from dotenv import load_dotenv
import locale
import time
import os
import getpass

# Variables
start_time = time.time()
username = getpass.getuser()
load_dotenv()
file_path = os.environ.get("FILE_PATH")
cotizaciones_path = os.environ.get("COTIZACIONES_PATH")
hoy = datetime.now()
prs = Presentation("./plantillas/cotizacion.pptm")
title_slide_layout = prs.slide_layouts[6]
locale.setlocale(locale.LC_TIME, "")

print("-------------****-------------- ")
client = input("Ingrese nombre cliente: ").title()
company = input("Ingrese nombre empresa: ").upper()
rep_name = input(
    "Ingrese nombre asesor comercial (sergio, carlos, ale, juli, com): "
).lower()
reference = (
    input("Ingrese referencias a consultar (separadas por coma): ").upper().split(",")
)
strip_reference = [ref.strip() for ref in reference]
ref_q = len(reference)

# Load header info
if username == "felipe" or username == "felip":
    consecutivo_path = f"{file_path}/data/consecutivo.txt"
else:
    consecutivo_path = f"{cotizaciones_path}/Z consecutivo.txt"


file = open(consecutivo_path, "r")
consecutivo = file.readline().strip()
file.close()

# Routes
if username == "felipe" or username == "felip":
    comercial_path = f"{file_path}/data/comercial.txt"
    carlos_path = f"{file_path}/data/carlos.txt"
    sergio_path = f"{file_path}/data/sergio.txt"
    juliana_path = f"{file_path}/data/juliana.txt"
    alejandra_path = f"{file_path}/data/sergio.txt"
    save_path = f"./cotizaciones/cotización_{company}.pptm"
    footer_path = f"{file_path}/data/data.txt"
else:
    comercial_path = f"{cotizaciones_path}/data/comercial.txt"
    carlos_path = f"{cotizaciones_path}/data/carlos.txt"
    sergio_path = f"{cotizaciones_path}/data/sergio.txt"
    juliana_path = f"{cotizaciones_path}/data/juliana.txt"
    alejandra_path = f"{cotizaciones_path}/data/alejandra.txt"
    save_path = f"{cotizaciones_path}/Cotización N°{consecutivo} - {company} - Magic Medios SAS.pptm"
    footer_path = f"{cotizaciones_path}/data/data.txt"

# Get info asesor comercial
if rep_name == "sergio":
    file = open(sergio_path, "r")
elif rep_name == "carlos":
    file = open(carlos_path, "r")
elif rep_name == "juli":
    file = open(juliana_path, "r")
elif rep_name == "ale":
    file = open(alejandra_path, "r")
else:
    file = open(comercial_path, "r")
    # file = open(comercial_path, "r")

representative = file.readline()
contact = file.readline()
email = file.readline()
file.close()

# Get footer info
file = open(footer_path, "r")
address = file.readline()
web = file.readline()
file.close()

suppliers = {
    "cat_promo": [],
    "mp_promo": [],
    "promo_op": [],
    "nw_promo": [],
    "cdo_promo": [],
    "best_stock": [],
}

# Add slides with logo and footer
num_of_slides = len(reference)
for i in range(0, num_of_slides + 1):
    prs.slides.add_slide(title_slide_layout)
    pic = prs.slides[i].shapes.add_picture(
        "./images/logo.jpg", left=Cm(1), top=Cm(0.5), width=Cm(8.9), height=Cm(1.7)
    )
    # footer = prs.slides[idx].shapes.add_textbox(left=Cm(7.5), top=Cm(22.3), width=Cm(14),height=Cm(3))
    footer = prs.slides[i].shapes.add_textbox(
        left=Cm(0.5), top=Cm(22.8), width=Cm(18), height=Cm(1)
    )
    tf_footer = footer.text_frame
    text_frame_paragraph(
        tf_footer, f"{address} {contact} {email} {web}", 7, False, True
    )

## Firste Slide
# Add Header
txBox = prs.slides[0].shapes.add_textbox(
    left=Cm(12), top=Cm(-0.5), width=Cm(6.6), height=Cm(6)
)
tf = txBox.text_frame
text_frame_paragraph(tf, f"{hoy.day} {hoy.strftime('%B')} de {hoy.year}", 14)
text_frame_paragraph(tf, f"Cot N°{consecutivo}", 14)
text_frame_paragraph(tf, "", 11)
text_frame_paragraph(tf, "Asesor Comercial", 11)
text_frame_paragraph(tf, f"{representative} {contact} {email}", 11)

# Add Client name
header = prs.slides[0].shapes.add_textbox(
    left=Cm(1), top=Cm(1.8), width=Cm(6.4), height=Cm(2)
)
tf_header = header.text_frame
text_frame_paragraph(tf_header, f"Señor(a) {client}.", 14, True)
text_frame_paragraph(tf_header, company, 14, True)

# Create each suppliers ref list
for ref in strip_reference:
    suppliers = create_supplier_ref_list(ref, suppliers)

# Scrapp Data
if len(suppliers["cat_promo"]) != 0:
    get_cat_promo_data(suppliers, prs, strip_reference)
if len(suppliers["mp_promo"]) != 0:
    get_mp_promo_data(suppliers, prs, strip_reference)
if len(suppliers["promo_op"]) != 0:
    get_promo_op__data(suppliers, prs, strip_reference)
if len(suppliers["nw_promo"]) != 0:
    get_nw_promo_data(suppliers, prs, strip_reference)
if len(suppliers["cdo_promo"]) != 0:
    get_cdo_promo_data(suppliers, prs, strip_reference)

# Condiciones comerciales
pic = prs.slides[num_of_slides].shapes.add_picture(
    "./images/condiciones.jpg",
    left=Cm(1),
    top=Cm(4.5),
    width=Cm(17.27),
    height=Cm(16.66),
)


prs.save(save_path)

# Guarda consecutivo
nuevo_consecutivo = int(consecutivo) + 1
file = open(consecutivo_path, "w")
file.write(f"{nuevo_consecutivo}\n")
file.close()

total_time = "{:.2f}".format((time.time() - start_time) / 60)
print(f"-------- Proceso Finalizado en {total_time} minutos --------")
