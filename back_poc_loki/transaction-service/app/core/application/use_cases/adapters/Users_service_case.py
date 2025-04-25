from app.core.application.ports.Users_adapter_port import UsersAdapterPort


class UsersUseCase:
    def __init__(self, Users_service_adapter: UsersAdapterPort):
        self.Users_service_adapter = Users_service_adapter

    async def get_Users_by_id_case(self, Users_id: str):
        return await self.Users_service_adapter.get_Users_by_id(Users_id=Users_id)
