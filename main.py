from docx import Document
from utils import create_supplier_ref_list, text_frame_paragraph
from catalogospromo import get_cat_promo_data
from mppromos import get_mp_promo_data
from nwpromo import get_nw_promo_data
from promoop import get_promo_op__data
from pptx import Presentation
from pptx.util import Pt, Cm
from datetime import datetime

file_path = (
    "C:/Users/felipe.ospina/OneDrive - MINEROS/Desktop/repo/projects/MagicMedios"
)
file = open(f"{file_path}/data/data.txt", "r")
consecutivo = file.readline().strip()
representative = file.readline()
contact = file.readline()
email = file.readline()
file.close()
nuevo_consecutivo = int(consecutivo) + 1

file = open(f"{file_path}/data/data.txt", "w")
file.write(f"{nuevo_consecutivo}\n")
file.write(representative)
file.write(contact)
file.write(email)
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

hoy = datetime.now()
prs = Presentation()
title_slide_layout = prs.slide_layouts[6]
for ref in reference:
    prs.slides.add_slide(title_slide_layout)
    pic = prs.slides[reference.index(ref)].shapes.add_picture("./images/logo.jpg",left=Cm(1), top=Cm(0.5), width=Cm(8.9), height=Cm(1.7))


txBox = prs.slides[0].shapes.add_textbox(left=Cm(18), top=Cm(-0.5), width=Cm(6.6),height=Cm(6))
tf = txBox.text_frame

text_frame_paragraph(tf,f'{hoy.day} {hoy.month} de {hoy.year}',14 )
text_frame_paragraph(tf,f'Cot N°{consecutivo}',14 )
text_frame_paragraph(tf,"",11 )
text_frame_paragraph(tf,'Asesor Comercial',11 )
text_frame_paragraph(tf,representative,11 )
text_frame_paragraph(tf,contact,11 )
text_frame_paragraph(tf,email,11 )

header = prs.slides[0].shapes.add_textbox(left=Cm(1), top=Cm(1.5), width=Cm(6.4),height=Cm(5))
tf_header = header.text_frame
text_frame_paragraph(tf_header,f'Señor(a) {client}.',14,True )
text_frame_paragraph(tf_header,company,14,True )

for ref in strip_reference:
    suppliers = create_supplier_ref_list(ref,suppliers)

# Scrapp Data
if len(suppliers['cat_promo']) != 0:
    get_cat_promo_data(suppliers, prs, strip_reference)
if len(suppliers['mp_promo']) != 0:
    get_mp_promo_data(suppliers, prs, strip_reference)
# if len(suppliers['promo_op']) != 0:
#     get_promo_op__data(suppliers, prs, strip_reference)
# if len(suppliers['nw_promo']) != 0:
#     get_nw_promo_data(suppliers, prs, strip_reference)


prs.save(f'./cotizaciones/cotización_{company}.pptx')

print('-------- Proceso Finalizado --------')