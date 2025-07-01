# Teams Video Downloader

Aplicación de escritorio para Windows que permite descargar videos de Microsoft Teams, SharePoint y OneDrive a partir de la URL del `videomanifest` usando `ffmpeg`.

## Características

- Interfaz gráfica sencilla y amigable (Tkinter).
- Descarga automática del video usando `ffmpeg`.
- Generación automática del nombre del archivo con fecha y hora.
- Código modular y fácil de mantener.

## Requisitos

- Python 3.x
- ffmpeg instalado y accesible desde el PATH del sistema
- (Opcional) PyInstaller para generar el ejecutable

### Instalación de ffmpeg en Windows

**Opción recomendada (instalador automático):**
1. Ve a [https://github.com/icedterminal/ffmpeg-installer/releases/latest](https://github.com/icedterminal/ffmpeg-installer/releases/latest)
2. Descarga el instalador `.exe` correspondiente a tu sistema.
3. Ejecuta el instalador y sigue los pasos. El instalador configura automáticamente el PATH de Windows.
4. Abre una nueva terminal y ejecuta `ffmpeg -version` para verificar que está correctamente instalado.

**Opción manual (Gyan.dev):**
1. Ve a [https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/).
2. Descarga el archivo **`ffmpeg-release-essentials.zip`** desde la sección "Release builds".
3. Descomprime el archivo descargado.
4. Dentro de la carpeta descomprimida, ubica la carpeta `bin` (contiene `ffmpeg.exe`).
5. Agrega la ruta completa de la carpeta `bin` al **PATH** del sistema operativo Windows:
   - Panel de control → Sistema → Configuración avanzada del sistema → Variables de entorno → Editar la variable `Path` → Agregar la ruta de la carpeta `bin`.
6. Abre una nueva terminal y ejecuta `ffmpeg -version` para verificar que está correctamente instalado.

**Opción manual (BtbN/FFmpeg-Builds):**
1. Ve a [https://github.com/BtbN/FFmpeg-Builds/releases/tag/latest](https://github.com/BtbN/FFmpeg-Builds/releases/tag/latest)
2. Descarga el archivo `ffmpeg-n*-latest-win64-gpl.zip` (versión estática, 64 bits).
3. Descomprime el archivo descargado.
4. Dentro de la carpeta descomprimida, ubica la carpeta `bin` (contiene `ffmpeg.exe`).
5. Agrega la ruta completa de la carpeta `bin` al **PATH** del sistema operativo Windows.
6. Abre una nueva terminal y ejecuta `ffmpeg -version` para verificar que está correctamente instalado.

Todas las opciones son válidas para este proyecto, pero se recomienda el instalador automático para mayor facilidad.

**Guía paso a paso para instalación manual (versiones comprimidas):**
Puedes consultar una guía ilustrada y detallada en español e inglés aquí:
[https://www.wikihow.com/Install-FFmpeg-on-Windows](https://www.wikihow.com/Install-FFmpeg-on-Windows)

## Instalación y uso

1. Clona este repositorio o descarga los archivos.
2. Instala las dependencias necesarias (solo Python estándar).
3. Asegúrate de tener `ffmpeg` instalado y en el PATH.
4. Ejecuta la aplicación:
   ```bash
   python main.py
   ```
5. Ingresa la URL del `videomanifest` y el nombre del archivo de salida (sin `.mp4`).
6. Haz clic en "Descargar".

## Generar ejecutable (.exe)

Para crear un ejecutable para Windows:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name TeamsDownloader main.py
```

El ejecutable estará en la carpeta `dist`.

## Estructura del proyecto

```
app/
├── __init__.py
├── ui.py
├── downloader.py
└── utils.py
main.py
README.md
TODO.md
```

## Notas

- El usuario debe obtener la URL del `videomanifest` desde las herramientas de red del navegador (ver instrucciones en `teams2mp4.md`).