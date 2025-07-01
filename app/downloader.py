import subprocess
import threading
import datetime

def log_event(mensaje):
    with open("app.log", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now()}] {mensaje}\n")

import re
import time

class Downloader:
    @staticmethod
    def _check_ffmpeg():
        import shutil
        return shutil.which("ffmpeg") is not None and shutil.which("ffprobe") is not None

    def descargar(self, url, nombre_archivo, callback, progress_callback=None, return_process=False):
        proceso_holder = {}

        def run():
            try:
                # Verificar ffmpeg y ffprobe
                if not self._check_ffmpeg():
                    callback(False, "No se encontró ffmpeg o ffprobe en el PATH del sistema. Instala ffmpeg y reinicia la aplicación.")
                    return

                # Obtener duración total con ffprobe
                duracion = None
                try:
                    probe_cmd = [
                        "ffprobe", "-v", "error", "-show_entries",
                        "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", url
                    ]
                    probe = subprocess.run(probe_cmd, capture_output=True, text=True, timeout=15)
                    if probe.returncode != 0:
                        log_event(f"ffprobe error: {probe.stderr}")
                        callback(False, "No se pudo obtener la duración del video. Verifica la URL o tu conexión.")
                        return
                    duracion = float(probe.stdout.strip())
                    log_event(f"Duración detectada: {duracion} segundos")
                except Exception as e:
                    log_event(f"No se pudo obtener duración: {e}")
                    callback(False, "No se pudo obtener la duración del video. Verifica la URL o tu conexión.")
                    return

                comando = ["ffmpeg", "-i", f'{url}', "-codec", "copy", nombre_archivo, "-y"]
                log_event(f"Intentando descarga: {' '.join(comando)}")
                try:
                    proceso = subprocess.Popen(
                        comando,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        universal_newlines=True,
                        bufsize=1
                    )
                except FileNotFoundError:
                    callback(False, "No se encontró ffmpeg en el PATH del sistema. Instala ffmpeg y reinicia la aplicación.")
                    return

                proceso_holder["proceso"] = proceso

                tiempo_actual = 0
                patron_time = re.compile(r"time=(\d+):(\d+):(\d+).(\d+)")

                errores = []
                if proceso.stderr:
                    for linea in proceso.stderr:
                        log_event(linea.strip())
                        errores.append(linea)
                        match = patron_time.search(linea)
                        if match and duracion and progress_callback:
                            h, m, s, ms = map(int, match.groups())
                            tiempo_actual = h * 3600 + m * 60 + s + ms / 100
                            progreso = min(100, int((tiempo_actual / duracion) * 100))
                            progress_callback(progreso)
                proceso.wait()
                error_str = "".join(errores)
                if proceso.returncode == 0:
                    log_event(f"Descarga exitosa: {nombre_archivo}")
                    if progress_callback:
                        progress_callback(100)
                    callback(True, "")
                else:
                    log_event(f"Error en descarga: {error_str}")
                    callback(False, "Error en la descarga. Revisa app.log para más detalles.")
            except Exception as e:
                log_event(f"Excepción: {str(e)}")
                callback(False, f"Ocurrió un error inesperado: {str(e)}")

        @staticmethod
        def _check_ffmpeg():
            import shutil
            return shutil.which("ffmpeg") is not None and shutil.which("ffprobe") is not None

        hilo = threading.Thread(target=run, daemon=True)
        hilo.start()
        if return_process:
            # Esperar a que el proceso esté disponible
            while "proceso" not in proceso_holder:
                time.sleep(0.05)
            return proceso_holder["proceso"]
        return None