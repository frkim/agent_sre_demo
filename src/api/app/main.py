"""FastAPI application entry point for the Contoso Trek catalog API."""

from __future__ import annotations

import logging
import os
import uuid
from collections.abc import Callable
from dataclasses import dataclass
from typing import Annotated

from app.telemetry import configure_azure_monitor_if_configured, configure_logging

configure_azure_monitor_if_configured()
configure_logging()

from fastapi import FastAPI, Query, Request, Response, status  # noqa: E402
from fastapi.responses import JSONResponse  # noqa: E402

from app.catalog import (  # noqa: E402
    ProductDetail,
    ProductPage,
    SortField,
    SortOrder,
    build_detail,
    get_product,
    list_categories,
    query_products,
)
from app.status import ErrorWindow  # noqa: E402
from app.telemetry import get_correlation_id, reset_correlation_id, set_correlation_id  # noqa: E402

SUPPORTED_BACKEND = "builtin"
logger = logging.getLogger("contoso_trek.api")


@dataclass(frozen=True)
class Settings:
    """Startup settings read from environment once per container revision."""

    inventory_backend: str = SUPPORTED_BACKEND
    version: str = "local"

    @classmethod
    def from_env(cls) -> Settings:
        return cls(
            inventory_backend=os.getenv("INVENTORY_BACKEND", SUPPORTED_BACKEND),
            version=os.getenv("APP_VERSION", "local"),
        )

    @property
    def inventory_available(self) -> bool:
        return self.inventory_backend == SUPPORTED_BACKEND


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create the configured FastAPI app."""
    app_settings = settings or Settings.from_env()
    error_window = ErrorWindow()
    app = FastAPI(title="Contoso Trek API", version=app_settings.version)
    app.state.settings = app_settings
    app.state.error_window = error_window

    @app.middleware("http")
    async def correlate_and_count_errors(
        request: Request, call_next: Callable[[Request], object]
    ) -> Response:
        correlation_id = request.headers.get("x-correlation-id") or str(uuid.uuid4())
        token = set_correlation_id(correlation_id)
        try:
            response = await call_next(request)
            if response.status_code >= 500:
                error_window.record()
            response.headers["x-correlation-id"] = correlation_id
            return response
        except Exception:
            error_window.record()
            raise
        finally:
            reset_correlation_id(token)

    def config_error_response() -> JSONResponse:
        logger.error(
            "CONFIG_ERROR: INVENTORY_BACKEND=%r is unsupported; expected %r",
            app_settings.inventory_backend,
            SUPPORTED_BACKEND,
        )
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"error": "CONFIG_ERROR", "correlationId": get_correlation_id()},
        )

    @app.get("/health/live")
    async def live() -> dict[str, str]:
        """Liveness probe; remains healthy for recoverable config faults."""
        return {"status": "live"}

    @app.get("/health/ready")
    async def ready():
        """Readiness probe reflecting inventory backend availability."""
        if not app_settings.inventory_available:
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={"status": "unready", "inventoryBackend": app_settings.inventory_backend},
            )
        return {"status": "ready", "inventoryBackend": app_settings.inventory_backend}

    @app.get("/api/v1/status")
    async def api_status() -> dict[str, str | int]:
        """Return storefront health for the status banner."""
        recent_errors = error_window.recent_count()
        if not app_settings.inventory_available:
            status_value = "outage"
            message = "Inventory backend is misconfigured. Catalog traffic is unavailable."
        elif recent_errors:
            status_value = "degraded"
            message = "Recent product detail failures detected. Some pages may be unavailable."
        else:
            status_value = "operational"
            message = "All systems operational."
        return {
            "status": status_value,
            "message": message,
            "inventoryBackend": app_settings.inventory_backend,
            "version": app_settings.version,
            "recentErrors": recent_errors,
        }

    @app.get("/api/v1/categories", response_model=list[str])
    async def categories():
        """Return available product categories."""
        if not app_settings.inventory_available:
            return config_error_response()
        return list_categories()

    @app.get("/api/v1/products", response_model=ProductPage)
    async def products(
        search: str | None = None,
        category: str | None = None,
        sort: SortField = "name",
        order: SortOrder = "asc",
        page: Annotated[int, Query(ge=1)] = 1,
        page_size: Annotated[int, Query(alias="pageSize", ge=1, le=50)] = 10,
    ):
        """Search, filter, sort, and page catalog products."""
        if not app_settings.inventory_available:
            return config_error_response()
        return query_products(
            search=search,
            category=category,
            sort=sort,
            order=order,
            page=page,
            page_size=page_size,
        )

    @app.get("/api/v1/products/{product_id}", response_model=ProductDetail)
    async def product_detail(product_id: str):
        """Return a product detail record including unit price."""
        if not app_settings.inventory_available:
            return config_error_response()
        product = get_product(product_id)
        if product is None:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"error": "NOT_FOUND"})
        return build_detail(product)

    return app


app = create_app()
