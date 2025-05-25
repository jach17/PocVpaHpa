from pydantic import BaseModel


class BillCreate(BaseModel):
    nombre: str
    telefono: str


class BillResponse(BaseModel):
    id: int
    nombre: str
    telefono: str

    class Config:
        orm_mode = True


class TransactionResponseService(BaseModel):
    id: int
    name: str
    status: str
    species: str
    type: str
    gender: str
    image: str
    url: str
    created: str

    class Config:
        from_attributes = True
