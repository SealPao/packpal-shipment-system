# PackPal Shipment System

PackPal Shipment System (出貨小幫手) is organized as a small monorepo with three primary components:

- `app-windows`: Windows workstation app for front-line operation flow
- `server-api`: FastAPI backend intended for NAS deployment
- `web-admin`: Web admin interface for search and management
- `docs`: Product and flow documentation
- `infra`: Infrastructure notes and deployment placeholders

## Recommended Structure

```text
packpal-shipment-system
|-- app-windows
|   |-- src
|   |   |-- app
|   |   |-- db
|   |   |-- services
|   |   |-- ui
|   |   `-- utils
|   |-- tests
|   `-- requirements.txt
|-- docs
|-- infra
|-- server-api
|   |-- app
|   |   |-- api
|   |   |-- core
|   |   `-- db
|   |-- tests
|   `-- requirements.txt
|-- web-admin
|   |-- app
|   |   `-- records
|   |-- tests
|   |-- package.json
|   `-- tsconfig.json
|-- CHANGELOG.md
`-- .gitignore
```

## Current Scope

This repository currently provides a maintainable starting skeleton only.

Implemented in `v0.1.0`:
- Windows login window and mode selection window
- FastAPI application startup with `/health`
- Next.js admin shell with dashboard and records placeholder
- Minimal smoke tests for all three components

Not implemented yet:
- Camera capture and OpenCV workflows
- Business logic for shipment, repair, or return intake
- Database schema and persistence
- Real API integration between components

## Local Development

### 1. Windows App

```powershell
cd app-windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:PYTHONPATH = "src"
python src/main.py
```

### 2. Server API

```powershell
cd server-api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:PYTHONPATH = "."
uvicorn app.main:app --reload
```

Open [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health).

### 3. Web Admin

```powershell
cd web-admin
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Tests

### Windows App

```powershell
cd app-windows
pip install -r requirements.txt
$env:PYTHONPATH = "src"
$env:QT_QPA_PLATFORM = "offscreen"
python -m pytest tests -q
```

### Server API

```powershell
cd server-api
pip install -r requirements.txt
$env:PYTHONPATH = "."
python -m pytest tests -q
```

### Web Admin

```powershell
cd web-admin
npm install
npm test
```

## Reference Docs

- [System Spec](docs/system-spec.md)
- [UI Flow](docs/ui-flow.md)