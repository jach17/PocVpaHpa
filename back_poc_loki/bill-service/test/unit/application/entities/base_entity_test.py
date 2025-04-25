import pytest
from dataclasses import dataclass, field
from app.core.domain.entities.base_entity import BaseEntity

# Clases de prueba que heredan de BaseEntity
@dataclass
class MockEntity(BaseEntity):
    id: str
    name: str = field(metadata={"data_key": "nombre"})

@dataclass
class NestedEntity(BaseEntity):
    value: int
    child: MockEntity

@dataclass
class ListEntity(BaseEntity):
    items: list[MockEntity]

def test_base_entity_dump():
    entity = MockEntity(id="1", name="Test")
    assert entity.dump() == {"id": "1", "name": "Test"}

def test_asdict_custom_simple_entity():
    entity = MockEntity(id="123", name="Hugo")
    
    result = entity.asdict_custom()
    
    assert result == {
        "id": "123",
        "nombre": "Hugo"  # Key renombrado por metadata
    }

def test_asdict_custom_nested_entity():
    nested = NestedEntity(
        value=42,
        child=MockEntity(id="2", name="Child")
    )
    
    result = nested.asdict_custom()
    
    assert result == {
        "value": 42,
        "child": {
            "id": "2",
            "nombre": "Child"
        }
    }

def test_asdict_custom_list_of_entities():
    list_entity = ListEntity(
        items=[
            MockEntity(id="1", name="Item1"),
            MockEntity(id="2", name="Item2")
        ]
    )
    
    result = list_entity.asdict_custom()
    
    assert result == {
        "items": [
            {"id": "1", "nombre": "Item1"},
            {"id": "2", "nombre": "Item2"}
        ]
    }

def test_asdict_custom_non_dataclass():
    class NonDataClass(BaseEntity):
        def __init__(self, value):
            self.value = value
    
    instance = NonDataClass(value=10)
    print(vars(instance))
    result = instance.asdict_custom()
    assert result == {"value": 10}
