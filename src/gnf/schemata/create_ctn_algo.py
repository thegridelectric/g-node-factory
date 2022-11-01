"""Type create.ctn.algo, version 001"""
import json
from typing import Dict
from typing import List
from typing import Literal

from pydantic import BaseModel
from pydantic import validator

import gnf.property_format as property_format
from gnf.errors import SchemaError
from gnf.property_format import predicate_validator


class CreateCtnAlgo(BaseModel):
    ChildAliasList: List[str]
    FromGNodeAlias: str  #
    MicroLat: int  #
    MicroLon: int  #
    CtnGNodeAlias: str  #
    GNodeRegistryAddr: str  #
    FromGNodeInstanceId: str  #
    TypeName: Literal["create.ctn.algo"] = "create.ctn.algo"
    Version: str = "001"

    @validator("ChildAliasList")
    def _validator_child_alias_list(cls, v: List) -> List:
        for elt in v:
            if not property_format.is_lrd_alias_format(elt):
                raise ValueError(
                    f"failure of predicate is_lrd_alias_format() on elt {elt} of ChildAliasList"
                )
        return v

    _validator_from_g_node_alias = predicate_validator(
        "FromGNodeAlias", property_format.is_lrd_alias_format
    )

    _validator_ctn_g_node_alias = predicate_validator(
        "CtnGNodeAlias", property_format.is_lrd_alias_format
    )

    _validator_g_node_registry_addr = predicate_validator(
        "GNodeRegistryAddr", property_format.is_algo_address_string_format
    )

    _validator_from_g_node_instance_id = predicate_validator(
        "FromGNodeInstanceId", property_format.is_uuid_canonical_textual
    )

    def as_dict(self) -> Dict:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class CreateCtnAlgo_Maker:
    type_name = "create.ctn.algo"
    version = "001"

    def __init__(
        self,
        child_alias_list: List[str],
        from_g_node_alias: str,
        micro_lat: int,
        micro_lon: int,
        ctn_g_node_alias: str,
        g_node_registry_addr: str,
        from_g_node_instance_id: str,
    ):

        self.tuple = CreateCtnAlgo(
            ChildAliasList=child_alias_list,
            FromGNodeAlias=from_g_node_alias,
            MicroLat=micro_lat,
            MicroLon=micro_lon,
            CtnGNodeAlias=ctn_g_node_alias,
            GNodeRegistryAddr=g_node_registry_addr,
            FromGNodeInstanceId=from_g_node_instance_id,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: CreateCtnAlgo) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> CreateCtnAlgo:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> CreateCtnAlgo:
        d2 = dict(d)

        return CreateCtnAlgo(
            ChildAliasList=d2["ChildAliasList"],
            FromGNodeAlias=d2["FromGNodeAlias"],
            MicroLat=d2["MicroLat"],
            MicroLon=d2["MicroLon"],
            CtnGNodeAlias=d2["CtnGNodeAlias"],
            GNodeRegistryAddr=d2["GNodeRegistryAddr"],
            FromGNodeInstanceId=d2["FromGNodeInstanceId"],
            TypeName=d2["TypeName"],
            Version="001",
        )
