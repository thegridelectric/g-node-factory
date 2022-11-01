"""Type status.basegnode, version 010"""
import json
from typing import Dict
from typing import List
from typing import Literal

from pydantic import BaseModel
from pydantic import validator

import gnf.property_format as property_format
from gnf.errors import SchemaError
from gnf.property_format import predicate_validator
from gnf.schemata.basegnode_gt import BasegnodeGt
from gnf.schemata.basegnode_gt import BasegnodeGt_Maker


class StatusBasegnode(BaseModel):
    IncludeAllDescendants: bool  #
    DescendantGNodeList: List[BasegnodeGt]
    FromGNodeAlias: str  #
    FromGNodeInstanceId: str  #
    TopGNodeId: str
    ToGNodeAlias: str  #
    TypeName: Literal["status.basegnode"] = "status.basegnode"
    Version: str = "010"

    @validator("DescendantGNodeList")
    def _validator_descendant_g_node_list(cls, v: List) -> List:
        for elt in v:
            if not isinstance(elt, BasegnodeGt):
                raise ValueError(
                    f"elt {elt} of DescendantGNodeList must have type BasegnodeGt."
                )
        return v

    _validator_from_g_node_alias = predicate_validator(
        "FromGNodeAlias", property_format.is_lrd_alias_format
    )

    _validator_from_g_node_instance_id = predicate_validator(
        "FromGNodeInstanceId", property_format.is_uuid_canonical_textual
    )

    _validator_to_g_node_alias = predicate_validator(
        "ToGNodeAlias", property_format.is_lrd_alias_format
    )

    def as_dict(self) -> Dict:
        d = self.dict()

        # Recursively call as_dict() for the SubTypes
        descendant_g_node_list = []
        for elt in self.DescendantGNodeList:
            descendant_g_node_list.append(elt.as_dict())
        d["DescendantGNodeList"] = descendant_g_node_list
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class StatusBasegnode_Maker:
    type_name = "status.basegnode"
    version = "010"

    def __init__(
        self,
        include_all_descendants: bool,
        descendant_g_node_list: List[BasegnodeGt],
        from_g_node_alias: str,
        from_g_node_instance_id: str,
        top_g_node_id: str,
        to_g_node_alias: str,
    ):

        self.tuple = StatusBasegnode(
            IncludeAllDescendants=include_all_descendants,
            DescendantGNodeList=descendant_g_node_list,
            FromGNodeAlias=from_g_node_alias,
            FromGNodeInstanceId=from_g_node_instance_id,
            TopGNodeId=top_g_node_id,
            ToGNodeAlias=to_g_node_alias,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: StatusBasegnode) -> str:
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
        d2 = dict(d)
        if "DescendantGNodeList" not in d2.keys():
            raise SchemaError(f"dict {d2} missing DescendantGNodeList")
        descendant_g_node_list = []
        if not isinstance(d2["DescendantGNodeList"], List):
            raise SchemaError("DescendantGNodeList must be a List!")
        for elt in d2["DescendantGNodeList"]:
            if not isinstance(elt, dict):
                raise SchemaError(
                    f"elt {elt} of DescendantGNodeList must be "
                    "BasegnodeGt but not even a dict!"
                )
            descendant_g_node_list.append(BasegnodeGt_Maker.dict_to_tuple(elt))
        d2["DescendantGNodeList"] = descendant_g_node_list
        if "TopGNodeId" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TopGNodeId")

        return StatusBasegnode(
            IncludeAllDescendants=d2["IncludeAllDescendants"],
            DescendantGNodeList=d2["DescendantGNodeList"],
            FromGNodeAlias=d2["FromGNodeAlias"],
            FromGNodeInstanceId=d2["FromGNodeInstanceId"],
            TopGNodeId=d2["TopGNodeId"],
            ToGNodeAlias=d2["ToGNodeAlias"],
            TypeName=d2["TypeName"],
            Version="010",
        )
