"""Makes create.ctn.algo.001 type"""
import json
from typing import List

from errors import SchemaError
from schemata.create_ctn_algo import CreateCtnAlgo


class CreateCtnAlgo_Maker:
    type_name = "create.ctn.algo.001"

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

        gw_tuple = CreateCtnAlgo(
            ChildAliasList=child_alias_list,
            FromGNodeAlias=from_g_node_alias,
            MicroLat=micro_lat,
            MicroLon=micro_lon,
            CtnGNodeAlias=ctn_g_node_alias,
            GNodeRegistryAddr=g_node_registry_addr,
            FromGNodeInstanceId=from_g_node_instance_id,
            #
        )
        gw_tuple.check_for_errors()
        self.tuple = gw_tuple

    @classmethod
    def tuple_to_type(cls, tuple: CreateCtnAlgo) -> str:
        tuple.check_for_errors()
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
        new_d = {}
        for key in d.keys():
            new_d[key] = d[key]
        if "TypeName" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TypeName")
        if "ChildAliasList" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing ChildAliasList")
        if "FromGNodeAlias" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing FromGNodeAlias")
        if "MicroLat" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing MicroLat")
        if "MicroLon" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing MicroLon")
        if "CtnGNodeAlias" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing CtnGNodeAlias")
        if "GNodeRegistryAddr" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing GNodeRegistryAddr")
        if "FromGNodeInstanceId" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing FromGNodeInstanceId")

        gw_tuple = CreateCtnAlgo(
            TypeName=new_d["TypeName"],
            ChildAliasList=new_d["ChildAliasList"],
            FromGNodeAlias=new_d["FromGNodeAlias"],
            MicroLat=new_d["MicroLat"],
            MicroLon=new_d["MicroLon"],
            CtnGNodeAlias=new_d["CtnGNodeAlias"],
            GNodeRegistryAddr=new_d["GNodeRegistryAddr"],
            FromGNodeInstanceId=new_d["FromGNodeInstanceId"],
            #
        )
        gw_tuple.check_for_errors()
        return gw_tuple
