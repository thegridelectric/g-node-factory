"""Schema enum g.node.status.100 definition.

Look in enums/g_node_status_100 for:
    - the local python enum GNodeStatus
    - the SchemaEnum GNodeStatus100SchemaEnum

The SchemaEnum is a list of symbols sent in API/ABI messages. Its symbols
are not supposed to be human readable.

The LocalEnum are intended to be human readable."""

import enum
from abc import ABC
from typing import List


class GNodeStatus(enum.Enum):
    """
    PERMANENTLY_DEACTIVATED,
    PENDING,
    ACTIVE,
    SUSPENDED,

    This is the human readable half of the g.node.status.100 schema enum.

    The schema enum is immutable, and used in the GridWorks Spaceheat Schemata.

    APIs using this schemata WILL BREAK if this enum is changed by hand.

    If you think the current version should be updated in the schema registry,
    please contact the  owner of this schema (Jessica Millar) at:

    jmillar@gridworks-consulting.com

    and make your case for a new semantic version for g.node.status.100.

    You should not have to think about the machine-readable half of the enum.

    TL; DR However, if you want to understand how it works:

    The bijection between human and machine readable sets is defined by the:
      - type_to_local and
      - local_to_type

    methods of GNodeStatusMap (in enums.g_node_status_map.py).
    """

    @classmethod
    def values(cls):
        return [elt.value for elt in cls]

    PERMANENTLY_DEACTIVATED = "PermanentlyDeactivated"
    PENDING = "Pending"
    ACTIVE = "Active"
    SUSPENDED = "Suspended"
    #


class GNodeStatus100SchemaEnum(ABC):
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

    symbols: List[str] = [
        "839b38db",
        "153d3475",
        "8d92bebe",
        "f5831e1d",
        #
    ]
