"""Schema enum registry.g.node.role.100 definition.

Look in enums/registry_g_node_role_100 for:
    - the local python enum RegistryGNodeRole
    - the SchemaEnum RegistryGNodeRole100SchemaEnum

The SchemaEnum is a list of symbols sent in API/ABI messages. Its symbols
are not supposed to be human readable.

The LocalEnum are intended to be human readable."""

import enum
from abc import ABC
from typing import List


class RegistryGNodeRole(enum.Enum):
    """
    G_NODE_FACTORY,
    WORLD_INSTANCE_REGISTRY,
    WORLD_COORDINATOR,
    G_NODE_REGISTRY,
    GRID_WORKS,

    This is the human readable half of the registry.g.node.role.100 schema enum.

    The schema enum is immutable, and used in the GridWorks Spaceheat Schemata.

    APIs using this schemata WILL BREAK if this enum is changed by hand.

    If you think the current version should be updated in the schema registry,
    please contact the  owner of this schema (Jessica Millar) at:

    jmillar@gridworks-consulting.com

    and make your case for a new semantic version for registry.g.node.role.100.

    You should not have to think about the machine-readable half of the enum.

    TL; DR However, if you want to understand how it works:

    The bijection between human and machine readable sets is defined by the:
      - type_to_local and
      - local_to_type

    methods of RegistryGNodeRoleMap (in enums.registry_g_node_role_map.py).
    """

    @classmethod
    def values(cls):
        return [elt.value for elt in cls]

    G_NODE_FACTORY = "GNodeFactory"
    WORLD_INSTANCE_REGISTRY = "WorldInstanceRegistry"
    WORLD_COORDINATOR = "WorldCoordinator"
    G_NODE_REGISTRY = "GNodeRegistry"
    GRID_WORKS = "GridWorks"
    #


class RegistryGNodeRole100SchemaEnum(ABC):
    """
    Map to a  RegistryGNodeRole enum:
        "79503448" -> G_NODE_FACTORY,
        "baa537f6" -> WORLD_INSTANCE_REGISTRY,
        "06469a3c" -> WORLD_COORDINATOR,
        "63a78529" -> G_NODE_REGISTRY,
        "f0f14c88" -> GRID_WORKS,

    The machine readable half of the registry.g.node.role.100 schema enum.

    Appear in API messages using the Gridworks Spaceheat Schemata.

    The bijection between human and machine readable sets is defined by the:
    - type_to_local and
    - local_to_type

    methods of RegistryGNodeRoleMap (in enums.registry_g_node_role_map.py).
    """

    symbols: List[str] = [
        "79503448",
        "baa537f6",
        "06469a3c",
        "63a78529",
        "f0f14c88",
        #
    ]
