from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from docx.shared import Inches
import time
import requests

def catalogos_promo(ref_list, document):
        
    path = "C:/chromedriver.exe"
    driver = webdriver.Chrome(path)
    driver.get('https://www.catalogospromocionales.com/')
    time.sleep(5)

    for reference in ref_list:

        # Busca referencia
        search_input = driver.find_element_by_id('productos')
        search_input.send_keys(reference)
        search_btn = driver.find_element_by_xpath("//input[@id='productos']/following-sibling::a")
        search_btn.click()

        # Entra en primer resultado
        result = driver.find_element_by_xpath("//div[@id='backTable']/div[1]/div[1]/a[1]")
        result.click()

        # titulo, referencia y descripción
        try:
            header = "//div[@class='hola']"
            title = driver.find_element_by_xpath(f"{header}/h2[1]")
            ref = driver.find_element_by_xpath(f"{header}/p[1]")
            desc = driver.find_element_by_xpath(f"{header}/p[2]")
            title_text = title.text
            ref_text = ref.text
            desc_text = desc.text

            titulo = document.add_paragraph()
            titulo.add_run(f'{ref_list.index(reference)+1}.{title_text} {ref_text}').bold = True
            document.add_paragraph(desc_text)
        except:
            print(f'No se pudo obtener la descripción de la ref {reference}')

        # Cantidad minima
        try:
            table = "//table[@class='table-list']"
            table_col_1 = driver.find_element_by_xpath(f"{table}/tbody[1]/tr[1]/td[1]")
            table_col_2 = driver.find_element_by_xpath(f"{table}/tbody[1]/tr[1]/td[2]")
            col_1_text = table_col_1.text
            col_2_text = table_col_2.text

            paragraph = document.add_paragraph(f'{col_1_text}  ')
            paragraph.add_run(col_2_text).bold = True
        except:
            print(f'No se pudo obtener la cantidad minima de la ref {reference}')

        # Imagen
        try:
            img = driver.find_element_by_id("img_01")
            img_src = img.get_attribute('src')
            response = requests.get(img_src)

            if response.status_code == 200:
                file = open("./images/sample_image.jpg", "wb")
                file.write(response.content)
                file.close()
                document.add_picture("./images/sample_image.jpg", width=Inches(5.25))
                document.add_page_break()
            else:
                print(f'Error al descargar imagen de la ref {reference}, status code({response.status_code})')
        except:
            print(f'Error al descargar imagen de la ref {reference}')

   
    driver.quit()