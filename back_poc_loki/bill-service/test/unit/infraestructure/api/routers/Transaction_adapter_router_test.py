from http import HTTPStatus
from unittest.mock import AsyncMock, patch

import pytest
from expects import equal, expect
from fastapi.testclient import TestClient

from app.infrastructure.api.main import app
from app.infrastructure.api.routers.Transaction_adapter_router import router
from app.infrastructure.api.schemas.Bill_schema import TransactionResponseService
from app.infrastructure.api.schemas.exceptions import BusinessError
from fastapi import status

app.include_router(router)
Transaction = TestClient(app)

router_path = "app.infrastructure.api.routers.Transaction_adapter_router"


@pytest.fixture
def mock_Transaction_adapter_use_case():
    with patch(
        router_path + ".builder_Transaction_adapter_use_case"
    ) as mock_factory:
        mock_use_case = AsyncMock()
        mock_factory.return_value = mock_use_case
        yield mock_use_case


def test_get_Transaction_by_id_success(mock_Transaction_adapter_use_case):
    mock_Transaction_adapter_use_case.get_Transaction_by_id_case.return_value = TransactionResponseService(
        id=1,
        name="Rick Sanchez",
        status="Alive",
        species="Human",
        type="",
        gender="Male",
        image="https://rickandmortyapi.com/api/character/avatar/1.jpeg",
        url="https://rickandmortyapi.com/api/character/1",
        created="2017-11-04T18:48:46.250Z"
    )

    response = Transaction.get("/api/v1/Transaction/?Transaction_id=1")

    expect(response.status_code).to(equal(HTTPStatus.OK))
    expect(response.json()).to(equal({
        "id": 1,
        "name": "Rick Sanchez",
        "status": "Alive",
        "species": "Human",
        "type": "",
        "gender": "Male",
        "image": "https://rickandmortyapi.com/api/character/avatar/1.jpeg",
        "url": "https://rickandmortyapi.com/api/character/1",
        "created": "2017-11-04T18:48:46.250Z"
    }))

def test_get_Transaction_by_id_business_error(mock_Transaction_adapter_use_case):
    test_error = BusinessError(
        message="Test error", 
        http_status=status.HTTP_400_BAD_REQUEST
    )
    mock_Transaction_adapter_use_case.get_Transaction_by_id_case.side_effect = test_error
    response = Transaction.get("/api/v1/Transaction/?Transaction_id=1")

    expect(response.status_code).to(equal(status.HTTP_400_BAD_REQUEST))
    expect(response.json()).to(equal({
        "detail": "Test error"
    }))
