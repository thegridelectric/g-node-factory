"""Makes basegnode.020 type"""
import json
from typing import Optional

from data_classes.base_g_node import BaseGNode
from enums.core_g_node_role_map import CoreGNodeRole
from enums.core_g_node_role_map import CoreGNodeRoleMap
from enums.g_node_status_map import GNodeStatus
from enums.g_node_status_map import GNodeStatusMap
from errors import SchemaError
from schemata.basegnode import Basegnode


class Basegnode_Maker:
    type_name = "basegnode.020"

    def __init__(
        self,
        status: GNodeStatus,
        g_node_registry_addr: str,
        role: CoreGNodeRole,
        alias: str,
        g_node_id: int,
        prev_alias: Optional[str],
        trading_rights_nft_id: Optional[int],
        ownership_deed_validator_addr: Optional[str],
        ownership_deed_nft_id: Optional[int],
        owner_addr: Optional[str],
        daemon_addr: Optional[str],
        gps_point_id: Optional[str],
    ):

        gw_tuple = Basegnode(
            Status=status,
            GNodeRegistryAddr=g_node_registry_addr,
            Role=role,
            PrevAlias=prev_alias,
            TradingRightsNftId=trading_rights_nft_id,
            OwnershipDeedValidatorAddr=ownership_deed_validator_addr,
            Alias=alias,
            GNodeId=g_node_id,
            OwnershipDeedNftId=ownership_deed_nft_id,
            OwnerAddr=owner_addr,
            DaemonAddr=daemon_addr,
            GpsPointId=gps_point_id,
            #
        )
        gw_tuple.check_for_errors()
        self.tuple = gw_tuple

    @classmethod
    def tuple_to_type(cls, tuple: Basegnode) -> str:
        tuple.check_for_errors()
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> Basegnode:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> Basegnode:
        new_d = {}
        for key in d.keys():
            new_d[key] = d[key]
        if "TypeName" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TypeName")
        if "StatusGtEnumSymbol" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing StatusGtEnumSymbol")
        new_d["Status"] = GNodeStatusMap.gt_to_local(new_d["StatusGtEnumSymbol"])
        if "GNodeRegistryAddr" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing GNodeRegistryAddr")
        if "RoleGtEnumSymbol" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing RoleGtEnumSymbol")
        new_d["Role"] = CoreGNodeRoleMap.gt_to_local(new_d["RoleGtEnumSymbol"])
        if "PrevAlias" not in new_d.keys():
            new_d["PrevAlias"] = None
        if "TradingRightsNftId" not in new_d.keys():
            new_d["TradingRightsNftId"] = None
        if "OwnershipDeedValidatorAddr" not in new_d.keys():
            new_d["OwnershipDeedValidatorAddr"] = None
        if "Alias" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing Alias")
        if "GNodeId" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing GNodeId")
        if "OwnershipDeedNftId" not in new_d.keys():
            new_d["OwnershipDeedNftId"] = None
        if "OwnerAddr" not in new_d.keys():
            new_d["OwnerAddr"] = None
        if "DaemonAddr" not in new_d.keys():
            new_d["DaemonAddr"] = None
        if "GpsPointId" not in new_d.keys():
            new_d["GpsPointId"] = None

        gw_tuple = Basegnode(
            TypeName=new_d["TypeName"],
            Status=new_d["Status"],
            GNodeRegistryAddr=new_d["GNodeRegistryAddr"],
            Role=new_d["Role"],
            PrevAlias=new_d["PrevAlias"],
            TradingRightsNftId=new_d["TradingRightsNftId"],
            OwnershipDeedValidatorAddr=new_d["OwnershipDeedValidatorAddr"],
            Alias=new_d["Alias"],
            GNodeId=new_d["GNodeId"],
            OwnershipDeedNftId=new_d["OwnershipDeedNftId"],
            OwnerAddr=new_d["OwnerAddr"],
            DaemonAddr=new_d["DaemonAddr"],
            GpsPointId=new_d["GpsPointId"],
            #
        )
        gw_tuple.check_for_errors()
        return gw_tuple

    @classmethod
    def tuple_to_dc(cls, t: Basegnode) -> BaseGNode:
        s = {
            "g_node_registry_addr": t.GNodeRegistryAddr,
            "prev_alias": t.PrevAlias,
            "trading_rights_nft_id": t.TradingRightsNftId,
            "ownership_deed_validator_addr": t.OwnershipDeedValidatorAddr,
            "alias": t.Alias,
            "g_node_id": t.GNodeId,
            "ownership_deed_nft_id": t.OwnershipDeedNftId,
            "owner_addr": t.OwnerAddr,
            "daemon_addr": t.DaemonAddr,
            "gps_point_id": t.GpsPointId,
            "status_gt_enum_symbol": GNodeStatusMap.local_to_gt(t.Status),
            "role_gt_enum_symbol": CoreGNodeRoleMap.local_to_gt(t.Role),
            #
        }
        if s["base_g_node_id"] in BaseGNode.by_id.keys():
            dc = BaseGNode.by_id[s["base_g_node_id"]]
        else:
            dc = BaseGNode(**s)
        return dc

    @classmethod
    def dc_to_tuple(cls, dc: BaseGNode) -> Basegnode:
        if dc is None:
            return None
        t = Basegnode(
            Status=dc.status,
            GNodeRegistryAddr=dc.g_node_registry_addr,
            Role=dc.role,
            PrevAlias=dc.prev_alias,
            TradingRightsNftId=dc.trading_rights_nft_id,
            OwnershipDeedValidatorAddr=dc.ownership_deed_validator_addr,
            Alias=dc.alias,
            GNodeId=dc.g_node_id,
            OwnershipDeedNftId=dc.ownership_deed_nft_id,
            OwnerAddr=dc.owner_addr,
            DaemonAddr=dc.daemon_addr,
            GpsPointId=dc.gps_point_id,
            #
        )
        t.check_for_errors()
        return t

    @classmethod
    def type_to_dc(cls, t: str) -> BaseGNode:
        return cls.tuple_to_dc(cls.type_to_tuple(t))

    @classmethod
    def dc_to_type(cls, dc: BaseGNode) -> str:
        return cls.dc_to_tuple(dc).as_type()

    @classmethod
    def dict_to_dc(cls, d: dict) -> BaseGNode:
        return cls.tuple_to_dc(cls.dict_to_tuple(d))
