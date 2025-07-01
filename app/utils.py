"""Módulo de utilidades para procesamiento de nombres de archivos y URLs de Teams Video Downloader."""

import datetime
import re
import os

def generar_nombre_archivo(nombre_base):
    """
    Genera el nombre completo del archivo de video a guardar, con formato:
    nombre_usuario_fecha.mp4, dentro de la carpeta 'descargas'.

    Args:
        nombre_base (str): Nombre base ingresado por el usuario.

    Returns:
        str: Ruta completa del archivo de salida.
    """
    fecha = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    carpeta = "descargas"
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    return os.path.join(carpeta, f"{nombre_base}_{fecha}.mp4")

def extraer_url_videomanifest(url):
    """
    Extrae la URL válida para ffmpeg desde un enlace largo de Teams/SharePoint.
    Recorta automáticamente la URL hasta el último 'true' (incluido), si existe.

    Args:
        url (str): URL completa pegada por el usuario.

    Returns:
        str: URL limpia y lista para usar con ffmpeg.
    """
    url = url.strip()
    patron = r"(https://[^\s]+videomanifest\?[^ \n]+)"
    match = re.search(patron, url)
    url_limpia = match.group(1) if match else url

    # Recortar hasta el último 'true' (incluido)
    idx = url_limpia.rfind("true")
    if idx != -1:
        return url_limpia[:idx + len("true")]
    return url_limpia