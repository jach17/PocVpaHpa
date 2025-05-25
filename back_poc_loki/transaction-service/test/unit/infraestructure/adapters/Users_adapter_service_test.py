import pytest
from expects import expect, equal
from unittest.mock import Mock

from app.infrastructure.adapters.Users_adapter_service import UsersAdapterService
from app.infrastructure.api.schemas.exceptions import BusinessError
from app.infrastructure.adapters.Users_adapter_service import Users_ENDPOINTS


@pytest.fixture
def mock_http_Users():
    return Mock()


@pytest.fixture
def adapter(mock_http_Users):
    return UsersAdapterService(http_client=mock_http_Users)

@pytest.mark.asyncio
async def test_get_Users_by_id_success(adapter, mock_http_Users):
    mock_response = {
        "id": 1,
        "name": "Rick Sanchez",
        "status": "Alive",
        "species": "Human",
        "type": "",
        "gender": "Male",
        "image": "https://rick.com/avatar/1.jpeg",
        "url": "https://rick.com/character/1",
        "created": "2024-01-01T00:00:00Z"
    }

    mock_http_Users.get.return_value = mock_response

    Users_dto = await adapter.get_Users_by_id("1")

    expect(Users_dto.id).to(equal(1))
    expect(Users_dto.name).to(equal("Rick Sanchez"))
    expect(Users_dto.status).to(equal("Alive"))
    expect(Users_dto.image).to(equal(mock_response["image"]))

@pytest.mark.asyncio
async def test_get_Users_by_id_raises_business_error(adapter, mock_http_Users):
    test_error = Exception("API Error")
    mock_http_Users.get.side_effect = test_error

    with pytest.raises(BusinessError) as exc_info:
        await adapter.get_Users_by_id("1")

    expected_error_message = f"Error on get petition - {test_error}"
    assert str(exc_info.value) == expected_error_message

    expected_endpoint = f"{Users_ENDPOINTS['get_character']}/1"
    mock_http_Users.get.assert_called_once_with(endpoint=expected_endpoint)