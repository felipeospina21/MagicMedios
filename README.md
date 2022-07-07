# MagicMedios

Automatización cotizador

# Instalación:

1. Instalar python==3.9.6 desde el link https://www.python.org/downloads/ or winget install python -v 3.8.6
2. Instalar git desde el link https://git-scm.com/download/win
3. git clone mkdiin C:/Robot
4. Instalar paquetes de python **pip install -r requirements.txt**
5. Agregar archivo .env con variable de ruta y api_token
6. Crear archivo .bat para ejecutar y actualizar el programa.
  **Actualizar**
    cd ../../../Robot/MagicMedios
    git restore --staged .
    git pull
    pause
    **Ejecutar**
    cd ../../../Robot/MagicMedios
    python main.py
7. Abrir cotizacion.pptm y guardarlo como \*.ppam
  7.1 Agregar a complementos de PowerPoint 
  7.2 Agregar macro ***agregar_bordes*** en cinta de opciones.

# Uso:

1. Escribir el nombre del cliente (Ej: juan pérez) => no importa si se usa o no mayusculas, el sistema siempre lo formatea para que queden las iniciales en mayusculas (Juan Pérez).
2. Escribir nombre de la empresa del cliente (ej: nutresa) => no importa si se usa o no mayusculas, el sistema siempre lo formatea para que queden las iniciales en mayusculas (Nutresa).
3. Escribir el listado de codigos a consultar separados por comas. Para que le programa pueda identificar a que proveedor pertenece cada código se debe escribir con el prefijo correspondiente a cada proveedor. No importa si se usa mayusculas o minusculas.

## Prefijos Proveedores:

cp => catalogos Promocionales (cpADV-STY)  
mp => Mp Promocionales (mpGO0020)  
po => Promo Opción (poAGTC 022 AR)  
cd => CDO Promocionales (cdU315)  
sin prefijo => NW Promocionales (no es necesario ya que todos sus códigos comienzan con NW)
