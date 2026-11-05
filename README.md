# MagicMedios

Automatización del proceso de cotización para una empresa de publicidad y merchandising (Magic Medios).

Dado un cliente y una lista de códigos de producto, el robot consulta los portales de varios proveedores con [Playwright](https://playwright.dev/python/), extrae título, descripción, precios e imágenes de cada referencia, y genera una presentación de PowerPoint (`.pptx`) con la cotización lista para enviar. Lleva un consecutivo de cotizaciones y registra un log de la ejecución.

## Cómo funciona

1. Pide el nombre del cliente, la empresa y el listado de códigos (con prefijo de proveedor).
2. Busca cada código en el portal del proveedor correspondiente (`suppliers/`).
3. Si algún código no se encuentra, permite reintentar solo con esos códigos.
4. Arma la presentación a partir de la plantilla `plantillas/cotizacion.pptm` (encabezado, datos del cliente, una diapositiva por referencia y política comercial).
5. Guarda el archivo e incrementa el consecutivo.

## Stack

- Python 3.12 o superior (el código usa la sintaxis `type`; los pasos de instalación de abajo mencionan 3.9.6 y están desactualizados)
- Playwright (scraping asíncrono) y `requests`
- `python-pptx` (generación de la cotización)
- `python-dotenv`
- Ruff (lint) y Makefile con atajos de ejecución

## Variables de entorno

Archivo `.env` en la raíz (solo se listan los nombres):

```
COTIZACIONES_PATH=
API_TOKEN=
MP_USERNAME=
MP_PASSWORD=
PROMO_OP_PASSWORD=
```

## Ejecución

```bash
python main.py                 # modo normal (pide cliente, empresa y usuario)
make start                     # idem, vía Makefile
make debug h=false             # modo debug (archivo de prueba, sin prompts)
make test                      # modo test
make load l=3                  # prueba de carga del scraper (sin generar PPTX)
make lint                      # ruff check
```

Opciones de línea de comandos: `--debug`, `--test`, `--load_test N`, `--concurrent_tasks N` y `--headless true|false`.

## Estructura

```
main.py            # Flujo principal
app.py             # Argumentos, prompts y consecutivo
scraper.py         # Orquestación de Playwright
suppliers/         # Un módulo por proveedor (cdopromo, mppromos, nwpromo, promoop, magicmedios)
presentation.py    # Generación del PowerPoint
entities/          # Tipos de datos
plantillas/        # Plantilla de cotización
*.bat              # Scripts para instalar/actualizar y correr en Windows
```

> Proyecto personal hecho para un caso de uso concreto. No es una herramienta de uso general.

---

# Instalación:

1. Instalar python==3.9.6 desde el link https://www.python.org/downloads/ or winget install python -v 3.9.6
2. Instalar git desde el link https://git-scm.com/download/win
3. cd C:// && mkdir Robot && cd Robot && git clone https://github.com/felipeospina21/MagicMedios.git && cd MagicMedios
4. Instalar paquetes de python **pip install -r requirements.txt**
5. playwright install or python -m playwright install
6. Agregar archivo .env con variable de ruta y api_token
7. Crear accesos directos en escritorio (enviar a) para actualizar.bat y robot.bat
8. Abrir cotizacion.pptm y guardarlo como \*.ppam
   7.1 Agregar a complementos de PowerPoint
   - click en Mas comandos
   - click en Complementos
   - click en administrar (abajo) seleccionar complementos de Powerpoint
   - click en ir
   - click en agregar nuevo
   - seleccionar cotizacion.ppam
   - click en cerrar

     7.2 Agregar macro **_agregar_bordes_** en cinta de opciones.

   - click en mas comandos
   - click en Personalizar cinta de opcions
   - seleccionar opcion Macros en el select Comandos disponibles en
   - click en Nueva pestana (nombrar Robot)
   - Renombrar grupo (Agregar Bordes)
   - seleccionar macro agregar_bordes
   - click agregar

# Uso:

1. Escribir el nombre del cliente (Ej: juan pérez) => no importa si se usa o no mayusculas, el sistema siempre lo formatea para que queden las iniciales en mayusculas (Juan Pérez).
2. Escribir nombre de la empresa del cliente (ej: nutresa) => no importa si se usa o no mayusculas, el sistema siempre lo formatea para que queden las iniciales en mayusculas (Nutresa).
3. Escribir el listado de codigos a consultar separados por comas. Para que le programa pueda identificar a que proveedor pertenece cada código se debe escribir con el prefijo correspondiente a cada proveedor. No importa si se usa mayusculas o minusculas.

## Prefijos Proveedores:

cp => catalogos Promocionales (cpMU-12-2, cpVA-1153, cpVA-509, cpva-1054, cpva-359-2)  
mp => Mp Promocionales (mpGO0020, mpTE0677, mpBE0412)  
po => Promo Opción (poTMPS 234, poBBQ 002)  
cd => CDO Promocionales (cdk8, cdt591, cdt602, cdt578, cd732)  
sin prefijo => NW Promocionales (no es necesario ya que todos sus códigos comienzan con NW)

test => (MU-12-2, vA-1153 , VA-509, GO0020 , TE0677,k8, t591, TMPS 234, BBQ 002)
test2 => (cpOF-434-2, cptapa mu-07,cpSELVA-MET, cpva-160, cptapa-alcan, cpmu-61)
test => (cpMU-12-2,mpGO0020, cpVA-1153,mpTE0677,cdk8)

### TODO:

1. Automatizar envio de app.log
2. Compilar a .bat https://cx-freeze.readthedocs.io
3. Mejorar manejo de errores
