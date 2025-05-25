from types import MappingProxyType

from app.core.application.ports.Users_adapter_port import UsersAdapterPort
from app.core.domain.entities.UsersAdapter.Users_dto import UsersDto
from app.infrastructure.api.schemas.exceptions import BusinessError
from app.infrastructure.http.http_client import HttpClient

API_Users_PREFIX = "api/v1/"

Users_ENDPOINTS = MappingProxyType({
    'get_character': f'{API_Users_PREFIX}empty'
})


class UsersAdapterService(UsersAdapterPort):
    def __init__(self, http_client: HttpClient):
        self._http_client = http_client

    async def get_Users_by_id(self, Users_id: str) -> UsersDto:
        try:
            print("On Users adapter service start ---")
            url = Users_ENDPOINTS['get_character']
            get_character_by_id_url = f"{url}?Empty_id={Users_id}"

            print(f"Trying to get to URL = {get_character_by_id_url}")

            response = self._http_client.get(
                endpoint=get_character_by_id_url
            )
            return UsersDto.from_dict(response)
        except Exception as error:
            raise BusinessError(f"Error on get petition - {error}")
