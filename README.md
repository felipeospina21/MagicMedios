# MagicMedios
Automatización cotizador

# Instalación:
1. Instalar python desde el link https://www.python.org/downloads/
2. Instalar paquetes de python en requirements.txt
3. Instalar Chrome Driver (https://sites.google.com/a/chromium.org/chromedriver/downloads o https://sites.google.com/chromium.org/driver/)
3.1 Revisar version de chrome, para saber cuál instalar.
3.2 Pegarlo en la raiz "C:"
4. Agregar archivo .env con variable de ruta y api_token
5. Agregar /data/data.txt con datos del asesor
6. Modificar consecutivo.txt y cotizaciones en la ruta final (carpeta compartida)
7. Crear archivo .bat para ejecutar el programa.

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
