from http import HTTPStatus
from unittest.mock import AsyncMock, patch

import pytest
from expects import equal, expect
from fastapi.testclient import TestClient

from app.infrastructure.api.main import app
from app.infrastructure.api.routers.Empty_adapter_router import router
from app.infrastructure.api.schemas.User_schema import EmptyResponseService
from app.infrastructure.api.schemas.exceptions import BusinessError
from fastapi import status

app.include_router(router)
Empty = TestClient(app)

router_path = "app.infrastructure.api.routers.Empty_adapter_router"


@pytest.fixture
def mock_Empty_adapter_use_case():
    with patch(
        router_path + ".builder_Empty_adapter_use_case"
    ) as mock_factory:
        mock_use_case = AsyncMock()
        mock_factory.return_value = mock_use_case
        yield mock_use_case


def test_get_Empty_by_id_success(mock_Empty_adapter_use_case):
    mock_Empty_adapter_use_case.get_Empty_by_id_case.return_value = EmptyResponseService(
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

    response = Empty.get("/api/v1/Empty/?Empty_id=1")

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

def test_get_Empty_by_id_business_error(mock_Empty_adapter_use_case):
    test_error = BusinessError(
        message="Test error", 
        http_status=status.HTTP_400_BAD_REQUEST
    )
    mock_Empty_adapter_use_case.get_Empty_by_id_case.side_effect = test_error
    response = Empty.get("/api/v1/Empty/?Empty_id=1")

    expect(response.status_code).to(equal(status.HTTP_400_BAD_REQUEST))
    expect(response.json()).to(equal({
        "detail": "Test error"
    }))
