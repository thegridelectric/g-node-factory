"""Type basegnodes.broadcast, version 000"""
import json
from typing import Any
from typing import Dict
from typing import List
from typing import Literal

from gridworks.errors import SchemaError
from pydantic import BaseModel
from pydantic import Field
from pydantic import validator

from gnf.types.base_g_node_gt import BaseGNodeGt
from gnf.types.base_g_node_gt import BaseGNodeGt_Maker


def check_is_uuid_canonical_textual(v: str) -> None:
    """
    UuidCanonicalTextual format:  A string of hex words separated by hyphens
    of length 8-4-4-4-12.

    Raises:
        ValueError: if not UuidCanonicalTextual format
    """
    try:
        x = v.split("-")
    except AttributeError as e:
        raise ValueError(f"Failed to split on -: {e}")
    if len(x) != 5:
        raise ValueError(f"{v} split by '-' did not have 5 words")
    for hex_word in x:
        try:
            int(hex_word, 16)
        except ValueError:
            raise ValueError(f"Words of {v} are not all hex")
    if len(x[0]) != 8:
        raise ValueError(f"{v} word lengths not 8-4-4-4-12")
    if len(x[1]) != 4:
        raise ValueError(f"{v} word lengths not 8-4-4-4-12")
    if len(x[2]) != 4:
        raise ValueError(f"{v} word lengths not 8-4-4-4-12")
    if len(x[3]) != 4:
        raise ValueError(f"{v} word lengths not 8-4-4-4-12")
    if len(x[4]) != 12:
        raise ValueError(f"{v} word lengths not 8-4-4-4-12")


def check_is_left_right_dot(v: str) -> None:
    """
    LeftRightDot format: Lowercase alphanumeric words separated by periods,
    most significant word (on the left) starting with an alphabet character.

    Raises:
        ValueError: if not LeftRightDot format
    """
    from typing import List

    try:
        x: List[str] = v.split(".")
    except:
        raise ValueError(f"Failed to seperate {v} into words with split'.'")
    first_word = x[0]
    first_char = first_word[0]
    if not first_char.isalpha():
        raise ValueError(f"Most significant word of {v} must start with alphabet char.")
    for word in x:
        if not word.isalnum():
            raise ValueError(f"words of {v} split by by '.' must be alphanumeric.")
    if not v.islower():
        raise ValueError(f"All characters of {v} must be lowercase.")


class BasegnodesBroadcast(BaseModel):
    """ """

    FromGNodeAlias: str = Field(
        title="FromGNodeAlias",
    )
    FromGNodeInstanceId: str = Field(
        title="FromGNodeInstanceId",
    )
    IncludeAllDescendants: bool = Field(
        title="IncludeAllDescendants",
    )
    TopGNode: BaseGNodeGt = Field(
        title="TopGNode",
    )
    DescendantGNodeList: List[BaseGNodeGt] = Field(
        title="DescendantGNodeList",
    )
    TypeName: Literal["basegnodes.broadcast"] = "basegnodes.broadcast"
    Version: str = "000"

    @validator("FromGNodeAlias")
    def _check_from_g_node_alias(cls, v: str) -> str:
        try:
            check_is_left_right_dot(v)
        except ValueError as e:
            raise ValueError(
                f"FromGNodeAlias failed LeftRightDot format validation: {e}"
            )
        return v

    @validator("FromGNodeInstanceId")
    def _check_from_g_node_instance_id(cls, v: str) -> str:
        try:
            check_is_uuid_canonical_textual(v)
        except ValueError as e:
            raise ValueError(
                f"FromGNodeInstanceId failed UuidCanonicalTextual format validation: {e}"
            )
        return v

    @validator("DescendantGNodeList")
    def _check_descendant_g_node_list(cls, v: List) -> List:
        for elt in v:
            if not isinstance(elt, BaseGNodeGt):
                raise ValueError(
                    f"elt {elt} of DescendantGNodeList must have type BaseGNodeGt."
                )
        return v

    def as_dict(self) -> Dict[str, Any]:
        d = self.dict()
        d["TopGNode"] = self.TopGNode.as_dict()

        # Recursively call as_dict() for the SubTypes
        descendant_g_node_list = []
        for elt in self.DescendantGNodeList:
            descendant_g_node_list.append(elt.as_dict())
        d["DescendantGNodeList"] = descendant_g_node_list
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class BasegnodesBroadcast_Maker:
    type_name = "basegnodes.broadcast"
    version = "000"

    def __init__(
        self,
        from_g_node_alias: str,
        from_g_node_instance_id: str,
        include_all_descendants: bool,
        top_g_node: BaseGNodeGt,
        descendant_g_node_list: List[BaseGNodeGt],
    ):
        self.tuple = BasegnodesBroadcast(
            FromGNodeAlias=from_g_node_alias,
            FromGNodeInstanceId=from_g_node_instance_id,
            IncludeAllDescendants=include_all_descendants,
            TopGNode=top_g_node,
            DescendantGNodeList=descendant_g_node_list,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: BasegnodesBroadcast) -> str:
        """
        Given a Python class object, returns the serialized JSON type object
        """
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> BasegnodesBroadcast:
        """
        Given a serialized JSON type object, returns the Python class object
        """
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict[str, Any]) -> BasegnodesBroadcast:
        d2 = dict(d)
        if "FromGNodeAlias" not in d2.keys():
            raise SchemaError(f"dict {d2} missing FromGNodeAlias")
        if "FromGNodeInstanceId" not in d2.keys():
            raise SchemaError(f"dict {d2} missing FromGNodeInstanceId")
        if "IncludeAllDescendants" not in d2.keys():
            raise SchemaError(f"dict {d2} missing IncludeAllDescendants")
        if "TopGNode" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TopGNode")
        if not isinstance(d2["TopGNode"], dict):
            raise SchemaError(f"d['TopGNode'] {d2['TopGNode']} must be a BaseGNodeGt!")
        top_g_node = BaseGNodeGt_Maker.dict_to_tuple(d2["TopGNode"])
        d2["TopGNode"] = top_g_node
        if "DescendantGNodeList" not in d2.keys():
            raise SchemaError(f"dict {d2} missing DescendantGNodeList")
        descendant_g_node_list = []
        if not isinstance(d2["DescendantGNodeList"], List):
            raise SchemaError("DescendantGNodeList must be a List!")
        for elt in d2["DescendantGNodeList"]:
            if not isinstance(elt, dict):
                raise SchemaError(
                    f"elt {elt} of DescendantGNodeList must be "
                    "BaseGNodeGt but not even a dict!"
                )
            descendant_g_node_list.append(BaseGNodeGt_Maker.dict_to_tuple(elt))
        d2["DescendantGNodeList"] = descendant_g_node_list
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return BasegnodesBroadcast(
            FromGNodeAlias=d2["FromGNodeAlias"],
            FromGNodeInstanceId=d2["FromGNodeInstanceId"],
            IncludeAllDescendants=d2["IncludeAllDescendants"],
            TopGNode=d2["TopGNode"],
            DescendantGNodeList=d2["DescendantGNodeList"],
            TypeName=d2["TypeName"],
            Version="000",
        )
