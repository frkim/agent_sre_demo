"""Telemetry and structured logging setup for Contoso Trek."""

from __future__ import annotations

import contextvars
import json
import logging
import os
import sys
from datetime import UTC, datetime
from typing import Any

_correlation_id: contextvars.ContextVar[str] = contextvars.ContextVar(
    "correlation_id", default="-"
)
_configured = False


def set_correlation_id(correlation_id: str) -> contextvars.Token[str]:
    """Attach a correlation id to logs emitted during the current request."""
    return _correlation_id.set(correlation_id)


def reset_correlation_id(token: contextvars.Token[str]) -> None:
    """Restore the previous request correlation id."""
    _correlation_id.reset(token)


def get_correlation_id() -> str:
    """Return the active request correlation id."""
    return _correlation_id.get()


class JsonFormatter(logging.Formatter):
    """Small JSON formatter that keeps application logs query-friendly."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created, UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "correlationId": get_correlation_id(),
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, separators=(",", ":"))


def configure_logging() -> None:
    """Configure structured console logging without including secret-bearing values."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


def configure_azure_monitor_if_configured() -> None:
    """Enable Azure Monitor OpenTelemetry export when Application Insights is configured."""
    global _configured
    if _configured:
        return
    if os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"):
        from azure.monitor.opentelemetry import configure_azure_monitor

        configure_azure_monitor()
    _configured = True
