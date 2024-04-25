# MagicMedios

Automatización cotizador

# Instalación:

1. Instalar python==3.9.6 desde el link https://www.python.org/downloads/ or winget install python -v 3.9.6
2. Instalar git desde el link https://git-scm.com/download/win
3. in C://
 mkdir Robot && cd Robot && git clone https://github.com/felipeospina21/MagicMedios.git && cd MagicMedios
4. Instalar paquetes de python **pip install -r requirements.txt**
5. Agregar archivo .env con variable de ruta y api_token
6. Crear accesos directos en escritorio (enviar a) para actualizar.bat y robot.bat
7. Abrir cotizacion.pptm y guardarlo como \*.ppam
  7.1 Agregar a complementos de PowerPoint
    - click en Mas comandos
    - click en Complementos
    - click en administrar (abajo) seleccionar complementos de Powerpoint
    - click en ir
    - click en agregar nuevo
    - seleccionar cotizacion.ppam
    - click en cerrar

  7.2 Agregar macro ***agregar_bordes*** en cinta de opciones.
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

cp => catalogos Promocionales (cpMU-12-2)  
mp => Mp Promocionales (mpGO0020)  
po => Promo Opción (poBBQ 002)  
cd => CDO Promocionales (cdk8, cdt591, cdt602, cdt578)  
sin prefijo => NW Promocionales (no es necesario ya que todos sus códigos comienzan con NW)
