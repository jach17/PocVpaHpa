from http import HTTPStatus
from unittest.mock import AsyncMock, patch

import pytest
from expects import expect, equal
from fastapi.testclient import TestClient

from app.infrastructure.api.main import app
from app.infrastructure.api.routers import User_repository_router
from app.infrastructure.api.schemas.User_schema import UserResponse

app.include_router(User_repository_router.router)
Empty = TestClient(app)

router_path = "app.infrastructure.api.routers.User_repository_router"


@pytest.fixture
def mock_get_all_Users_case():
    with patch(
        f"{router_path}.get_all_Users_case",
        new_callable=AsyncMock,
    ) as mock:
        yield mock


@pytest.fixture
def mock_create_User_case():
    with patch(
        f"{router_path}.create_User_case",
        new_callable=AsyncMock,
    ) as mock:
        yield mock


@pytest.fixture
def mock_update_User_case():
    with patch(
        f"{router_path}.update_User_case",
        new_callable=AsyncMock,
    ) as mock:
        yield mock


def test_list_Users_success(mock_get_all_Users_case):
    mock_get_all_Users_case.return_value = [
        {"id": 1, "nombre": "Alice", "telefono": "123456"},
        {"id": 2, "nombre": "Bob", "telefono": "654321"},
    ]

    response = Empty.get("/api/v1/repo/repository/")

    expect(response.status_code).to(equal(HTTPStatus.OK))
    expect(response.json()).to(equal(mock_get_all_Users_case.return_value))


def test_create_User_success(mock_create_User_case):
    mock_create_User_case.return_value = {
        "id": 3, "nombre": "Charlie", "telefono": "111222"
    }

    payload = {"nombre": "Charlie", "telefono": "111222"}

    response = Empty.post("/api/v1/repo/repository/", json=payload)

    expect(response.status_code).to(equal(HTTPStatus.OK))
    expect(response.json()).to(equal(mock_create_User_case.return_value))


def test_update_User_success(mock_update_User_case):
    mock_update_User_case.return_value = {
        "id": 4, "nombre": "Updated", "telefono": "999000"
    }

    payload = {"nombre": "Updated", "telefono": "999000"}

    response = Empty.put("/api/v1/repo/repository/4", json=payload)

    expect(response.status_code).to(equal(HTTPStatus.OK))
    expect(response.json()).to(equal(mock_update_User_case.return_value))


def test_update_User_not_found(mock_update_User_case):
    mock_update_User_case.return_value = None

    payload = {"nombre": "Ghost", "telefono": "000000"}

    response = Empty.put("/api/v1/repo/repository/999", json=payload)

    expect(response.status_code).to(equal(HTTPStatus.NOT_FOUND))
    expect(response.json()["detail"]).to(equal("User not found"))
