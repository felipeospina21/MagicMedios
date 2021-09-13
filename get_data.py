from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from docx.shared import Inches, Cm
from docx.enum.table import WD_ROW_HEIGHT_RULE
from pptx.enum.text import MSO_AUTO_SIZE
from utils import text_frame_paragraph
import time
import requests

class Get_Data:
    def __init__(self, url, supplier, prs, references):
        self.supplier = supplier
        self.url = url
        self.prs= prs
        self.references = references

        self.path = "C:/chromedriver.exe"
        self.driver = webdriver.Chrome(self.path)
        if self.supplier == 'mp_promo':
            self.driver.get('chrome://settings/')
            self.driver.execute_script('chrome.settingsPrivate.setDefaultZoom(0.25);')
        self.driver.get(self.url)
        time.sleep(5)

    def zoom_out_window(self):
        self.driver.get('chrome://settings/')
        self.driver.execute_script('chrome.settingsPrivate.setDefaultZoom(0.25);')

    def check_pop_up(self):
        if self.supplier == 'nw_promo':
            try:
                self.driver.execute_script("document.getElementsByClassName('fancybox-overlay fancybox-overlay-fixed labpopup')[0].style.display = 'none';")
            except:
                print("No se encontro popup")

    def search_ref(self, ref, search_box_id):
        try:
            search_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, search_box_id))
                )
            # search_input = self.driver.find_element_by_id(search_box_id)
            search_input.clear()
            search_input.send_keys(ref)
            search_input.send_keys(Keys.RETURN)
            # time.sleep(3)
        except:
            print("No se pudo encontrar la barra de busqueda")

    def click_first_result(self, first_result_xpath, ref):
        try:
            result = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, first_result_xpath))
                )
            # result = self.driver.find_element_by_xpath(first_result_xpath)
            result.click()
        except:
            print(f"No se pudo encontrar la ref {ref}")

    def get_title(self, header_xpath, title_index, sub_title_index, count, ref):
        try:
            header = self.driver.find_element_by_xpath(header_xpath)
            header_text = header.text.split("\n")
            title = header_text[title_index]
            slide_idx = self.references.index(ref)
            titulo = self.prs.slides[slide_idx].shapes.add_textbox(left=Cm(1.5), top=Cm(3), width=Cm(19),height=Cm(1))
            tf_titulo= titulo.text_frame
            text_frame_paragraph(tf_titulo,f'{count}.{title} {ref}',12,True )

            # titulo = self.document.add_paragraph()
            # titulo.add_run(f'{count}.{title} {ref}').bold = True
            if sub_title_index != None:
                sub_title = header_text[sub_title_index]
                # self.document.add_paragraph(sub_title)
                sub_titulo = self.prs.slides[slide_idx].shapes.add_textbox(left=Cm(1.5), top=Cm(3.5), width=Cm(19),height=Cm(2))
                tf_sub_titulo= sub_titulo.text_frame
                tf_sub_titulo.word_wrap = True
                text_frame_paragraph(tf_sub_titulo,sub_title,11,True )
        except:
            print(f'No se pudo obtener el título de la ref {ref}')

    def get_title_mppromo(self, count, ref):
        try:
            title = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//h1[@class='g-font-size-20 g-font-weight-600']"))
                )
            title = self.driver.find_element_by_xpath("//h1[@class='g-font-size-20 g-font-weight-600']")
            # title_text = title.text
            # titulo = self.document.add_paragraph()
            # titulo.add_run(f'{count}.{title_text}').bold = True
            slide_idx = self.references.index(ref)
            titulo = self.prs.slides[slide_idx].shapes.add_textbox(left=Cm(1.5), top=Cm(3), width=Cm(19),height=Cm(1))
            tf_titulo= titulo.text_frame
            text_frame_paragraph(tf_titulo,f'{count}.{title.text}',11,True )

        except:
            print(f'No se pudo obtener el título de la ref {ref}')

        try:
            sub_title = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@class='g-font-size-18 g-mb-15']"))
                )
            sub_title = self.driver.find_element_by_xpath("//div[@class='g-font-size-18 g-mb-15']")
            # self.document.add_paragraph(sub_title.text)
            # sub_title_text = sub_title.text
            sub_titulo = self.prs.slides[slide_idx].shapes.add_textbox(left=Cm(1.5), top=Cm(3.5), width=Cm(19),height=Cm(2))
            tf_sub_titulo= sub_titulo.text_frame
            tf_sub_titulo.word_wrap = True
            text_frame_paragraph(tf_sub_titulo,sub_title.text,11,True )
        except:
            print(f'No se pudo obtener el subtítulo de la ref {ref}')
        
    def get_description(self, desc_xpath, ref):
        try:
            desc = self.driver.find_elements_by_xpath(desc_xpath)
            # descripcion = self.document.add_paragraph()
            slide_idx = self.references.index(ref)
            description = self.prs.slides[slide_idx].shapes.add_textbox(left=Cm(1.5), top=Cm(5), width=Cm(19),height=Cm(5))
            tf_desc= description.text_frame
            # text_frame_paragraph(tf_desc,"",11,True )
            for element in desc:
                text_frame_paragraph(tf_desc,element.text,11 )
                # desc_line = descripcion.add_run(element.text)
                # desc_line.add_break()

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

            slide_idx = self.references.index(ref)
            p1 = self.prs.slides[slide_idx].shapes.add_textbox(left=Cm(1.5), top=Cm(8), width=Cm(19),height=Cm(5))
            tf_p1= p1.text_frame
            # p2 = self.prs.slides[slide_idx].shapes.add_textbox(left=Cm(1.5), top=Cm(8.5), width=Cm(6.4),height=Cm(5))
            # tf_p2= p2.text_frame
            text_frame_paragraph(tf_p1,f'{unit_1_text} {unit_2_text}',11,True )
            text_frame_paragraph(tf_p1,f'{package_1_text} {package_2_text}',11,True )
            # paragraph = self.document.add_paragraph(f'{unit_1_text}  ')
            # paragraph.add_run(unit_2_text).bold = True

            # paragraph2 = self.document.add_paragraph(f'{package_1_text}  ')
            # paragraph2.add_run(package_2_text).bold = True
        except:
            print(f'No se pudo obtener la cantidad minima de la ref {ref}')

    def get_inventory(self, xpath_colores, xpath_tabla_colores, ref):
        try:
            self.driver.implicitly_wait(1)
            colores = self.driver.find_elements_by_xpath(xpath_colores)
            q_colores = len(colores)
            tabla_colores = xpath_tabla_colores

            slide_idx = self.references.index(ref)
            cols = 2
            rows = q_colores
            left = Cm(1.5)
            top = Cm(9)
            width = Cm(8)
            height = Cm(8.5)
            table = self.prs.slides[slide_idx].shapes.add_table(rows, cols, left, top, width, height).table
            # table.fill.background()

            # table = self.document.add_table(rows=q_colores, cols=2)
            # col1 = table.columns[0]
            # col2 = table.columns[1]
            for i in range (1, q_colores + 1):
                if self.supplier == 'cat_promo':
                    color_xpath = f"tbody[1]/tr[{i+2}]/td[1]"
                    inv_color_xpath = f"tbody[1]/tr[{i+2}]/td[4]"
                elif self.supplier == 'mp_promo':
                    color_xpath = f"mat-row[{i}]/mat-cell[3]/span[2]"
                    inv_color_xpath = f"mat-row[{i}]/mat-cell[7]/span[2]"
                elif self.supplier == 'nw_promo':
                    color_xpath = f"tr[{i}]/td[1]"
                    inv_color_xpath = f"tr[{i}]/td[5]"

                color = self.driver.find_element_by_xpath(f"{tabla_colores}/{color_xpath}").text
                inv_color = self.driver.find_element_by_xpath(f"{tabla_colores}/{inv_color_xpath}").text
                table.cell(i-1, 0).text = color
                table.cell(i-1, 1).text = inv_color
                table.rows[i-1].height = Cm(0.5)
                # col1.cells[i-1].text = color
                # col1.cells[i-1].width = Cm(4)
                # col2.cells[i-1].text = inv_color
                # col2.cells[i-1].width = Cm(1.4)
                # table.rows[i-1].height = Cm(0.5)
                # table.rows[i-1].height_rule = WD_ROW_HEIGHT_RULE.EXACTLY

            # table.autofit = True
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
                slide_idx = self.references.index(ref)
                pic = self.prs.slides[slide_idx].shapes.add_picture("./images/sample_image.jpg",left=Cm(12), top=Cm(9), width=Cm(13.2), height=Cm(9.5))

                # self.document.add_picture("./images/sample_image.jpg", width=Inches(5.25))
                # self.document.add_page_break()
            else:
                print(f'Error al descargar imagen de la ref {ref}, status code({response.status_code})')
        except:
            print(f'Error al descargar imagen de la ref {ref}') 

    def close_driver(self):
        self.driver.close()     

   