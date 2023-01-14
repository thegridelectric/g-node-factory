from enum import auto
from typing import List

from fastapi_utils.enums import StrEnum


class RegistryGNodeRole(StrEnum):
    """


    Choices and descriptions:

      * Unknown:
      * GNodeFactory:
      * GNodeRegistry:
      * WorldInstanceRegistry:
      * World:
      * GridWorks:
    """

    Unknown = auto()
    GNodeFactory = auto()
    GNodeRegistry = auto()
    WorldInstanceRegistry = auto()
    World = auto()
    GridWorks = auto()

    @classmethod
    def default(cls) -> "RegistryGNodeRole":
        """
        Returns default value Unknown
        """
        return cls.Unknown

    @classmethod
    def values(cls) -> List[str]:
        """
        Returns enum choices
        """
        return [elt.value for elt in cls]
