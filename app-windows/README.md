# Windows Workstation App

Desktop skeleton for the PackPal workstation client.

## Structure

- `src/main.py`: application entry point
- `src/app`: app-level configuration and version
- `src/ui`: desktop windows and shared widgets
- `src/services`: camera selection and local draft persistence helpers
- `src/db`: local SQLite-related modules
- `src/utils`: shared helpers
- `tests`: minimal UI smoke tests
- `build.ps1`: PyInstaller build entry point

## Run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:PYTHONPATH = "src"
python src/main.py
```

What you can try now:
- Login screen
- Camera selection before entering workflow pages
- Shipment / Repair / Return workflow pages
- Save draft / load latest draft using local SQLite storage

## Test

```powershell
pip install -r requirements.txt
$env:PYTHONPATH = "src"
$env:QT_QPA_PLATFORM = "offscreen"
python -m pytest tests -q
```

## Build EXE

```powershell
.\build.ps1
```

Expected output:
- `dist\packpal-windows.exe`

## Current Scope

Included:
- Login window
- Mode selection window
- Camera device selection
- Three workflow shells
- Local draft persistence with SQLite
- Shared footer with version display

Deferred:
- Camera recording
- OpenCV capture workflow
- Real business validation rules
- Background upload queue