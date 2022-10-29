"""Makes create.terminalasset.algo.010 type"""
import json

from errors import SchemaError
from schemata.create_terminalasset_algo import CreateTerminalassetAlgo


class CreateTerminalassetAlgo_Maker:
    type_name = "create.terminalasset.algo.010"

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

        gw_tuple = CreateTerminalassetAlgo(
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
        gw_tuple.check_for_errors()
        self.tuple = gw_tuple

    @classmethod
    def tuple_to_type(cls, tuple: CreateTerminalassetAlgo) -> str:
        tuple.check_for_errors()
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
        new_d = {}
        for key in d.keys():
            new_d[key] = d[key]
        if "TypeName" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TypeName")
        if "TaGNodeAlias" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TaGNodeAlias")
        if "MicroLon" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing MicroLon")
        if "ValidatorAddr" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing ValidatorAddr")
        if "TaOwnerAddr" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TaOwnerAddr")
        if "MicroLat" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing MicroLat")
        if "GNodeRegistryAddr" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing GNodeRegistryAddr")
        if "FromGNodeInstanceId" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing FromGNodeInstanceId")
        if "FromGNodeAlias" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing FromGNodeAlias")

        gw_tuple = CreateTerminalassetAlgo(
            TypeName=new_d["TypeName"],
            TaGNodeAlias=new_d["TaGNodeAlias"],
            MicroLon=new_d["MicroLon"],
            ValidatorAddr=new_d["ValidatorAddr"],
            TaOwnerAddr=new_d["TaOwnerAddr"],
            MicroLat=new_d["MicroLat"],
            GNodeRegistryAddr=new_d["GNodeRegistryAddr"],
            FromGNodeInstanceId=new_d["FromGNodeInstanceId"],
            FromGNodeAlias=new_d["FromGNodeAlias"],
            #
        )
        gw_tuple.check_for_errors()
        return gw_tuple
