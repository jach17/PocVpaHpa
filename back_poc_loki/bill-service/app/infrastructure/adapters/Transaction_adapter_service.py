from types import MappingProxyType

from app.core.application.ports.Transaction_adapter_port import TransactionAdapterPort
from app.core.domain.entities.TransactionAdapter.Transaction_dto import TransactionDto
from app.infrastructure.api.schemas.exceptions import BusinessError
from app.infrastructure.http.http_client import HttpClient

API_Transaction_PREFIX = "api/v1/"

Transaction_ENDPOINTS = MappingProxyType({
    'get_character': f'{API_Transaction_PREFIX}transaction/user'
})


class TransactionAdapterService(TransactionAdapterPort):
    def __init__(self, http_client: HttpClient):
        self._http_client = http_client

    async def get_Transaction_by_id(self, Transaction_id: str) -> TransactionDto:
        try:
            print("On Transaction adapter service start ---")
            url = Transaction_ENDPOINTS['get_character']
            get_character_by_id_url = f"{url}?Users_id={Transaction_id}"

            print(f"Trying to get to URL = {get_character_by_id_url}")

            response = self._http_client.get(
                endpoint=get_character_by_id_url
            )
            
            return TransactionDto.from_dict(response)
        except Exception as error:
            raise BusinessError(f"Error on get petition - {error}")
