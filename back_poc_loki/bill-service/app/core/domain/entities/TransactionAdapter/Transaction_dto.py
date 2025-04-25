from dataclasses import dataclass

from app.core.domain.entities.base_entity import BaseEntity


@dataclass
class TransactionDto(BaseEntity):
    id: int
    name: str
    status: str
    species: str
    type: str
    gender: str
    image: str
    url: str
    created: str
