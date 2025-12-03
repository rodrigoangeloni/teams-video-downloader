# Copilot Instructions - Teams Video Downloader

## Project Overview
Desktop application (Windows) for downloading Microsoft Teams/SharePoint/OneDrive videos via `videomanifest` URLs. Built with Python 3.11+, Tkinter GUI, and ffmpeg for video processing.

## Architecture

### Module Structure
```
main.py          → Entry point, creates AppUI instance
app/ui.py        → Tkinter GUI, i18n (es/en), user interaction
app/downloader.py → Threaded ffmpeg subprocess, progress parsing
app/utils.py     → URL sanitization, filename generation
```

### Data Flow
1. User pastes videomanifest URL → `extraer_url_videomanifest()` trims to last "true"
2. `Downloader.descargar()` spawns thread → ffprobe gets duration → ffmpeg downloads
3. Progress parsed from ffmpeg stderr (`time=HH:MM:SS`) → callback updates UI progressbar
4. Output: `descargas/{nombre}_{YYYY-MM-DD_HHMM}.mp4`

## Key Patterns

### Threading Model
Downloads run in daemon threads to keep UI responsive. The `proceso_holder` dict pattern passes subprocess reference back for cancellation:
```python
# app/downloader.py
proceso_holder["proceso"] = proceso
if return_process:
    while "proceso" not in proceso_holder:
        time.sleep(0.05)
    return proceso_holder["proceso"]
```

### Internationalization
All UI strings in `self.idiomas` dict with `es`/`en` keys in `app/ui.py`. When adding text:
```python
self.idiomas = {
    "es": { "new_key": "Texto en español" },
    "en": { "new_key": "English text" }
}
```

### URL Processing
URLs must be trimmed to last `true` parameter for ffmpeg compatibility:
```python
# app/utils.py - extraer_url_videomanifest()
idx = url_limpia.rfind("true")
if idx != -1:
    return url_limpia[:idx + len("true")]
```

## Development Commands

### Setup
```powershell
python -m venv venv
venv\Scripts\activate
pip install pyperclip
```

### Run Application
```powershell
python main.py
```

### Build Executable
```powershell
python build_exe.py  # Interactive, prompts for version
# Or direct:
pyinstaller --onefile --windowed --icon=ico/favicon.ico --version-file=version.txt --name TeamsDownloader-v1.0 main.py
```

## External Dependencies

- **ffmpeg/ffprobe**: Must be in system PATH. Check with `shutil.which("ffmpeg")`
- **pyperclip**: Optional, for clipboard auto-paste (gracefully handles ImportError)

## Conventions

- **Logging**: Use `log_event()` from `app/downloader.py` → writes to `app.log`
- **File naming**: `{user_input}_{YYYY-MM-DD_HHMM}.mp4` via `generar_nombre_archivo()`
- **Error handling**: Show user-friendly messages via `messagebox`, log technical details to `app.log`
- **Version**: Update `__version__` in `main.py` and `version.txt` when releasing

## UI Guidelines

- Green neon progressbar (`#39FF14`) styled via ttk
- Entry placeholders clear on focus, restore on blur if empty
- All buttons enable/disable based on download state
- Window icon from `ico/favicon.ico`
