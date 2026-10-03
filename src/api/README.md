# Contoso Trek API

FastAPI catalog service for the Azure SRE Agent demo.

## Run locally

```powershell
cd src\api
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt -r requirements-dev.txt
$env:APP_VERSION = "local"
.\.venv\Scripts\python -m uvicorn app.main:app --host 127.0.0.1 --port 8080
```

## Test and lint

```powershell
.\.venv\Scripts\python -m ruff check .
.\.venv\Scripts\python -m pytest -q
```

## Environment variables

- `APPLICATIONINSIGHTS_CONNECTION_STRING`: enables Azure Monitor OpenTelemetry export when set.
- `OTEL_SERVICE_NAME`: service name supplied by Container Apps infrastructure.
- `INVENTORY_BACKEND`: catalog provider; only `builtin` is supported. Other values return catalog `503` responses while `/health/live` remains `200`.
- `APP_VERSION`: version string returned by `/api/v1/status`.

The service listens on port `8080`.
