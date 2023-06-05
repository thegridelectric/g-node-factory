"""Type basegnode.ctn.create, version 000"""
import json
from typing import Any
from typing import Dict
from typing import List
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


class BasegnodeCtnCreate(BaseModel):
    """ """

    FromGNodeAlias: str = Field(
        title="FromGNodeAlias",
    )
    FromGNodeInstanceId: str = Field(
        title="FromGNodeInstanceId",
    )
    CtnGNodeAlias: str = Field(
        title="CtnGNodeAlias",
    )
    MicroLat: int = Field(
        title="MicroLat",
    )
    MicroLon: int = Field(
        title="MicroLon",
    )
    ChildAliasList: List[str] = Field(
        title="ChildAliasList",
    )
    GNodeRegistryAddr: str = Field(
        title="GNodeRegistryAddr",
    )
    TypeName: Literal["basegnode.ctn.create"] = "basegnode.ctn.create"
    Version: str = "000"

    @validator("FromGNodeAlias")
    def _check_from_g_node_alias(cls, v: str) -> str:
        try:
            check_is_left_right_dot(v)
        except ValueError as e:
            raise ValueError(
                f"FromGNodeAlias failed LeftRightDot format validation: {e}"
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

    @validator("CtnGNodeAlias")
    def _check_ctn_g_node_alias(cls, v: str) -> str:
        try:
            check_is_left_right_dot(v)
        except ValueError as e:
            raise ValueError(
                f"CtnGNodeAlias failed LeftRightDot format validation: {e}"
            )
        return v

    @validator("ChildAliasList")
    def _check_child_alias_list(cls, v: List) -> List:
        for elt in v:
            try:
                check_is_left_right_dot(elt)
            except ValueError as e:
                raise ValueError(
                    f"ChildAliasList element {elt} failed LeftRightDot format validation: {e}"
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

    def as_dict(self) -> Dict[str, Any]:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class BasegnodeCtnCreate_Maker:
    type_name = "basegnode.ctn.create"
    version = "000"

    def __init__(
        self,
        from_g_node_alias: str,
        from_g_node_instance_id: str,
        ctn_g_node_alias: str,
        micro_lat: int,
        micro_lon: int,
        child_alias_list: List[str],
        g_node_registry_addr: str,
    ):
        self.tuple = BasegnodeCtnCreate(
            FromGNodeAlias=from_g_node_alias,
            FromGNodeInstanceId=from_g_node_instance_id,
            CtnGNodeAlias=ctn_g_node_alias,
            MicroLat=micro_lat,
            MicroLon=micro_lon,
            ChildAliasList=child_alias_list,
            GNodeRegistryAddr=g_node_registry_addr,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: BasegnodeCtnCreate) -> str:
        """
        Given a Python class object, returns the serialized JSON type object
        """
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> BasegnodeCtnCreate:
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
    def dict_to_tuple(cls, d: dict[str, Any]) -> BasegnodeCtnCreate:
        d2 = dict(d)
        if "FromGNodeAlias" not in d2.keys():
            raise SchemaError(f"dict {d2} missing FromGNodeAlias")
        if "FromGNodeInstanceId" not in d2.keys():
            raise SchemaError(f"dict {d2} missing FromGNodeInstanceId")
        if "CtnGNodeAlias" not in d2.keys():
            raise SchemaError(f"dict {d2} missing CtnGNodeAlias")
        if "MicroLat" not in d2.keys():
            raise SchemaError(f"dict {d2} missing MicroLat")
        if "MicroLon" not in d2.keys():
            raise SchemaError(f"dict {d2} missing MicroLon")
        if "ChildAliasList" not in d2.keys():
            raise SchemaError(f"dict {d2} missing ChildAliasList")
        if "GNodeRegistryAddr" not in d2.keys():
            raise SchemaError(f"dict {d2} missing GNodeRegistryAddr")
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return BasegnodeCtnCreate(
            FromGNodeAlias=d2["FromGNodeAlias"],
            FromGNodeInstanceId=d2["FromGNodeInstanceId"],
            CtnGNodeAlias=d2["CtnGNodeAlias"],
            MicroLat=d2["MicroLat"],
            MicroLon=d2["MicroLon"],
            ChildAliasList=d2["ChildAliasList"],
            GNodeRegistryAddr=d2["GNodeRegistryAddr"],
            TypeName=d2["TypeName"],
            Version="000",
        )
