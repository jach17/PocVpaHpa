from app.core.application.ports.Transaction_adapter_port import TransactionAdapterPort


class TransactionUseCase:
    def __init__(self, Transaction_service_adapter: TransactionAdapterPort):
        self.Transaction_service_adapter = Transaction_service_adapter

    async def get_Transaction_by_id_case(self, Transaction_id: str):
        return await self.Transaction_service_adapter.get_Transaction_by_id(Transaction_id=Transaction_id)
