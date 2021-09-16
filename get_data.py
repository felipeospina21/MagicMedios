from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pptx.util import Cm, Pt
from pptx.dml.color import RGBColor
from utils import text_frame_paragraph
import requests
import time
import re

class Get_Data:
    def __init__(self, url, supplier, prs, references, measures):
        self.supplier = supplier
        self.url = url
        self.prs= prs
        self.references = references
        self.lf_1 = Cm(measures["lf_1"])
        self.lf_2 = Cm(measures["lf_2"])
        self.lf_3 = Cm(measures["lf_3"])

        self.t_1 = Cm(measures["t_1"])
        self.t_2 = Cm(measures["t_2"])
        self.t_3 = Cm(measures["t_3"])
        self.t_4 = Cm(measures["t_4"])
        self.t_5 = Cm(measures["t_5"])
        self.t_6 = Cm(measures["t_6"])

        self.w_1 = Cm(measures["w_1"])
        self.w_2 = Cm(measures["w_2"])
        self.w_3 = Cm(measures["w_3"])

        self.h_1 = Cm(measures["h_1"])
        self.h_2 = Cm(measures["h_2"])
        self.h_3 = Cm(measures["h_3"])
        self.h_4 = Cm(measures["h_4"])
        self.h_5 = Cm(measures["h_5"])

        self.path = "C:/chromedriver.exe"
        self.driver = webdriver.Chrome(self.path)
        self.driver.set_page_load_timeout(20)
        if self.supplier == 'mp_promo':
            self.driver.get('chrome://settings/')
            self.driver.execute_script('chrome.settingsPrivate.setDefaultZoom(0.25);')
        try:
            self.driver.get(self.url)
        except Exception as e:
            print(f"Error de tipo {e.__class__}")

        time.sleep(5)

    def check_pop_up(self):
        if self.supplier == 'nw_promo':
            try:
                self.driver.execute_script("document.getElementsByClassName('fancybox-overlay fancybox-overlay-fixed labpopup')[0].style.display = 'none';")
            except Exception as e:
                print(f"Error de tipo {e.__class__}")
                print("No se encontro overlay")

    def search_ref(self, ref, search_box_id):
        try:
            # element_present =  WebDriverWait(self.driver, 30).until(
            #         EC.presence_of_element_located((By.ID, search_box_id))
            #     )

            search_input = self.driver.find_element_by_id(search_box_id)
            time.sleep(1)
            search_input.clear()
            search_input.send_keys(ref)
            search_input.send_keys(Keys.RETURN)
        except Exception as e:
            print(f"Error de tipo {e.__class__}")
            print("No se pudo encontrar la barra de busqueda")

    def click_first_result(self, first_result_xpath, ref):
        try:
            result = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, first_result_xpath))
                )
            # result = self.driver.find_element_by_xpath(first_result_xpath)
            time.sleep(1)
            result.click()
        except Exception as e:
            print(f"Error de tipo {e.__class__}")
            print(f"No se pudo encontrar la ref {ref}")

    def get_original_ref_list_idx(self, ref) :
        if self.supplier == 'cat_promo':
            return self.references.index("CP" + ref)
        elif self.supplier == 'mp_promo':
            return self.references.index("MP" + ref)
        elif self.supplier == 'promo_op':
            return self.references.index("PO" + ref)
        elif self.supplier == 'nw_promo':
            return self.references.index(ref)
        elif self.supplier == 'cdo_promo':
            return self.references.index("CD" + ref)

    def get_title_and_subtitle(self, header_xpath, title_index, subtitle_index, ref):
        try:
            header = self.driver.find_element_by_xpath(header_xpath)
            header_text = header.text.split("\n")
            title = header_text[title_index]
            subtitle = header_text[subtitle_index]
            return (title, subtitle)

        except Exception as e:
            print(f"Error de tipo {e.__class__}")   
            print(f'No se pudo obtener el título de la ref {ref}')

    def get_title_with_xpath(self, title_xpath, ref):
        try:
            title = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, title_xpath ))
                )
            title = self.driver.find_element_by_xpath(title_xpath)
            return title.text

        except Exception as e:
            print(f"Error de tipo {e.__class__}")
            print(f'No se pudo obtener el título de la ref {ref}')
    
    def get_subtitle_with_xpath(self, sub_title_xpath, ref):
        def get_subtitle_promo_op(subtitle_result):
            split_text = subtitle_result.text.split("\n")
            for txt in split_text:
                if re.search("^Desc", txt):
                    result_idx = split_text.index(txt)

            result = split_text[result_idx].split("Descripción: ")
            return result[1]

        try:
            subtitle = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, sub_title_xpath))
                )
            subtitle = self.driver.find_element_by_xpath(sub_title_xpath)
            if self.supplier == "promo_op":
                subtitle_text = get_subtitle_promo_op(subtitle)
                return subtitle_text

            return subtitle.text
            
        except Exception as e:
            print(f"Error de tipo {e.__class__}")
            print(f'No se pudo obtener el subtítulo de la ref {ref}')

    def get_description(self, desc_xpath, ref):
        try:
            desc = self.driver.find_elements_by_xpath(desc_xpath)
            return desc

        except Exception as e:
            print(f"Error de tipo {e.__class__}")
            print(f'No se pudo obtener la descripción de la ref {ref}')

    def get_package_info(self, ref):
        try:
            table = "//table[@class='table-list']"
            unit_col_1 = self.driver.find_element_by_xpath(f"{table}/tbody[1]/tr[1]/td[1]")
            unit_col_2 = self.driver.find_element_by_xpath(f"{table}/tbody[1]/tr[1]/td[2]")
            package_col_1 = self.driver.find_element_by_xpath(f"{table}/tbody[1]/tr[2]/td[1]")
            package_col_2 = self.driver.find_element_by_xpath(f"{table}/tbody[1]/tr[2]/td[2]")
            table_texts_list = [unit_col_1.text, unit_col_2.text, package_col_1.text, package_col_2.text]

            return table_texts_list

        except Exception as e:
            print(f"Error de tipo {e.__class__}")
            print(f'No se pudo obtener la info de empaque de la ref {ref}')

    def get_inventory(self, xpath_colores, ref):
        try:
            time.sleep(1)
            colores = self.driver.find_elements_by_xpath(xpath_colores)
            q_colores = len(colores)

            for i in range (1, q_colores + 1):
                if self.supplier == 'cat_promo':
                    color_xpath = f"tbody[1]/tr[{i+2}]/td[1]"
                    inv_color_xpath = f"tbody[1]/tr[{i+2}]/td[4]"
                    return color_xpath, inv_color_xpath, q_colores

                elif self.supplier == 'mp_promo':
                    color_xpath = f"mat-row[{i}]/mat-cell[3]/span[2]"
                    inv_color_xpath = f"mat-row[{i}]/mat-cell[7]/span[2]"
                    return color_xpath, inv_color_xpath, q_colores

                elif self.supplier == 'nw_promo':
                    color_xpath = f"tr[{i}]/td[1]"
                    inv_color_xpath = f"tr[{i}]/td[5]"
                    return color_xpath, inv_color_xpath, q_colores

                else:
                    print("proveedor sin inventario")

        except Exception as e:
            print(f"Error de tipo {e.__class__}")
            print(f'No se pudo obtener los colores de la ref {ref}')
            
    def get_img(self, img_xpath, ref):
        try:
            if self.supplier == 'promo_op':
                time.sleep(5)

            img = self.driver.find_element_by_xpath(img_xpath)
            img_src = img.get_attribute('src')
            response = requests.get(img_src)

            return response

        except Exception as e:
            print(f"Error de tipo {e.__class__}")
            print(f'No se pudo encontrar la imagen de la ref {ref}') 

    def create_quantity_table(self, ref, idx):
        try:
            table = self.prs.slides[idx].shapes.add_table(3 , 2, self.lf_3, self.t_5, self.w_1, self.h_2).table
            table.cell(0,0).text = "Cantidad (und)"
            table.cell(0,1).text = "Valor unitario"
            table.rows[0].height = Cm(0.5)
            table.first_row = True
            table.horz_banding = False
            for i in range (1, 3):
                table.rows[i].height = Cm(0.5)
                # Cell Color
                cell1 = table.cell(i,0)
                cell2 = table.cell(i,1)
                cell1.fill.solid()
                cell1.fill.fore_color.rgb = RGBColor(255,255,255)
                cell2.fill.solid()
                cell2.fill.fore_color.rgb = RGBColor(255,255,255)
                
            table.columns[0].width = Cm(3)
            table.columns[1].width = Cm(9.5)
        except Exception as e:
            print(f"Error al crear tabla de cantidades de la ref {ref} ({e.__class__})")

    def create_title(self, title_text, idx, count, ref):
        try:
            title = title_text
            titulo = self.prs.slides[idx].shapes.add_textbox(left=self.lf_1, top=self.t_1, width=self.w_1, height=self.h_1) 
            tf_titulo= titulo.text_frame
            text_frame_paragraph(tf_titulo,f'{count}.{title} {ref}',12,True )

        except Exception as e:
            print(f"Error de tipo {e.__class__}")   
            print(f'No se pudo crear el título de la ref {ref}')

    def create_subtitle(self, subtitle_text, idx, ref):
        try:
            subtitle = subtitle_text
            sub_titulo = self.prs.slides[idx].shapes.add_textbox(left=self.lf_1, top=self.t_2, width=self.w_1,height=self.h_2)
            tf_sub_titulo= sub_titulo.text_frame
            tf_sub_titulo.word_wrap = True
            text_frame_paragraph(tf_sub_titulo,subtitle,11,True )

        except Exception as e:
            print(f"Error de tipo {e.__class__}")   
            print(f'No se pudo crear el subtítulo de la ref {ref}')

    def create_description(self, desc_list, idx, ref):
        try:
            description = self.prs.slides[idx].shapes.add_textbox(left=self.lf_1, top=self.t_3, width=self.w_1,height=self.h_3)
            tf_desc= description.text_frame
            tf_desc.word_wrap = True
            for element in desc_list:
                text_frame_paragraph(tf_desc, element.text, 11 )

        except Exception as e:
            print(f"Error de tipo {e.__class__}")
            print(f'No se pudo crear la descripción de la ref {ref}')

    def create_package_info(self, unit_1_text, unit_2_text, package_1_text, package_2_text, idx, ref):
        try:
            p1 = self.prs.slides[idx].shapes.add_textbox(left=self.lf_1, top=self.t_4, width=self.w_1,height=self.h_2)
            tf_p1= p1.text_frame
         
            text_frame_paragraph(tf_p1,f'{unit_1_text} {unit_2_text}',11,True )
            text_frame_paragraph(tf_p1,f'{package_1_text} {package_2_text}',11,True )

        except Exception as e:
            print(f"Error de tipo {e.__class__}")
            print(f'No se pudo crear la info de empaque de la ref {ref}')

    def create_inventory_table(self, q_colores, color_xpath, inv_color_xpath, xpath_tabla_colores, idx, ref):
        try:
            cols = 2
            rows = q_colores
            table = self.prs.slides[idx].shapes.add_table(rows + 1, cols, self.lf_1, self.t_6, self.w_2, self.h_4).table
            
            # Table Header
            h1 = table.cell(0,0)
            h2 = table.cell(0,1)
            h1.text = "Color"
            h2.text = "Inventario"
            h1.text_frame.paragraphs[0].font.size = Pt(9)
            h2.text_frame.paragraphs[0].font.size = Pt(9)
            table.rows[0].height = Cm(0.5)
            table.first_row = False
            table.horz_banding = False

            for i in range (1, q_colores + 1):
                try:
                    color = self.driver.find_element_by_xpath(f"{xpath_tabla_colores}/{color_xpath}").text
                    inv_color = self.driver.find_element_by_xpath(f"{xpath_tabla_colores}/{inv_color_xpath}").text
                except Exception as e:
                    print(f'No se pudo obtener el inventario de la ref {ref} // Error de tipo {e.__class__}')

                c1 = table.cell(i, 0)
                c1.text = color
                c1.text_frame.paragraphs[0].font.size = Pt(9)
                c2 = table.cell(i, 1)
                c2.text = inv_color
                c2.text_frame.paragraphs[0].font.size = Pt(9)
                table.rows[i].height = Cm(0.5)
                # Cell Color
                cell1 = table.cell(i,0)
                cell2 = table.cell(i,1)
                cell1.fill.solid()
                cell1.fill.fore_color.rgb = RGBColor(255,255,255)
                cell2.fill.solid()
                cell2.fill.fore_color.rgb = RGBColor(255,255,255)
            
            table.columns[0].width = Cm(3.8)
            table.columns[1].width = Cm(2.2)
        except Exception as e:
            print(f"Error de tipo {e.__class__}")
            print(f'No se pudo crear la tabla de inventario de la ref {ref}')

    def create_img(self, response, idx, ref):
        try:
            if response.status_code == 200:
                file = open("./images/sample_image.jpg", "wb")
                file.write(response.content)
                file.close()
                self.prs.slides[idx].shapes.add_picture("./images/sample_image.jpg",left=self.lf_2, top=self.t_6, width=self.w_3, height=self.h_5)
            else:
                print(f'Error al descargar imagen de la ref {ref}, status code({response.status_code})')

        except Exception as e:
            print(f"Error de tipo {e.__class__}")
            print(f'Error al crear la imagen de la ref {ref}')

    def close_driver(self):
        self.driver.close()     

   