"""Schema enum core.g.node.role.100 definition.

Look in enums/core_g_node_role_100 for:
    - the local python enum CoreGNodeRole
    - the SchemaEnum CoreGNodeRole100SchemaEnum

The SchemaEnum is a list of symbols sent in API/ABI messages. Its symbols
are not supposed to be human readable.

The LocalEnum are intended to be human readable."""

import enum
from abc import ABC
from typing import List


class CoreGNodeRole(enum.Enum):
    """
    CONDUCTOR_TOPOLOGY_NODE,
    ATOMIC_T_NODE,
    TERMINAL_ASSET,
    INTERCONNECTION_COMPONENT,
    OTHER,
    MARKET_MAKER,
    ATOMIC_METERING_NODE,

    This is the human readable half of the core.g.node.role.100 schema enum.

    The schema enum is immutable, and used in the GridWorks Spaceheat Schemata.

    APIs using this schemata WILL BREAK if this enum is changed by hand.

    If you think the current version should be updated in the schema registry,
    please contact the  owner of this schema (Jessica Millar) at:

    jmillar@gridworks-consulting.com

    and make your case for a new semantic version for core.g.node.role.100.

    You should not have to think about the machine-readable half of the enum.

    TL; DR However, if you want to understand how it works:

    The bijection between human and machine readable sets is defined by the:
      - type_to_local and
      - local_to_type

    methods of CoreGNodeRoleMap (in enums.core_g_node_role_map.py).
    """

    @classmethod
    def values(cls):
        return [elt.value for elt in cls]

    CONDUCTOR_TOPOLOGY_NODE = "ConductorTopologyNode"
    ATOMIC_T_NODE = "AtomicTNode"
    TERMINAL_ASSET = "TerminalAsset"
    INTERCONNECTION_COMPONENT = "InterconnectionComponent"
    OTHER = "Other"
    MARKET_MAKER = "MarketMaker"
    ATOMIC_METERING_NODE = "AtomicMeteringNode"
    #


class CoreGNodeRole100SchemaEnum(ABC):
    """
    Map to a  CoreGNodeRole enum:
        "4502e355" -> CONDUCTOR_TOPOLOGY_NODE,
        "d9823442" -> ATOMIC_T_NODE,
        "0f8872f7" -> TERMINAL_ASSET,
        "d67e564e" -> INTERCONNECTION_COMPONENT,
        "6b58d301" -> OTHER,
        "86f21dd2" -> MARKET_MAKER,
        "9521af06" -> ATOMIC_METERING_NODE,

    The machine readable half of the core.g.node.role.100 schema enum.

    Appear in API messages using the Gridworks Spaceheat Schemata.

    The bijection between human and machine readable sets is defined by the:
    - type_to_local and
    - local_to_type

    methods of CoreGNodeRoleMap (in enums.core_g_node_role_map.py).
    """

    symbols: List[str] = [
        "4502e355",
        "d9823442",
        "0f8872f7",
        "d67e564e",
        "6b58d301",
        "86f21dd2",
        "9521af06",
        #
    ]
