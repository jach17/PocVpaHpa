from http import HTTPStatus
from unittest.mock import AsyncMock, patch

import pytest
from expects import expect, equal
from fastapi.testclient import TestClient

from app.infrastructure.api.main import app
from app.infrastructure.api.routers import Transaction_repository_router
from app.infrastructure.api.schemas.Transaction_schema import TransactionResponse

app.include_router(Transaction_repository_router.router)
Users = TestClient(app)

router_path = "app.infrastructure.api.routers.Transaction_repository_router"


@pytest.fixture
def mock_get_all_Transactions_case():
    with patch(
        f"{router_path}.get_all_Transactions_case",
        new_callable=AsyncMock,
    ) as mock:
        yield mock


@pytest.fixture
def mock_create_Transaction_case():
    with patch(
        f"{router_path}.create_Transaction_case",
        new_callable=AsyncMock,
    ) as mock:
        yield mock


@pytest.fixture
def mock_update_Transaction_case():
    with patch(
        f"{router_path}.update_Transaction_case",
        new_callable=AsyncMock,
    ) as mock:
        yield mock


def test_list_Transactions_success(mock_get_all_Transactions_case):
    mock_get_all_Transactions_case.return_value = [
        {"id": 1, "nombre": "Alice", "telefono": "123456"},
        {"id": 2, "nombre": "Bob", "telefono": "654321"},
    ]

    response = Users.get("/api/v1/repo/repository/")

    expect(response.status_code).to(equal(HTTPStatus.OK))
    expect(response.json()).to(equal(mock_get_all_Transactions_case.return_value))


def test_create_Transaction_success(mock_create_Transaction_case):
    mock_create_Transaction_case.return_value = {
        "id": 3, "nombre": "Charlie", "telefono": "111222"
    }

    payload = {"nombre": "Charlie", "telefono": "111222"}

    response = Users.post("/api/v1/repo/repository/", json=payload)

    expect(response.status_code).to(equal(HTTPStatus.OK))
    expect(response.json()).to(equal(mock_create_Transaction_case.return_value))


def test_update_Transaction_success(mock_update_Transaction_case):
    mock_update_Transaction_case.return_value = {
        "id": 4, "nombre": "Updated", "telefono": "999000"
    }

    payload = {"nombre": "Updated", "telefono": "999000"}

    response = Users.put("/api/v1/repo/repository/4", json=payload)

    expect(response.status_code).to(equal(HTTPStatus.OK))
    expect(response.json()).to(equal(mock_update_Transaction_case.return_value))


def test_update_Transaction_not_found(mock_update_Transaction_case):
    mock_update_Transaction_case.return_value = None

    payload = {"nombre": "Ghost", "telefono": "000000"}

    response = Users.put("/api/v1/repo/repository/999", json=payload)

    expect(response.status_code).to(equal(HTTPStatus.NOT_FOUND))
    expect(response.json()["detail"]).to(equal("Transaction not found"))
