"""create.terminalasset.algo.010 type"""
import json
from typing import Dict
from typing import Literal

from pydantic import BaseModel

import gnf.property_format as property_format
from gnf.errors import SchemaError
from gnf.property_format import predicate_validator


class CreateTerminalassetAlgo(BaseModel):
    TaGNodeAlias: str  #
    MicroLon: int  #
    ValidatorAddr: str  #
    TaOwnerAddr: str  #
    MicroLat: int  #
    GNodeRegistryAddr: str  #
    FromGNodeInstanceId: str  #
    FromGNodeAlias: str  #
    TypeName: Literal["create.terminalasset.algo"] = "create.terminalasset.algo"

    _validator_ta_g_node_alias = predicate_validator(
        "TaGNodeAlias", property_format.is_lrd_alias_format
    )

    _validator_validator_addr = predicate_validator(
        "ValidatorAddr", property_format.is_algo_address_string_format
    )

    _validator_ta_owner_addr = predicate_validator(
        "TaOwnerAddr", property_format.is_algo_address_string_format
    )

    _validator_g_node_registry_addr = predicate_validator(
        "GNodeRegistryAddr", property_format.is_algo_address_string_format
    )

    _validator_from_g_node_instance_id = predicate_validator(
        "FromGNodeInstanceId", property_format.is_uuid_canonical_textual
    )

    _validator_from_g_node_alias = predicate_validator(
        "FromGNodeAlias", property_format.is_lrd_alias_format
    )

    def as_dict(self) -> Dict:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class CreateTerminalassetAlgo_Maker:
    type_name = "create.terminalasset.algo"

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

        self.tuple = CreateTerminalassetAlgo(
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
    def tuple_to_type(cls, tuple: CreateTerminalassetAlgo) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> CreateTerminalassetAlgo:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> CreateTerminalassetAlgo:
        d2 = dict(d)
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return CreateTerminalassetAlgo(
            TypeName=d2["TypeName"],
            TaGNodeAlias=d2["TaGNodeAlias"],
            MicroLon=d2["MicroLon"],
            ValidatorAddr=d2["ValidatorAddr"],
            TaOwnerAddr=d2["TaOwnerAddr"],
            MicroLat=d2["MicroLat"],
            GNodeRegistryAddr=d2["GNodeRegistryAddr"],
            FromGNodeInstanceId=d2["FromGNodeInstanceId"],
            FromGNodeAlias=d2["FromGNodeAlias"],
        )
