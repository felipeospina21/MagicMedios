#MagicMedios

Automatización cotizador

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

cp => catalogos Promocionales (cpMU-12-2, cpVA-1153, cpVA-509)  
mp => Mp Promocionales (mpGO0020, mpTE0677)  
po => Promo Opción (poTMPS 234, poBBQ 002)  
cd => CDO Promocionales (cdk8, cdt591, cdt602, cdt578, cd732)  
sin prefijo => NW Promocionales (no es necesario ya que todos sus códigos comienzan con NW)

test => (cpMU-12-2, cpVA-1153, cpVA-509,mpGO0020, mpTE0677,cdk8, cdt591, poTMPS 234, poBBQ 002)
test2 => (cpOF-434-2, cptapa mu-07,cpSELVA-MET, cpva-160, cptapa-alcan, cpmu-61)
test => (cpMU-12-2,mpGO0020, cpVA-1153,mpTE0677,cdk8)

### TODO:

1. Automatizar envio de app.log
2. Compilar a .bat https://cx-freeze.readthedocs.io
3. Mejorar manejo de errores
