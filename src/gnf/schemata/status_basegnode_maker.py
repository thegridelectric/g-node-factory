"""Makes status.basegnode.010 type"""
import json
from typing import List

from errors import SchemaError
from schemata.basegnode_maker import Basegnode
from schemata.basegnode_maker import Basegnode_Maker
from schemata.status_basegnode import StatusBasegnode


class StatusBasegnode_Maker:
    type_name = "status.basegnode.010"

    def __init__(
        self,
        include_all_descendants: bool,
        descendant_g_node_list: List[Basegnode],
        from_g_node_alias: str,
        from_g_node_instance_id: str,
        top_g_node: Basegnode,
        to_g_node_alias: str,
    ):

        gw_tuple = StatusBasegnode(
            IncludeAllDescendants=include_all_descendants,
            DescendantGNodeList=descendant_g_node_list,
            FromGNodeAlias=from_g_node_alias,
            FromGNodeInstanceId=from_g_node_instance_id,
            TopGNode=top_g_node,
            ToGNodeAlias=to_g_node_alias,
            #
        )
        gw_tuple.check_for_errors()
        self.tuple = gw_tuple

    @classmethod
    def tuple_to_type(cls, tuple: StatusBasegnode) -> str:
        tuple.check_for_errors()
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> StatusBasegnode:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> StatusBasegnode:
        new_d = {}
        for key in d.keys():
            new_d[key] = d[key]
        if "TypeName" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TypeName")
        if "IncludeAllDescendants" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing IncludeAllDescendants")
        if "DescendantGNodeList" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing DescendantGNodeList")
        descendant_g_node_list = []
        for elt in new_d["DescendantGNodeList"]:
            if not isinstance(elt, dict):
                raise SchemaError(
                    f"elt {elt} of DescendantGNodeList must be "
                    "Basegnode but not even a dict!"
                )
            descendant_g_node_list.append(Basegnode_Maker.dict_to_tuple(elt))
        new_d["DescendantGNodeList"] = descendant_g_node_list
        if "FromGNodeAlias" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing FromGNodeAlias")
        if "FromGNodeInstanceId" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing FromGNodeInstanceId")
        if "TopGNode" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TopGNode")
        if not isinstance(new_d["TopGNode"], dict):
            raise SchemaError(f"d['TopGNode'] {new_d['TopGNode']} must be a Basegnode!")
        top_g_node = Basegnode_Maker.dict_to_tuple(new_d["TopGNode"])
        new_d["TopGNode"] = top_g_node
        if "ToGNodeAlias" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing ToGNodeAlias")

        gw_tuple = StatusBasegnode(
            TypeName=new_d["TypeName"],
            IncludeAllDescendants=new_d["IncludeAllDescendants"],
            DescendantGNodeList=new_d["DescendantGNodeList"],
            FromGNodeAlias=new_d["FromGNodeAlias"],
            FromGNodeInstanceId=new_d["FromGNodeInstanceId"],
            TopGNode=new_d["TopGNode"],
            ToGNodeAlias=new_d["ToGNodeAlias"],
            #
        )
        gw_tuple.check_for_errors()
        return gw_tuple
