from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from docx.shared import Inches
import time
import requests

class Get_Data:
# (self,url, search_box_id, first_result_xpath, header_xpath, title_index, sub_title_index,
#     xpath_colores, xpath_tabla_colores, img_xpath,
#     supplier, ref_list, document):

    def __init__(self, url, supplier, document):
        self.supplier = supplier
        self.url = url
        self.document= document

        self.path = "C:/chromedriver.exe"
        self.driver = webdriver.Chrome(self.path)
        # self.driver.get('chrome://settings/')
        # self.driver.execute_script('chrome.settingsPrivate.setDefaultZoom(0.25);')
        self.driver.get(self.url)
        time.sleep(10)


    def check_pop_up(self):
        if self.supplier == 'nw_promo':
            try:
                self.driver.execute_script("document.getElementsByClassName('fancybox-overlay fancybox-overlay-fixed labpopup')[0].style.display = 'none';")
            except:
                print("No se encontro popup")

    def search_ref(self, ref, search_box_id):
        try:
            search_input = self.driver.find_element_by_id(search_box_id)
            search_input.clear()
            search_input.send_keys(ref)
            search_input.send_keys(Keys.RETURN)
            time.sleep(3)
        except:
            print("No se pudo encontrar la barra de busqueda")

    def click_first_result(self, first_result_xpath, ref):
        try:
            result = self.driver.find_element_by_xpath(first_result_xpath)
            result.click()
        except:
            print(f"No se pudo encontrar la ref {ref}")

    def get_title(self, header_xpath, title_index, sub_title_index, count, ref):
        # titulo, referencia y descripción
        try:
            header = self.driver.find_element_by_xpath(header_xpath)
            header_text = header.text.split("\n")
            title = header_text[title_index]
            titulo = self.document.add_paragraph()
            titulo.add_run(f'{count}.{title} {ref}').bold = True
            if sub_title_index != None:
                sub_title = header_text[sub_title_index]
                self.document.add_paragraph(sub_title)
        except:
            print(f'No se pudo obtener el título de la ref {ref}')
    
    def get_description(self, desc_xpath, ref):
        # Revisar como estandarizar, todos los procedimientos tienen esta parte diferente
        try:
            desc = self.driver.find_elements_by_xpath(desc_xpath)
            descripcion = self.document.add_paragraph()
            for element in desc:
                desc_line = descripcion.add_run(element.text)
                desc_line.add_break()

        except:
            print(f'No se pudo obtener la descripción de la ref {ref}')
    
    def get_package_info(self, ref):
        try:
            table = "//table[@class='table-list']"
            unit_col_1 = self.driver.find_element_by_xpath(f"{table}/tbody[1]/tr[1]/td[1]")
            unit_col_2 = self.driver.find_element_by_xpath(f"{table}/tbody[1]/tr[1]/td[2]")
            package_col_1 = self.driver.find_element_by_xpath(f"{table}/tbody[1]/tr[2]/td[1]")
            package_col_2 = self.driver.find_element_by_xpath(f"{table}/tbody[1]/tr[2]/td[2]")

            unit_1_text = unit_col_1.text
            unit_2_text = unit_col_2.text
            package_1_text = package_col_1.text
            package_2_text = package_col_2.text

            paragraph = self.document.add_paragraph(f'{unit_1_text}  ')
            paragraph.add_run(unit_2_text).bold = True

            paragraph2 = self.document.add_paragraph(f'{package_1_text}  ')
            paragraph2.add_run(package_2_text).bold = True
        except:
            print(f'No se pudo obtener la cantidad minima de la ref {ref}')

    def get_inventory(self, xpath_colores, xpath_tabla_colores):
        try:
            colores = self.driver.find_elements_by_xpath(xpath_colores)
            q_colores = len(colores)
            tabla_colores = xpath_tabla_colores
            table = self.document.add_table(rows=q_colores, cols=2)
            col1 = table.columns[0]
            col2 = table.columns[1]
            for i in range (1, q_colores + 1):
                if self.supplier == 'cat_promo':
                    color_xpath = f"tbody[1]/tr[{i+2}]/td[1]"
                    inv_color_xpath = f"tbody[1]/tr[{i+2}]/td[4]"
                elif self.supplier == 'mp_promo':
                    pass
                elif self.supplier == 'nw_promo':
                    pass

                color = self.driver.find_element_by_xpath(f"{tabla_colores}/{color_xpath}").text
                inv_color = self.driver.find_element_by_xpath(f"{tabla_colores}/{inv_color_xpath}").text
                col1.cells[i-1].text = color
                col2.cells[i-1].text = inv_color
        except:
            print('No se pudo obtener el inventario')
    
    def get_img(self, img_xpath, ref):
        try:
            if self.supplier == 'promo_op':
                time.sleep(5)

            img = self.driver.find_element_by_xpath(img_xpath)
            img_src = img.get_attribute('src')
            response = requests.get(img_src)

            if response.status_code == 200:
                file = open("./images/sample_image.jpg", "wb")
                file.write(response.content)
                file.close()
                self.document.add_picture("./images/sample_image.jpg", width=Inches(5.25))
                self.document.add_page_break()
            else:
                print(f'Error al descargar imagen de la ref {ref}, status code({response.status_code})')
        except:
            print(f'Error al descargar imagen de la ref {ref}') 

    def close_driver(self):
        self.driver.close()     

   
    # driver.quit()