import os
import sys
import subprocess
import shutil

def check_python_version():
    """Verifica que Python sea 3.10 o superior"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print(f"❌ Error: Se requiere Python 3.10 o superior. Versión actual: {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detectado")
    return True

def create_venv():
    """Crea el entorno virtual si no existe"""
    venv_path = "venv"
    if os.path.exists(venv_path):
        print("✅ Entorno virtual ya existe")
        return True
    
    print("📦 Creando entorno virtual...")
    try:
        subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
        print("✅ Entorno virtual creado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al crear entorno virtual: {e}")
        return False

def get_pip_path():
    """Obtiene la ruta del pip del entorno virtual"""
    if sys.platform == "win32":
        return os.path.join("venv", "Scripts", "pip.exe")
    return os.path.join("venv", "bin", "pip")

def get_python_path():
    """Obtiene la ruta del python del entorno virtual"""
    if sys.platform == "win32":
        return os.path.join("venv", "Scripts", "python.exe")
    return os.path.join("venv", "bin", "python")

def install_dependencies():
    """Instala las dependencias necesarias"""
    pip_path = get_pip_path()
    
    dependencies = ["pyinstaller", "pillow", "pyperclip"]
    
    print("📦 Instalando dependencias...")
    for dep in dependencies:
        print(f"   Instalando {dep}...")
        try:
            subprocess.run([pip_path, "install", dep, "-q"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Error al instalar {dep}: {e}")
            return False
    
    print("✅ Dependencias instaladas")
    return True

def update_version_files(version):
    """Actualiza la versión en main.py y version.txt"""
    # Actualizar main.py
    main_script = "main.py"
    try:
        with open(main_script, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Actualizar __version__
        import re
        content = re.sub(r'__version__\s*=\s*"[^"]+"', f'__version__ = "{version}"', content)
        
        # Actualizar docstring
        content = re.sub(r'Teams Video Downloader v[\d.]+', f'Teams Video Downloader v{version}', content)
        
        with open(main_script, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ main.py actualizado a v{version}")
    except Exception as e:
        print(f"⚠️ Advertencia: No se pudo actualizar main.py: {e}")
    
    # Actualizar version.txt
    version_file = "version.txt"
    try:
        parts = version.split(".")
        major = parts[0] if len(parts) > 0 else "1"
        minor = parts[1] if len(parts) > 1 else "0"
        patch = parts[2] if len(parts) > 2 else "0"
        
        version_content = f'''# version.txt
# UTF-8
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({major}, {minor}, {patch}, 0),
    prodvers=({major}, {minor}, {patch}, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        '040904B0',
        [StringStruct('CompanyName', 'RoanDev'),
        StringStruct('FileDescription', 'Teams Video Downloader'),
        StringStruct('FileVersion', '{major}.{minor}.{patch}.0'),
        StringStruct('InternalName', 'TeamsDownloader'),
        StringStruct('LegalCopyright', 'Copyright (c) RoanDev 2025'),
        StringStruct('OriginalFilename', 'TeamsDownloader-v{version}.exe'),
        StringStruct('ProductName', 'Teams Video Downloader'),
        StringStruct('ProductVersion', '{major}.{minor}.{patch}.0')])
      ]), 
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)
'''
        with open(version_file, "w", encoding="utf-8") as f:
            f.write(version_content)
        print(f"✅ version.txt actualizado a v{version}")
    except Exception as e:
        print(f"⚠️ Advertencia: No se pudo actualizar version.txt: {e}")

def build_executable(version):
    """Compila el ejecutable con PyInstaller"""
    python_path = get_python_path()
    exe_name = f"TeamsDownloader-v{version}"
    icon_path = "ico/favicon.ico"
    main_script = "main.py"
    
    # Verificar que el icono existe
    if not os.path.exists(icon_path):
        print(f"⚠️ Advertencia: No se encontró el icono en {icon_path}")
        icon_arg = ""
    else:
        icon_arg = f"--icon={icon_path}"
    
    # Limpiar builds anteriores
    for folder in ["build", "dist", "__pycache__"]:
        if os.path.exists(folder):
            shutil.rmtree(folder, ignore_errors=True)
    
    # Eliminar .spec anterior si existe
    spec_file = f"{exe_name}.spec"
    if os.path.exists(spec_file):
        os.remove(spec_file)
    
    print(f"🔨 Compilando {exe_name}.exe...")
    
    cmd = [
        python_path, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--clean",
        "--noconfirm",
        f"--name={exe_name}",
        "--version-file=version.txt"
    ]
    
    if icon_arg:
        cmd.append(icon_arg)
    
    # Agregar datos adicionales (icono para la UI)
    cmd.append(f"--add-data=ico;ico")
    
    cmd.append(main_script)
    
    try:
        subprocess.run(cmd, check=True)
        print(f"\n✅ ¡Compilación exitosa!")
        print(f"📁 Ejecutable: dist/{exe_name}.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en la compilación: {e}")
        return False

def main():
    print("=" * 50)
    print("  Teams Video Downloader - Generador de Ejecutable")
    print("=" * 50)
    print()
    
    # 1. Verificar versión de Python
    if not check_python_version():
        sys.exit(1)
    
    # 2. Solicitar versión
    version = input("\n📝 Ingrese la versión (ej: 1.2): ").strip()
    if not version:
        print("❌ Versión no válida.")
        sys.exit(1)
    
    print()
    
    # 3. Crear entorno virtual
    if not create_venv():
        sys.exit(1)
    
    # 4. Instalar dependencias
    if not install_dependencies():
        sys.exit(1)
    
    # 5. Actualizar archivos de versión
    update_version_files(version)
    
    # 6. Compilar
    print()
    if build_executable(version):
        print()
        print("=" * 50)
        print(f"  ¡Listo! Ejecutable generado correctamente")
        print(f"  Ubicación: dist/TeamsDownloader-v{version}.exe")
        print("=" * 50)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()