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

from new_quotation import New_Quotation

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
program_flow = input("Digite el número de la acción que desea realizar: \n[1] Crear nueva cotizacion \n[2] Crear nuevo usuario\n> ")

if program_flow == '1':
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



  # Guarda consecutivo
  nuevo_consecutivo = int(consecutivo) + 1
  file = open(consecutivo_path, "w")
  file.write(f"{nuevo_consecutivo}\n")
  file.close()

  total_time = "{:.2f}".format((time.time() - start_time) / 60)
  print(f"-------- Proceso Finalizado en {total_time} minutos --------")

else:

  suppliers = {
      "cat_promo": [],
      "mp_promo": [],
      "promo_op": [],
      "nw_promo": [],
      "cdo_promo": [],
      "best_stock": [],
  }

  quotation = New_Quotation( file_path, prs, title_slide_layout)
  quotation.set_slides()
  quotation.add_header(hoy)
  quotation.add_client_name()
  suppliers_list = quotation.create_suppliers_ref_list(suppliers)
  quotation.scrapp_data(suppliers_list, suppliers)
  quotation.create_commercial_policy()
  quotation.save()

