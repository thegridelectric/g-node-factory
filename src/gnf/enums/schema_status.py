from enum import auto

from fastapi_utils.enums import StrEnum


class SchemaStatus(StrEnum):
    @classmethod
    def values(cls):
        return [elt.value for elt in cls]

    Deprecated = auto()
    Active = auto()
    Pending = auto()
