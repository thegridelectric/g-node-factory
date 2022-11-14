"""Type tadeed.specs.private.hack, version 000"""
import json
from typing import Any
from typing import Dict
from typing import Literal

from pydantic import BaseModel
from pydantic import validator

import gnf.property_format as property_format
from gnf.errors import SchemaError
from gnf.property_format import predicate_validator


class TadeedSpecsPrivateHack(BaseModel):
    TerminalAssetAlias: str  #
    TaOwnerSk: str  #
    TaDaemonSk: str  #
    MicroLat: int  #
    MicroLon: int  #
    TypeName: Literal["tadeed.specs.private.hack"] = "tadeed.specs.private.hack"
    Version: str = "000"

    _validator_terminal_asset_alias = predicate_validator(
        "TerminalAssetAlias", property_format.is_lrd_alias_format
    )

    def as_dict(self) -> Dict[str, Any]:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class TadeedSpecsPrivateHack_Maker:
    type_name = "tadeed.specs.private.hack"
    version = "000"

    def __init__(
        self,
        terminal_asset_alias: str,
        ta_owner_sk: str,
        ta_daemon_sk: str,
        micro_lat: int,
        micro_lon: int,
    ):

        self.tuple = TadeedSpecsPrivateHack(
            TerminalAssetAlias=terminal_asset_alias,
            TaOwnerSk=ta_owner_sk,
            TaDaemonSk=ta_daemon_sk,
            MicroLat=micro_lat,
            MicroLon=micro_lon,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: TadeedSpecsPrivateHack) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> TadeedSpecsPrivateHack:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict[str, Any]) -> TadeedSpecsPrivateHack:
        d2 = dict(d)
        if "TerminalAssetAlias" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TerminalAssetAlias")
        if "TaOwnerSk" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TaOwnerSk")
        if "TaDaemonSk" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TaDaemonSk")
        if "MicroLat" not in d2.keys():
            raise SchemaError(f"dict {d2} missing MicroLat")
        if "MicroLon" not in d2.keys():
            raise SchemaError(f"dict {d2} missing MicroLon")
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return TadeedSpecsPrivateHack(
            TerminalAssetAlias=d2["TerminalAssetAlias"],
            TaOwnerSk=d2["TaOwnerSk"],
            TaDaemonSk=d2["TaDaemonSk"],
            MicroLat=d2["MicroLat"],
            MicroLon=d2["MicroLon"],
            TypeName=d2["TypeName"],
            Version="000",
        )
