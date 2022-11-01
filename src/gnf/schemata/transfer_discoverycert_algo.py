"""transfer.discoverycert.algo.001 type"""
import json
from typing import Dict
from typing import Literal

from pydantic import BaseModel

import gnf.property_format as property_format
from gnf.errors import SchemaError
from gnf.property_format import predicate_validator


class TransferDiscoverycertAlgo(BaseModel):
    GNodeAlias: str  #
    DiscovererAddr: str  #
    TypeName: Literal["transfer.discoverycert.algo"] = "transfer.discoverycert.algo"

    _validator_g_node_alias = predicate_validator(
        "GNodeAlias", property_format.is_lrd_alias_format
    )

    _validator_discoverer_addr = predicate_validator(
        "DiscovererAddr", property_format.is_algo_address_string_format
    )

    def as_dict(self) -> Dict:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class TransferDiscoverycertAlgo_Maker:
    type_name = "transfer.discoverycert.algo"

    def __init__(self, g_node_alias: str, discoverer_addr: str):

        self.tuple = TransferDiscoverycertAlgo(
            GNodeAlias=g_node_alias,
            DiscovererAddr=discoverer_addr,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: TransferDiscoverycertAlgo) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> TransferDiscoverycertAlgo:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> TransferDiscoverycertAlgo:
        d2 = dict(d)
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return TransferDiscoverycertAlgo(
            TypeName=d2["TypeName"],
            GNodeAlias=d2["GNodeAlias"],
            DiscovererAddr=d2["DiscovererAddr"],
        )
