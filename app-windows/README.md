# Windows Workstation App

Desktop skeleton for the PackPal workstation client.

## Structure

- `src/main.py`: application entry point
- `src/app`: app-level configuration and version
- `src/ui`: desktop windows and shared widgets
- `src/services`: future integrations and workflows
- `src/db`: local SQLite-related modules
- `src/utils`: shared helpers

## Run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:PYTHONPATH = "src"
python src/main.py
```

## Current Scope

Included:
- Login window
- Mode selection window
- Shared footer with version display

Deferred:
- Camera recording
- OpenCV workflow
- Local database logic
- Background upload queue
