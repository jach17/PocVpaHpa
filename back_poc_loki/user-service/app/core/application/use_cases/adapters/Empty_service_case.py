from app.core.application.ports.Empty_adapter_port import EmptyAdapterPort


class EmptyUseCase:
    def __init__(self, Empty_service_adapter: EmptyAdapterPort):
        self.Empty_service_adapter = Empty_service_adapter

    async def get_Empty_by_id_case(self, Empty_id: str):
        return await self.Empty_service_adapter.get_Empty_by_id(Empty_id=Empty_id)
