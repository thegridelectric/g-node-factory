"""status.basegnode.010 type"""

import json
from typing import List
from typing import NamedTuple

import gnf.property_format as property_format
from gnf.errors import SchemaError
from gnf.schemata.basegnode_gt import BasegnodeGt


class StatusBasegnode(NamedTuple):
    IncludeAllDescendants: bool  #
    DescendantGNodeList: List[BasegnodeGt]
    FromGNodeAlias: str  #
    FromGNodeInstanceId: str  #
    TopGNodeId: str
    ToGNodeAlias: str  #
    TypeName: str = "status.basegnode.010"

    def as_type(self) -> str:
        return json.dumps(self.asdict())

    def asdict(self):
        d = self._asdict()

        # Recursively call asdict() for the SubTypes
        descendant_g_node_list = []
        for elt in self.DescendantGNodeList:
            descendant_g_node_list.append(elt.asdict())
        d["DescendantGNodeList"] = descendant_g_node_list
        return d

    def derived_errors(self) -> List[str]:
        errors = []
        if not isinstance(self.IncludeAllDescendants, bool):
            errors.append(
                f"IncludeAllDescendants {self.IncludeAllDescendants} must have type bool."
            )
        if not isinstance(self.DescendantGNodeList, list):
            errors.append(
                f"DescendantGNodeList {self.DescendantGNodeList} must have type list."
            )
        else:
            for elt in self.DescendantGNodeList:
                if not isinstance(elt, BasegnodeGt):
                    errors.append(
                        f"elt {elt} of DescendantGNodeList must have type BasegnodeGt."
                    )
        if not isinstance(self.FromGNodeAlias, str):
            errors.append(f"FromGNodeAlias {self.FromGNodeAlias} must have type str.")
        try:
            property_format.check_is_lrd_alias_format(self.FromGNodeAlias)
        except SchemaError as e:
            errors.append(
                f"FromGNodeAlias {self.FromGNodeAlias}"
                " must have format LrdAliasFormat: {e}"
            )
        if not isinstance(self.FromGNodeInstanceId, str):
            errors.append(
                f"FromGNodeInstanceId {self.FromGNodeInstanceId} must have type str."
            )
        try:
            property_format.check_is_uuid_canonical_textual(self.FromGNodeInstanceId)
        except SchemaError as e:
            errors.append(
                f"FromGNodeInstanceId {self.FromGNodeInstanceId}"
                " must have format UuidCanonicalTextual: {e}"
            )
        if not isinstance(self.TopGNodeId, str):
            errors.append(f"TopGNodeId {self.TopGNodeId} must have type str.")
        try:
            property_format.check_is_uuid_canonical_textual(self.TopGNodeId)
        except SchemaError as e:
            errors.append(
                f"TopGNodeId {self.TopGNodeId}" " must have format UuidCanonicalTextual"
            )
        if not isinstance(self.ToGNodeAlias, str):
            errors.append(f"ToGNodeAlias {self.ToGNodeAlias} must have type str.")
        try:
            property_format.check_is_lrd_alias_format(self.ToGNodeAlias)
        except SchemaError as e:
            errors.append(
                f"ToGNodeAlias {self.ToGNodeAlias}"
                " must have format LrdAliasFormat: {e}"
            )
        if self.TypeName != "status.basegnode.010":
            errors.append(
                f"Type requires TypeName of status.basegnode.010, not {self.TypeName}."
            )

        return errors

    def check_for_errors(self):
        if self.derived_errors() == []:
            errors = self.hand_coded_errors()
        else:
            errors = self.derived_errors()
        if len(errors) > 0:
            raise SchemaError(
                f"Errors making status.basegnode.010 for {self}: {errors}"
            )

    def __repr__(self):
        return "StatusBasegnode"

    def hand_coded_errors(self):
        return []


class StatusBasegnode_Maker:
    type_name = "status.basegnode.010"

    def __init__(
        self,
        include_all_descendants: bool,
        descendant_g_node_list: List[BasegnodeGt],
        from_g_node_alias: str,
        from_g_node_instance_id: str,
        top_g_node_id: str,
        to_g_node_alias: str,
    ):

        gw_tuple = StatusBasegnode(
            IncludeAllDescendants=include_all_descendants,
            DescendantGNodeList=descendant_g_node_list,
            FromGNodeAlias=from_g_node_alias,
            FromGNodeInstanceId=from_g_node_instance_id,
            TopGNodeId=top_g_node_id,
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
                    "BasegnodeGt but not even a dict!"
                )
            descendant_g_node_list.append(BasegnodeGt_Maker.dict_to_tuple(elt))
        new_d["DescendantGNodeList"] = descendant_g_node_list
        if "FromGNodeAlias" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing FromGNodeAlias")
        if "FromGNodeInstanceId" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing FromGNodeInstanceId")
        if "TopGNodeId" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TopGNodeId")
        if "ToGNodeAlias" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing ToGNodeAlias")

        gw_tuple = StatusBasegnode(
            TypeName=new_d["TypeName"],
            IncludeAllDescendants=new_d["IncludeAllDescendants"],
            DescendantGNodeList=new_d["DescendantGNodeList"],
            FromGNodeAlias=new_d["FromGNodeAlias"],
            FromGNodeInstanceId=new_d["FromGNodeInstanceId"],
            TopGNodeId=new_d["TopGNodeId"],
            ToGNodeAlias=new_d["ToGNodeAlias"],
            #
        )
        gw_tuple.check_for_errors()
        return gw_tuple
