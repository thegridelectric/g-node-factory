"""Type discoverycert.algo.transfer, version 000"""
import json
from typing import Any
from typing import Dict
from typing import Literal

from gridworks.errors import SchemaError
from pydantic import BaseModel
from pydantic import Field
from pydantic import validator


def check_is_left_right_dot(v: str) -> None:
    """
    LeftRightDot format: Lowercase alphanumeric words separated by periods,
    most significant word (on the left) starting with an alphabet character.

    Raises:
        ValueError: if not LeftRightDot format
    """
    from typing import List

    try:
        x: List[str] = v.split(".")
    except:
        raise ValueError(f"Failed to seperate {v} into words with split'.'")
    first_word = x[0]
    first_char = first_word[0]
    if not first_char.isalpha():
        raise ValueError(f"Most significant word of {v} must start with alphabet char.")
    for word in x:
        if not word.isalnum():
            raise ValueError(f"words of {v} split by by '.' must be alphanumeric.")
    if not v.islower():
        raise ValueError(f"All characters of {v} must be lowercase.")


def check_is_algo_address_string_format(v: str) -> None:
    """
    AlgoAddressStringFormat format: The public key of a private/public Ed25519
    key pair, transformed into an  Algorand address, by adding a 4-byte checksum
    to the end of the public key and then encoding in base32.

    Raises:
        ValueError: if not AlgoAddressStringFormat format
    """
    import algosdk

    at = algosdk.abi.AddressType()
    try:
        result = at.decode(at.encode(v))
    except Exception as e:
        raise ValueError(f"Not AlgoAddressStringFormat: {e}")


class DiscoverycertAlgoTransfer(BaseModel):
    """ """

    GNodeAlias: str = Field(
        title="GNodeAlias",
    )
    DiscovererAddr: str = Field(
        title="DiscovererAddr",
    )
    TypeName: Literal["discoverycert.algo.transfer"] = "discoverycert.algo.transfer"
    Version: str = "000"

    @validator("GNodeAlias")
    def _check_g_node_alias(cls, v: str) -> str:
        try:
            check_is_left_right_dot(v)
        except ValueError as e:
            raise ValueError(f"GNodeAlias failed LeftRightDot format validation: {e}")
        return v

    @validator("DiscovererAddr")
    def _check_discoverer_addr(cls, v: str) -> str:
        try:
            check_is_algo_address_string_format(v)
        except ValueError as e:
            raise ValueError(
                f"DiscovererAddr failed AlgoAddressStringFormat format validation: {e}"
            )
        return v

    def as_dict(self) -> Dict[str, Any]:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class DiscoverycertAlgoTransfer_Maker:
    type_name = "discoverycert.algo.transfer"
    version = "000"

    def __init__(self, g_node_alias: str, discoverer_addr: str):
        self.tuple = DiscoverycertAlgoTransfer(
            GNodeAlias=g_node_alias,
            DiscovererAddr=discoverer_addr,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: DiscoverycertAlgoTransfer) -> str:
        """
        Given a Python class object, returns the serialized JSON type object
        """
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> DiscoverycertAlgoTransfer:
        """
        Given a serialized JSON type object, returns the Python class object
        """
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict[str, Any]) -> DiscoverycertAlgoTransfer:
        d2 = dict(d)
        if "GNodeAlias" not in d2.keys():
            raise SchemaError(f"dict {d2} missing GNodeAlias")
        if "DiscovererAddr" not in d2.keys():
            raise SchemaError(f"dict {d2} missing DiscovererAddr")
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return DiscoverycertAlgoTransfer(
            GNodeAlias=d2["GNodeAlias"],
            DiscovererAddr=d2["DiscovererAddr"],
            TypeName=d2["TypeName"],
            Version="000",
        )
