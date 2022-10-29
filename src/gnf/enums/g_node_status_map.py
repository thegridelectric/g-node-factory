"""Schema enum g.node.status.100 definition.

This includes the definition of:
    - the local python enum GNodeStatus
    - the SchemaEnum GNodeStatus100SchemaEnum

The SchemaEnum is a list of symbols sent in API/ABI messages. Its symbols
are not supposed to be human readable.

The LocalEnum are intended to be human readable.

The two are in bijection via the ComponentCategoryMap."""

from typing import Dict

from enums.g_node_status_100 import GNodeStatus
from enums.g_node_status_100 import GNodeStatus100SchemaEnum
from errors import SchemaError


class GNodeStatusSchemaEnum(GNodeStatus100SchemaEnum):
    """
    Map to a  GNodeStatus enum:
        "839b38db" -> PERMANENTLY_DEACTIVATED,
        "153d3475" -> PENDING,
        "8d92bebe" -> ACTIVE,
        "f5831e1d" -> SUSPENDED,

    The machine readable half of the g.node.status.100 schema enum.

    Appear in API messages using the Gridworks Spaceheat Schemata.

    The bijection between human and machine readable sets is defined by the:
    - type_to_local and
    - local_to_type

    methods of GNodeStatusMap (in enums.g_node_status_map.py).
    """

    @classmethod
    def is_symbol(cls, candidate) -> bool:
        if candidate in cls.symbols:
            return True
        return False


class GNodeStatusMap:
    @classmethod
    def type_to_local(cls, symbol):
        if not GNodeStatusSchemaEnum.is_symbol(symbol):
            raise SchemaError(
                f"{symbol} must belong to key of {GNodeStatusMap.type_to_local_dict}"
            )
        return cls.type_to_local_dict[symbol]

    @classmethod
    def local_to_type(cls, g_node_status):
        if not isinstance(g_node_status, GNodeStatus):
            raise SchemaError(f"{g_node_status} must be of type {GNodeStatus}")
        return cls.local_to_type_dict[g_node_status]

    type_to_local_dict: Dict[str, GNodeStatus] = {
        "839b38db": GNodeStatus.PERMANENTLY_DEACTIVATED,
        "153d3475": GNodeStatus.PENDING,
        "8d92bebe": GNodeStatus.ACTIVE,
        "f5831e1d": GNodeStatus.SUSPENDED,
    }

    local_to_type_dict: Dict[GNodeStatus, str] = {
        GNodeStatus.PERMANENTLY_DEACTIVATED: "839b38db",
        GNodeStatus.PENDING: "153d3475",
        GNodeStatus.ACTIVE: "8d92bebe",
        GNodeStatus.SUSPENDED: "f5831e1d",
        #
    }
