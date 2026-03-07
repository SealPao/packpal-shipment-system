# Server API

FastAPI skeleton intended for NAS-side deployment.

## Structure

- `app/main.py`: FastAPI app factory and startup
- `app/core/config.py`: environment-driven settings
- `app/api/routes_health.py`: health endpoint
- `app/db`: placeholders for models and session wiring

## Run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:PYTHONPATH = "."
uvicorn app.main:app --reload
```

## Available Endpoints

- `GET /`
- `GET /health`
