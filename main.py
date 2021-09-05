from docx import Document
from docx.shared import Inches
from utils import create_supplier_ref_list, scrapp_supplier_data


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

document = Document('./plantillas/plantilla_cot.docx')
cliente = document.add_paragraph()
cliente.add_run(f'Señor(a) {client}.').bold = True
empresa = document.add_paragraph()
empresa.add_run(company).bold = True

asesor = document.add_paragraph()
nombre = asesor.add_run(representative)
contacto= asesor.add_run(contact)
correo = asesor.add_run(email)
correo.add_break()

for ref in strip_reference:
    suppliers = create_supplier_ref_list(ref,suppliers)

scrapp_supplier_data(suppliers, document)
document.save(f'./cotizaciones/cotización_{company}.docx')

print('-------- Proceso Finalizado --------')