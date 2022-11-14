"""Type tadeed.specs.hack, version 000"""
import json
from typing import Any
from typing import Dict
from typing import Literal

from pydantic import BaseModel
from pydantic import validator

import gnf.property_format as property_format
from gnf.errors import SchemaError
from gnf.property_format import predicate_validator


class TadeedSpecsHack(BaseModel):
    TerminalAssetAlias: str  #
    TaOwnerAddr: str  #
    TaDaemonAddr: str  #
    MicroLat: int  #
    MicroLon: int  #
    TypeName: Literal["tadeed.specs.hack"] = "tadeed.specs.hack"
    Version: str = "000"

    _validator_terminal_asset_alias = predicate_validator(
        "TerminalAssetAlias", property_format.is_lrd_alias_format
    )

    _validator_ta_owner_addr = predicate_validator(
        "TaOwnerAddr", property_format.is_algo_address_string_format
    )

    _validator_ta_daemon_addr = predicate_validator(
        "TaDaemonAddr", property_format.is_algo_address_string_format
    )

    def as_dict(self) -> Dict[str, Any]:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class TadeedSpecsHack_Maker:
    type_name = "tadeed.specs.hack"
    version = "000"

    def __init__(
        self,
        terminal_asset_alias: str,
        ta_owner_addr: str,
        ta_daemon_addr: str,
        micro_lat: int,
        micro_lon: int,
    ):

        self.tuple = TadeedSpecsHack(
            TerminalAssetAlias=terminal_asset_alias,
            TaOwnerAddr=ta_owner_addr,
            TaDaemonAddr=ta_daemon_addr,
            MicroLat=micro_lat,
            MicroLon=micro_lon,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: TadeedSpecsHack) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> TadeedSpecsHack:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict[str, Any]) -> TadeedSpecsHack:
        d2 = dict(d)
        if "TerminalAssetAlias" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TerminalAssetAlias")
        if "TaOwnerAddr" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TaOwnerAddr")
        if "TaDaemonAddr" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TaDaemonAddr")
        if "MicroLat" not in d2.keys():
            raise SchemaError(f"dict {d2} missing MicroLat")
        if "MicroLon" not in d2.keys():
            raise SchemaError(f"dict {d2} missing MicroLon")
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return TadeedSpecsHack(
            TerminalAssetAlias=d2["TerminalAssetAlias"],
            TaOwnerAddr=d2["TaOwnerAddr"],
            TaDaemonAddr=d2["TaDaemonAddr"],
            MicroLat=d2["MicroLat"],
            MicroLon=d2["MicroLon"],
            TypeName=d2["TypeName"],
            Version="000",
        )
