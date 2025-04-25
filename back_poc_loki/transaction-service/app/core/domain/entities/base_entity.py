from dataclasses import asdict, fields, is_dataclass
from typing import Any, Dict, TypedDict


class BaseEntity(object):
    def dump(self) -> dict:
        return asdict(self)

    def asdict_custom(self) -> Dict[str, Any]:
        if not is_dataclass(self):
            return {
            key: value.asdict_custom() if isinstance(value, BaseEntity) else value
            for key, value in vars(self).items()
        }

        custom: Dict[str, Any] = {}
        for field in fields(self):
            field_value = getattr(self, field.name)
            key = field.metadata.get('data_key', field.name)

            if isinstance(field_value, list):
                custom[key] = [
                    record.asdict_custom() if isinstance(record, BaseEntity) else record
                    for record in field_value
                ]
            elif isinstance(field_value, BaseEntity):
                custom[key] = field_value.asdict_custom()
            else:
                custom[key] = field_value

        return custom

    @classmethod
    def from_dict(cls, raw: dict):
        valid_keys = {f.name for f in fields(cls)}
        filtered_data = {k: v for k, v in raw.items() if k in valid_keys}
        return cls(**filtered_data)


class TemplateResponseDict(TypedDict):
    success: bool
    message: str
