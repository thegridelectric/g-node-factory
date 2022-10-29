"""Base for status.basegnode.010 """


import json
from typing import List
from typing import NamedTuple

import property_format
from errors import SchemaError
from schemata.basegnode_maker import Basegnode


class StatusBasegnodeBase(NamedTuple):
    IncludeAllDescendants: bool  #
    DescendantGNodeList: List[Basegnode]
    FromGNodeAlias: str  #
    FromGNodeInstanceId: str  #
    TopGNode: Basegnode  #
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
        d["TopGNode"] = self.TopGNode.asdict()
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
                if not isinstance(elt, Basegnode):
                    errors.append(
                        f"elt {elt} of DescendantGNodeList must have type Basegnode."
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
        if not isinstance(self.TopGNode, Basegnode):
            errors.append(f"TopGNode {self.TopGNode} must have typeBasegnode.")
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
