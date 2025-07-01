import os
import sys

def main():
    print("=== Generador de ejecutable Teams Video Downloader ===")
    version = input("Ingrese la versión para el ejecutable (ej: 1.0): ").strip()
    if not version:
        print("Versión no válida.")
        sys.exit(1)

    exe_name = f"TeamsDownloader-v{version}"
    icon_path = "ico/favicon.ico"
    main_script = "main.py"

    # Actualiza la versión en main.py (opcional, si se desea)
    try:
        with open(main_script, "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open(main_script, "w", encoding="utf-8") as f:
            for line in lines:
                if line.startswith("__version__"):
                    f.write(f'__version__ = "{version}"\n')
                else:
                    f.write(line)
    except Exception as e:
        print(f"Advertencia: No se pudo actualizar la versión en main.py: {e}")

    cmd = f'venv\\Scripts\\activate && pyinstaller --onefile --windowed --icon={icon_path} --version-file=version.txt --name {exe_name} {main_script}'
    print(f"Ejecutando: {cmd}")
    os.system(cmd)
    print(f"\n¡Listo! El ejecutable se encuentra en dist/{exe_name}.exe")

if __name__ == "__main__":
    main()