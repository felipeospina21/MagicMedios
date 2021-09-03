from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from docx import Document
from docx.shared import Inches
import time
import sys
import requests

path = "C:/chromedriver.exe"
driver = webdriver.Chrome(path)
driver.get('https://www.catalogospromocionales.com/')
time.sleep(5)

file_path = (
    "C:/Users/felipe.ospina/OneDrive - MINEROS/Desktop/repo/projects/MagicMedios"
)
file = open(f"{file_path}/data.txt", "r")
consecutivo = file.readline().strip()
representative = file.readline()
contact = file.readline()
email = file.readline()
file.close()
nuevo_consecutivo = int(consecutivo) + 1

file = open(f"{file_path}/info.txt", "w")
file.write(f"{nuevo_consecutivo}\n")
file.write(representative)
file.write(contact)
file.write(email)
file.close()

print("-------------****-------------- ")
client = input("Ingrese nombre cliente: ").title()
company = input("Ingrese nombre empresa: ").title()
reference = input("Ingrese referencias a consultar (separadas por coma): ").lower().replace(" ", "").split(",")
q = len(reference)

document = Document('plantilla_cot.docx')
cliente = document.add_paragraph()
cliente.add_run(f'Señor(a) {client}.').bold = True
empresa = document.add_paragraph()
empresa.add_run(company).bold = True

asesor = document.add_paragraph()
asesor.add_run(representative).bold = False
contacto = document.add_paragraph()
contacto.add_run(contact).bold = False
correo = document.add_paragraph()
correo.add_run(email).bold = False

for i in range(0, q):

    # Busca referencia
    search_input = driver.find_element_by_id('productos')
    search_input.send_keys(reference[i])
    search_btn = driver.find_element_by_xpath("//input[@id='productos']/following-sibling::a")
    search_btn.click()

    # Entra en primer resultado
    result = driver.find_element_by_xpath("//div[@id='backTable']/div[1]/div[1]/a[1]")
    result.click()

    # Extrae textos
    header = "//div[@class='hola']"
    title = driver.find_element_by_xpath(f"{header}/h2[1]")
    ref = driver.find_element_by_xpath(f"{header}/p[1]")
    desc = driver.find_element_by_xpath(f"{header}/p[2]")
    title_text = title.text
    ref_text = ref.text
    desc_text = desc.text

    table = "//table[@class='table-list']"
    table_col_1 = driver.find_element_by_xpath(f"{table}/tbody[1]/tr[1]/td[1]")
    table_col_2 = driver.find_element_by_xpath(f"{table}/tbody[1]/tr[1]/td[2]")
    col_1_text = table_col_1.text
    col_2_text = table_col_2.text

    # Extrae y guarda Imagen
    img = driver.find_element_by_id("img_01")
    img_src = img.get_attribute('src')
    response = requests.get(img_src)
    file = open("sample_image.jpg", "wb")
    file.write(response.content)
    file.close()

    # Crear cotización en Word
    titulo = document.add_paragraph()
    titulo.add_run(f'{i+1}.{title_text} {ref_text}').bold = True

    document.add_paragraph(desc_text)
    paragraph = document.add_paragraph(f'{col_1_text}  ')
    paragraph.add_run(col_2_text).bold = True

    document.add_picture("sample_image.jpg", width=Inches(5.25))
    document.add_page_break()

document.save(f'cotización_{company}.docx')
driver.quit()