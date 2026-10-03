from __future__ import annotations

import pytest
from app.main import Settings, create_app
from fastapi.testclient import TestClient


def client_for(settings: Settings | None = None) -> TestClient:
    return TestClient(create_app(settings), raise_server_exceptions=False)


def test_status_operational() -> None:
    client = client_for(Settings(version="test"))

    response = client.get("/api/v1/status")

    assert response.status_code == 200
    assert response.json() == {
        "status": "operational",
        "message": "All systems operational.",
        "inventoryBackend": "builtin",
        "version": "test",
        "recentErrors": 0,
    }


def test_products_support_paging_sort_search_and_filter() -> None:
    client = client_for()

    page = client.get(
        "/api/v1/products",
        params={"page": 1, "pageSize": 5, "sort": "price", "order": "desc"},
    )
    assert page.status_code == 200
    payload = page.json()
    assert payload["page"] == 1
    assert payload["pageSize"] == 5
    assert payload["total"] == 24
    prices = [item["price"] for item in payload["items"]]
    assert prices == sorted(prices, reverse=True)

    filtered = client.get(
        "/api/v1/products",
        params={"category": "Water Sports", "search": "dry", "sort": "name"},
    )
    assert filtered.status_code == 200
    filtered_payload = filtered.json()
    assert filtered_payload["total"] == 1
    assert filtered_payload["items"][0]["id"] == "water-drybag-trio"


def test_product_detail_for_non_climbing_product_includes_unit_price() -> None:
    client = client_for()

    response = client.get("/api/v1/products/apparel-socks-3")

    assert response.status_code == 200
    payload = response.json()
    assert payload["packSize"] == 3
    assert payload["unitPrice"] == 12.0


def test_config_fault_returns_503_outage_status_and_live_health() -> None:
    client = client_for(Settings(inventory_backend="cosmosdb-prod", version="test"))

    products = client.get("/api/v1/products")
    assert products.status_code == 503
    assert products.json()["error"] == "CONFIG_ERROR"
    assert products.json()["correlationId"]

    status_response = client.get("/api/v1/status")
    assert status_response.status_code == 200
    assert status_response.json()["status"] == "outage"

    live = client.get("/health/live")
    assert live.status_code == 200


@pytest.mark.xfail(strict=True, reason="Known defect – demo scenario 1")
def test_climbing_product_detail_returns_200() -> None:
    client = client_for()

    response = client.get("/api/v1/products/climb-cragdraw-6")

    assert response.status_code == 200
