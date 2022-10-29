"""Makes create.discoverycert.algo.001 type"""
import json
from typing import List
from typing import Optional

from enums.core_g_node_role_map import CoreGNodeRole
from enums.core_g_node_role_map import CoreGNodeRoleMap
from errors import SchemaError
from schemata.create_discoverycert_algo import CreateDiscoverycertAlgo


class CreateDiscoverycertAlgo_Maker:
    type_name = "create.discoverycert.algo.001"

    def __init__(
        self,
        old_child_alias_list: List[str],
        g_node_alias: str,
        discoverer_addr: str,
        supporting_material_hash: str,
        core_g_node_role: CoreGNodeRole,
        micro_lon: Optional[int],
        micro_lat: Optional[int],
    ):

        gw_tuple = CreateDiscoverycertAlgo(
            OldChildAliasList=old_child_alias_list,
            GNodeAlias=g_node_alias,
            DiscovererAddr=discoverer_addr,
            MicroLon=micro_lon,
            SupportingMaterialHash=supporting_material_hash,
            CoreGNodeRole=core_g_node_role,
            MicroLat=micro_lat,
            #
        )
        gw_tuple.check_for_errors()
        self.tuple = gw_tuple

    @classmethod
    def tuple_to_type(cls, tuple: CreateDiscoverycertAlgo) -> str:
        tuple.check_for_errors()
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> CreateDiscoverycertAlgo:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> CreateDiscoverycertAlgo:
        new_d = {}
        for key in d.keys():
            new_d[key] = d[key]
        if "TypeName" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TypeName")
        if "OldChildAliasList" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing OldChildAliasList")
        if "GNodeAlias" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing GNodeAlias")
        if "DiscovererAddr" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing DiscovererAddr")
        if "MicroLon" not in new_d.keys():
            new_d["MicroLon"] = None
        if "SupportingMaterialHash" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing SupportingMaterialHash")
        if "CoreGNodeRoleGtEnumSymbol" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing CoreGNodeRoleGtEnumSymbol")
        new_d["CoreGNodeRole"] = CoreGNodeRoleMap.gt_to_local(
            new_d["CoreGNodeRoleGtEnumSymbol"]
        )
        if "MicroLat" not in new_d.keys():
            new_d["MicroLat"] = None

        gw_tuple = CreateDiscoverycertAlgo(
            TypeName=new_d["TypeName"],
            OldChildAliasList=new_d["OldChildAliasList"],
            GNodeAlias=new_d["GNodeAlias"],
            DiscovererAddr=new_d["DiscovererAddr"],
            MicroLon=new_d["MicroLon"],
            SupportingMaterialHash=new_d["SupportingMaterialHash"],
            CoreGNodeRole=new_d["CoreGNodeRole"],
            MicroLat=new_d["MicroLat"],
            #
        )
        gw_tuple.check_for_errors()
        return gw_tuple
