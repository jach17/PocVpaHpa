from types import MappingProxyType

from app.core.application.ports.Empty_adapter_port import EmptyAdapterPort
from app.core.domain.entities.EmptyAdapter.Empty_dto import EmptyDto
from app.infrastructure.api.schemas.exceptions import BusinessError
from app.infrastructure.http.http_client import HttpClient

API_Empty_PREFIX = "api/"

Empty_ENDPOINTS = MappingProxyType({
    'get_character': f'{API_Empty_PREFIX}character'
})


class EmptyAdapterService(EmptyAdapterPort):
    def __init__(self, http_client: HttpClient):
        self._http_client = http_client

    async def get_Empty_by_id(self, Empty_id: str) -> EmptyDto:
        try:
            print("On Empty adapter service start ---")
            url = Empty_ENDPOINTS['get_character']
            get_character_by_id_url = f"{url}/{Empty_id}"

            print(f"Trying to get to URL = {get_character_by_id_url}")

            response = self._http_client.get(
                endpoint=get_character_by_id_url
            )
            return EmptyDto.from_dict(response)
        except Exception as error:
            raise BusinessError(f"Error on get petition - {error}")
