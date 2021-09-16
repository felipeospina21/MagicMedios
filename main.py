from utils import create_supplier_ref_list, text_frame_paragraph
from catalogospromo import get_cat_promo_data
from mppromos import get_mp_promo_data
from nwpromo import get_nw_promo_data
from promoop import get_promo_op__data
from cdopromo import get_cdo_promo_data
from pptx import Presentation
from pptx.util import Cm
from datetime import datetime
from dotenv import load_dotenv
import locale
import time
import os


# Variables
start_time = time.time()
load_dotenv()
file_path = os.environ.get("FILE_PATH")
hoy = datetime.now()
prs = Presentation("./plantillas/cotizacion.pptx")
title_slide_layout = prs.slide_layouts[6]

locale.setlocale(locale.LC_TIME, '')

# Load header info
file = open(f"{file_path}/data/consecutivo.txt", "r")
consecutivo = file.readline().strip()
file.close()

nuevo_consecutivo = int(consecutivo) + 1
file = open(f"{file_path}/data/consecutivo.txt", "w")
file.write(f"{nuevo_consecutivo}\n")
file.close()

file = open(f"{file_path}/data/data.txt", "r")
representative = file.readline()
contact = file.readline()
email = file.readline()
address = file.readline()
web = file.readline()
file.close()

file = open(f"{file_path}/data/data.txt", "w")
file.write(representative)
file.write(contact)
file.write(email)
file.write(address)
file.write(web)
file.close()

print("-------------****-------------- ")
client = input("Ingrese nombre cliente: ").title()
company = input("Ingrese nombre empresa: ").title()
reference = input("Ingrese referencias a consultar (separadas por coma): ").upper().split(",")
strip_reference = [ref.strip() for ref in reference]
ref_q = len(reference)

suppliers = {
    'cat_promo' : [],
    'mp_promo' : [],
    'promo_op' : [],
    'nw_promo' : [],
    'cdo_promo' : [],
    'best_stock' : [],
}

# Add slides with logo and footer
for idx, ref in enumerate(reference):
    prs.slides.add_slide(title_slide_layout)
    pic = prs.slides[idx].shapes.add_picture("./images/logo.jpg",left=Cm(1), top=Cm(0.5), width=Cm(8.9), height=Cm(1.7))
    footer = prs.slides[idx].shapes.add_textbox(left=Cm(7.5), top=Cm(22.3), width=Cm(14),height=Cm(3))
    tf_footer = footer.text_frame
    text_frame_paragraph(tf_footer,f'{address} {contact} {email} {web}',11 )

# Add Header
txBox = prs.slides[0].shapes.add_textbox(left=Cm(12), top=Cm(-0.5), width=Cm(6.6),height=Cm(6))
tf = txBox.text_frame
text_frame_paragraph(tf,f"{hoy.day} {hoy.strftime('%B')} de {hoy.year}",14 )
text_frame_paragraph(tf,f'Cot N°{consecutivo}',14 )
text_frame_paragraph(tf,"",11 )
text_frame_paragraph(tf,'Asesor Comercial',11 )
text_frame_paragraph(tf,f'{representative} {contact} {email}',11 )

# Add Client name
header = prs.slides[0].shapes.add_textbox(left=Cm(1), top=Cm(2.5), width=Cm(6.4),height=Cm(2))
tf_header = header.text_frame
text_frame_paragraph(tf_header,f'Señor(a) {client}.',14,True )
text_frame_paragraph(tf_header,company,14,True )

# Create each suppliers ref list
for ref in strip_reference:
    suppliers = create_supplier_ref_list(ref,suppliers)

# Scrapp Data
if len(suppliers['cat_promo']) != 0:
    get_cat_promo_data(suppliers, prs, strip_reference)
if len(suppliers['mp_promo']) != 0:
    get_mp_promo_data(suppliers, prs, strip_reference)
if len(suppliers['promo_op']) != 0:
    get_promo_op__data(suppliers, prs, strip_reference)
if len(suppliers['nw_promo']) != 0:
    get_nw_promo_data(suppliers, prs, strip_reference)
if len(suppliers['cdo_promo']) != 0:
    get_cdo_promo_data(suppliers, prs, strip_reference)

prs.save(f'./cotizaciones/cotización_{company}.pptx')

total_time = "{:.2f}".format((time.time() - start_time)/60)
print(f'-------- Proceso Finalizado en {total_time} minutos --------')