import tkinter as tk
from tkinter import messagebox, ttk
from app.downloader import Downloader
from app.utils import generar_nombre_archivo, extraer_url_videomanifest

import threading

class AppUI:
    def __init__(self):
        import re
        # Intentar importar pyperclip para portapapeles global
        try:
            global pyperclip
            import pyperclip
        except ImportError:
            pyperclip = None
        self.idiomas = {
            "es": {
                "title": "Descargador de videos de Teams",
                "desc": "1. Copia la URL del 'videomanifest' desde el inspector de red de tu navegador.\n2. Pega la URL en el campo resaltado en rojo.\n3. Ingresa el nombre del archivo (sin .mp4).\n4. Haz clic en 'Descargar'. Puedes detener la descarga en cualquier momento.\n5. Al finalizar, puedes abrir la carpeta de descargas directamente.",
                "url_placeholder": "URL del videomanifest...",
                "name_placeholder": "Nombre del archivo (sin .mp4)...",
                "dest_folder": "Carpeta de destino:",
                "select_folder": "Seleccionar...",
                "download": "Descargar",
                "stop": "Detener descarga",
                "open_folder": "Abrir carpeta de descargas",
                "ready": "Listo",
                "downloading": "Descargando...",
                "completed": "Descarga completada:",
                "error": "Error en la descarga",
                "success": "Éxito",
                "file_saved": "Video guardado como:\n{}",
                "error_url": "Por favor, ingresa la URL del videomanifest.",
                "error_stop": "No se pudo detener la descarga: {}",
                "stopped": "Descarga detenida por el usuario."
            },
            "en": {
                "title": "Teams Video Downloader",
                "desc": "1. Copy the 'videomanifest' URL from your browser's network inspector.\n2. Paste the URL in the red highlighted field.\n3. Enter the file name (without .mp4).\n4. Click 'Download'. You can stop the download at any time.\n5. When finished, you can open the downloads folder directly.",
                "url_placeholder": "Paste videomanifest URL...",
                "name_placeholder": "File name (without .mp4)...",
                "dest_folder": "Destination folder:",
                "select_folder": "Select...",
                "download": "Download",
                "stop": "Stop download",
                "open_folder": "Open downloads folder",
                "ready": "Ready",
                "downloading": "Downloading...",
                "completed": "Download completed:",
                "error": "Download error",
                "success": "Success",
                "file_saved": "Video saved as:\n{}",
                "error_url": "Please enter the videomanifest URL.",
                "error_stop": "Could not stop download: {}",
                "stopped": "Download stopped by user."
            }
        }
        self.lang = "es"

        self.root = tk.Tk()
        self.root.title(self.idiomas[self.lang]["title"])
        self.root.geometry("510x540")
        self.root.resizable(True, True)
        self.root.configure(bg="#f4f6fb")

        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TFrame", background="#f4f6fb")
        style.configure("TLabel", background="#f4f6fb", font=("Segoe UI", 11))
        style.configure("TButton", font=("Segoe UI", 11, "bold"), foreground="#fff", background="#0078d7")
        style.map("TButton", background=[("active", "#005fa3")])
        style.configure("TEntry", font=("Segoe UI", 11))
        style.layout("green.Horizontal.TProgressbar",
            [('Horizontal.Progressbar.trough',
              {'children': [('Horizontal.Progressbar.pbar',
                             {'side': 'left', 'sticky': 'ns'})],
               'sticky': 'nswe'}),
             ('Horizontal.Progressbar.label', {'sticky': ''})])
        style.configure("green.Horizontal.TProgressbar", troughcolor="#e0e0e0", bordercolor="#e0e0e0",
                        background="#39FF14", lightcolor="#39FF14", darkcolor="#39FF14")

        frame = ttk.Frame(self.root, padding=24, style="TFrame")
        frame.pack(expand=True, fill="both")

        # Selector de idioma
        idioma_frame = ttk.Frame(frame)
        idioma_frame.pack(fill="x", pady=(0, 6))
        ttk.Label(idioma_frame, text="Idioma / Language:", font=("Segoe UI", 10)).pack(side="left")
        self.combo_idioma = ttk.Combobox(idioma_frame, values=["Español", "English"], width=10, state="readonly")
        self.combo_idioma.current(0)
        self.combo_idioma.pack(side="left", padx=(6, 0))
        self.combo_idioma.bind("<<ComboboxSelected>>", self.cambiar_idioma)

        self.label_title = ttk.Label(frame, text=self.idiomas[self.lang]["title"], font=("Segoe UI", 16, "bold"), foreground="#0078d7")
        self.label_title.pack(pady=(0, 8))

        self.label_desc = ttk.Label(frame, text=self.idiomas[self.lang]["desc"], font=("Segoe UI", 10), foreground="#444", wraplength=460, justify="left")
        self.label_desc.pack(pady=(0, 10))

        # Campo URL resaltado en rojo
        self.entry_url = ttk.Entry(frame, width=60, font=("Segoe UI", 11))
        self.entry_url.pack(fill="x", pady=(0, 8))
        self.entry_url.insert(0, "")
        self.entry_url.bind("<FocusIn>", lambda e: self._placeholder(self.entry_url, self.idiomas[self.lang]["url_placeholder"], True))
        self.entry_url.bind("<FocusOut>", lambda e: self._placeholder(self.entry_url, self.idiomas[self.lang]["url_placeholder"], False))
        self._placeholder(self.entry_url, self.idiomas[self.lang]["url_placeholder"], False)
        self.entry_url.config(foreground="#00FF37")

        self.entry_nombre = ttk.Entry(frame, width=40, font=("Segoe UI", 11))
        self.entry_nombre.pack(fill="x", pady=(0, 8))
        self.entry_nombre.insert(0, "")
        self.entry_nombre.bind("<FocusIn>", lambda e: self._placeholder(self.entry_nombre, self.idiomas[self.lang]["name_placeholder"], True))
        self.entry_nombre.bind("<FocusOut>", lambda e: self._placeholder(self.entry_nombre, self.idiomas[self.lang]["name_placeholder"], False))
        self._placeholder(self.entry_nombre, self.idiomas[self.lang]["name_placeholder"], False)

        self.carpeta_destino = tk.StringVar(value="descargas")
        carpeta_frame = ttk.Frame(frame)
        carpeta_frame.pack(fill="x", pady=(0, 8))
        ttk.Label(carpeta_frame, text=self.idiomas[self.lang]["dest_folder"], font=("Segoe UI", 10)).pack(side="left")
        self.entry_carpeta = ttk.Entry(carpeta_frame, textvariable=self.carpeta_destino, width=28, font=("Segoe UI", 10))
        self.entry_carpeta.pack(side="left", padx=(6, 0))
        ttk.Button(carpeta_frame, text=self.idiomas[self.lang]["select_folder"], command=self.seleccionar_carpeta, style="TButton").pack(side="left", padx=(6, 0))

        self.btn_descargar = ttk.Button(frame, text=self.idiomas[self.lang]["download"], command=self.descargar_video, style="TButton")
        self.btn_descargar.pack(pady=(8, 4), fill="x")

        self.btn_detener = ttk.Button(frame, text=self.idiomas[self.lang]["stop"], command=self.detener_descarga, style="TButton")
        self.btn_detener.pack(pady=(0, 8), fill="x")
        self.btn_detener.config(state=tk.DISABLED)

        self.btn_abrir = ttk.Button(frame, text=self.idiomas[self.lang]["open_folder"], command=self.abrir_descargas, style="TButton")
        self.btn_abrir.pack(pady=(0, 8), fill="x")
        self.btn_abrir.config(state=tk.DISABLED)

        self.progress = ttk.Progressbar(frame, mode="determinate", maximum=100, style="green.Horizontal.TProgressbar")
        self.progress.pack(fill="x", pady=(0, 10))
        self.progress["value"] = 0

        self.label_estado = ttk.Label(frame, text=self.idiomas[self.lang]["ready"], foreground="#0078d7", font=("Segoe UI", 10, "italic"))
        self.label_estado.pack(anchor="w", pady=(4, 0))

    def cambiar_idioma(self, event):
        idx = self.combo_idioma.current()
        self.lang = "es" if idx == 0 else "en"
        self.label_title.config(text=self.idiomas[self.lang]["title"])
        self.label_desc.config(text=self.idiomas[self.lang]["desc"])
        self._placeholder(self.entry_url, self.idiomas[self.lang]["url_placeholder"], False)
        self._placeholder(self.entry_nombre, self.idiomas[self.lang]["name_placeholder"], False)
        self.btn_descargar.config(text=self.idiomas[self.lang]["download"])
        self.btn_detener.config(text=self.idiomas[self.lang]["stop"])
        self.btn_abrir.config(text=self.idiomas[self.lang]["open_folder"])
        self.label_estado.config(text=self.idiomas[self.lang]["ready"])
        # Actualizar label y botón de carpeta
        for widget in self.entry_carpeta.master.winfo_children():
            if isinstance(widget, ttk.Label):
                widget.config(text=self.idiomas[self.lang]["dest_folder"])
            if isinstance(widget, ttk.Button):
                widget.config(text=self.idiomas[self.lang]["select_folder"])

    def seleccionar_carpeta(self):
        from tkinter import filedialog
        carpeta = filedialog.askdirectory(initialdir=".", title="Selecciona la carpeta de destino")
        if carpeta:
            self.carpeta_destino.set(carpeta)

    def _placeholder(self, entry, text, clear):
        if clear:
            if entry.get() == text:
                entry.delete(0, tk.END)
                entry.config(foreground="#222")
        else:
            if not entry.get():
                entry.insert(0, text)
                entry.config(foreground="#888")

    def descargar_video(self):
        url = self.entry_url.get().strip()
        nombre = self.entry_nombre.get().strip()
        if not url or url == self.idiomas[self.lang]["url_placeholder"]:
            messagebox.showerror(self.idiomas[self.lang]["error"], self.idiomas[self.lang]["error_url"])
            return
        if not nombre or nombre == self.idiomas[self.lang]["name_placeholder"]:
            nombre = "teamsvideo"
        url_limpia = extraer_url_videomanifest(url)
        nombre_archivo = generar_nombre_archivo(nombre)
        self.label_estado.config(text=self.idiomas[self.lang]["downloading"], foreground="#0078d7")
        self.btn_descargar.config(state=tk.DISABLED)
        self.btn_detener.config(state=tk.NORMAL)
        self.btn_abrir.config(state=tk.DISABLED)
        self.progress["mode"] = "determinate"
        self.progress["value"] = 0

        self._descarga_en_curso = True
        self._proceso_descarga = None

        def on_finish(exito, mensaje):
            self.btn_detener.config(state=tk.DISABLED)
            if exito:
                self.progress["value"] = 100
                self.label_estado.config(text=f"{self.idiomas[self.lang]['completed']} {nombre_archivo}", foreground="#228B22")
                self.btn_abrir.config(state=tk.NORMAL)
                messagebox.showinfo(self.idiomas[self.lang]["success"], self.idiomas[self.lang]["file_saved"].format(nombre_archivo))
            else:
                self.progress["value"] = 0
                self.label_estado.config(text=self.idiomas[self.lang]["error"], foreground="#B22222")
                messagebox.showerror(self.idiomas[self.lang]["error"], mensaje)
            self.btn_descargar.config(state=tk.NORMAL)
            self._descarga_en_curso = False

        def on_progress(porcentaje):
            self.progress["mode"] = "determinate"
            self.progress["value"] = porcentaje
            self.label_estado.config(text=f"{self.idiomas[self.lang]['downloading']} {porcentaje}%", foreground="#0078d7")
            self.root.update_idletasks()

        # Modificación: guardar el proceso para poder detenerlo
        def descargar_con_proceso():
            self._proceso_descarga = Downloader().descargar(
                url_limpia, nombre_archivo, on_finish, progress_callback=on_progress
            )
        threading.Thread(target=descargar_con_proceso, daemon=True).start()

    def detener_descarga(self):
        if hasattr(self, "_proceso_descarga") and self._proceso_descarga:
            try:
                self._proceso_descarga.terminate()
                self.label_estado.config(text=self.idiomas[self.lang]["stopped"], foreground="#B22222")
                self.btn_descargar.config(state=tk.NORMAL)
                self.btn_detener.config(state=tk.DISABLED)
            except Exception as e:
                messagebox.showerror(self.idiomas[self.lang]["error"], self.idiomas[self.lang]["error_stop"].format(e))

    def abrir_descargas(self):
        import os
        import platform
        carpeta = os.path.abspath("descargas")
        if platform.system() == "Windows":
            os.startfile(carpeta)
        elif platform.system() == "Darwin":
            os.system(f"open '{carpeta}'")
        else:
            os.system(f"xdg-open '{carpeta}'")

    def run(self):
        self.root.mainloop()