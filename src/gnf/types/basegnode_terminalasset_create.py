"""Type basegnode.terminalasset.create, version 000"""
import json
from typing import Any
from typing import Dict
from typing import Literal

from gridworks.errors import SchemaError
from pydantic import BaseModel
from pydantic import Field
from pydantic import validator


def check_is_uuid_canonical_textual(v: str) -> None:
    """
    UuidCanonicalTextual format:  A string of hex words separated by hyphens
    of length 8-4-4-4-12.

    Raises:
        ValueError: if not UuidCanonicalTextual format
    """
    try:
        x = v.split("-")
    except AttributeError as e:
        raise ValueError(f"Failed to split on -: {e}")
    if len(x) != 5:
        raise ValueError(f"{v} split by '-' did not have 5 words")
    for hex_word in x:
        try:
            int(hex_word, 16)
        except ValueError:
            raise ValueError(f"Words of {v} are not all hex")
    if len(x[0]) != 8:
        raise ValueError(f"{v} word lengths not 8-4-4-4-12")
    if len(x[1]) != 4:
        raise ValueError(f"{v} word lengths not 8-4-4-4-12")
    if len(x[2]) != 4:
        raise ValueError(f"{v} word lengths not 8-4-4-4-12")
    if len(x[3]) != 4:
        raise ValueError(f"{v} word lengths not 8-4-4-4-12")
    if len(x[4]) != 12:
        raise ValueError(f"{v} word lengths not 8-4-4-4-12")


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


class BasegnodeTerminalassetCreate(BaseModel):
    """ """

    TaGNodeAlias: str = Field(
        title="TaGNodeAlias",
    )
    MicroLon: int = Field(
        title="MicroLon",
    )
    ValidatorAddr: str = Field(
        title="ValidatorAddr",
    )
    TaOwnerAddr: str = Field(
        title="TaOwnerAddr",
    )
    MicroLat: int = Field(
        title="MicroLat",
    )
    GNodeRegistryAddr: str = Field(
        title="GNodeRegistryAddr",
    )
    FromGNodeInstanceId: str = Field(
        title="FromGNodeInstanceId",
    )
    FromGNodeAlias: str = Field(
        title="FromGNodeAlias",
    )
    TypeName: Literal[
        "basegnode.terminalasset.create"
    ] = "basegnode.terminalasset.create"
    Version: str = "000"

    @validator("TaGNodeAlias")
    def _check_ta_g_node_alias(cls, v: str) -> str:
        try:
            check_is_left_right_dot(v)
        except ValueError as e:
            raise ValueError(f"TaGNodeAlias failed LeftRightDot format validation: {e}")
        return v

    @validator("ValidatorAddr")
    def _check_validator_addr(cls, v: str) -> str:
        try:
            check_is_algo_address_string_format(v)
        except ValueError as e:
            raise ValueError(
                f"ValidatorAddr failed AlgoAddressStringFormat format validation: {e}"
            )
        return v

    @validator("TaOwnerAddr")
    def _check_ta_owner_addr(cls, v: str) -> str:
        try:
            check_is_algo_address_string_format(v)
        except ValueError as e:
            raise ValueError(
                f"TaOwnerAddr failed AlgoAddressStringFormat format validation: {e}"
            )
        return v

    @validator("GNodeRegistryAddr")
    def _check_g_node_registry_addr(cls, v: str) -> str:
        try:
            check_is_algo_address_string_format(v)
        except ValueError as e:
            raise ValueError(
                f"GNodeRegistryAddr failed AlgoAddressStringFormat format validation: {e}"
            )
        return v

    @validator("FromGNodeInstanceId")
    def _check_from_g_node_instance_id(cls, v: str) -> str:
        try:
            check_is_uuid_canonical_textual(v)
        except ValueError as e:
            raise ValueError(
                f"FromGNodeInstanceId failed UuidCanonicalTextual format validation: {e}"
            )
        return v

    @validator("FromGNodeAlias")
    def _check_from_g_node_alias(cls, v: str) -> str:
        try:
            check_is_left_right_dot(v)
        except ValueError as e:
            raise ValueError(
                f"FromGNodeAlias failed LeftRightDot format validation: {e}"
            )
        return v

    def as_dict(self) -> Dict[str, Any]:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class BasegnodeTerminalassetCreate_Maker:
    type_name = "basegnode.terminalasset.create"
    version = "000"

    def __init__(
        self,
        ta_g_node_alias: str,
        micro_lon: int,
        validator_addr: str,
        ta_owner_addr: str,
        micro_lat: int,
        g_node_registry_addr: str,
        from_g_node_instance_id: str,
        from_g_node_alias: str,
    ):
        self.tuple = BasegnodeTerminalassetCreate(
            TaGNodeAlias=ta_g_node_alias,
            MicroLon=micro_lon,
            ValidatorAddr=validator_addr,
            TaOwnerAddr=ta_owner_addr,
            MicroLat=micro_lat,
            GNodeRegistryAddr=g_node_registry_addr,
            FromGNodeInstanceId=from_g_node_instance_id,
            FromGNodeAlias=from_g_node_alias,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: BasegnodeTerminalassetCreate) -> str:
        """
        Given a Python class object, returns the serialized JSON type object
        """
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> BasegnodeTerminalassetCreate:
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
    def dict_to_tuple(cls, d: dict[str, Any]) -> BasegnodeTerminalassetCreate:
        d2 = dict(d)
        if "TaGNodeAlias" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TaGNodeAlias")
        if "MicroLon" not in d2.keys():
            raise SchemaError(f"dict {d2} missing MicroLon")
        if "ValidatorAddr" not in d2.keys():
            raise SchemaError(f"dict {d2} missing ValidatorAddr")
        if "TaOwnerAddr" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TaOwnerAddr")
        if "MicroLat" not in d2.keys():
            raise SchemaError(f"dict {d2} missing MicroLat")
        if "GNodeRegistryAddr" not in d2.keys():
            raise SchemaError(f"dict {d2} missing GNodeRegistryAddr")
        if "FromGNodeInstanceId" not in d2.keys():
            raise SchemaError(f"dict {d2} missing FromGNodeInstanceId")
        if "FromGNodeAlias" not in d2.keys():
            raise SchemaError(f"dict {d2} missing FromGNodeAlias")
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return BasegnodeTerminalassetCreate(
            TaGNodeAlias=d2["TaGNodeAlias"],
            MicroLon=d2["MicroLon"],
            ValidatorAddr=d2["ValidatorAddr"],
            TaOwnerAddr=d2["TaOwnerAddr"],
            MicroLat=d2["MicroLat"],
            GNodeRegistryAddr=d2["GNodeRegistryAddr"],
            FromGNodeInstanceId=d2["FromGNodeInstanceId"],
            FromGNodeAlias=d2["FromGNodeAlias"],
            TypeName=d2["TypeName"],
            Version="000",
        )
