# Server API

FastAPI skeleton intended for NAS-side deployment.

## Structure

- `app/main.py`: FastAPI app factory and startup
- `app/core/config.py`: environment-driven settings
- `app/api/routes_health.py`: health endpoint
- `app/db`: placeholders for models and session wiring
- `tests`: API smoke tests

## Run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:PYTHONPATH = "."
uvicorn app.main:app --reload
```

## Test

```powershell
pip install -r requirements.txt
$env:PYTHONPATH = "."
python -m pytest tests -q
```

## Available Endpoints

- `GET /`
- `GET /health`