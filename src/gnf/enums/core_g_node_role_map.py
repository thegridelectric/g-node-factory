"""Schema enum core.g.node.role.100 definition.

This includes the definition of:
    - the local python enum CoreGNodeRole
    - the SchemaEnum CoreGNodeRole100SchemaEnum

The SchemaEnum is a list of symbols sent in API/ABI messages. Its symbols
are not supposed to be human readable.

The LocalEnum are intended to be human readable.

The two are in bijection via the ComponentCategoryMap."""

from typing import Dict

from enums.core_g_node_role_100 import CoreGNodeRole
from enums.core_g_node_role_100 import CoreGNodeRole100SchemaEnum
from errors import SchemaError


class CoreGNodeRoleSchemaEnum(CoreGNodeRole100SchemaEnum):
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

    @classmethod
    def is_symbol(cls, candidate) -> bool:
        if candidate in cls.symbols:
            return True
        return False


class CoreGNodeRoleMap:
    @classmethod
    def type_to_local(cls, symbol):
        if not CoreGNodeRoleSchemaEnum.is_symbol(symbol):
            raise SchemaError(
                f"{symbol} must belong to key of {CoreGNodeRoleMap.type_to_local_dict}"
            )
        return cls.type_to_local_dict[symbol]

    @classmethod
    def local_to_type(cls, core_g_node_role):
        if not isinstance(core_g_node_role, CoreGNodeRole):
            raise SchemaError(f"{core_g_node_role} must be of type {CoreGNodeRole}")
        return cls.local_to_type_dict[core_g_node_role]

    type_to_local_dict: Dict[str, CoreGNodeRole] = {
        "4502e355": CoreGNodeRole.CONDUCTOR_TOPOLOGY_NODE,
        "d9823442": CoreGNodeRole.ATOMIC_T_NODE,
        "0f8872f7": CoreGNodeRole.TERMINAL_ASSET,
        "d67e564e": CoreGNodeRole.INTERCONNECTION_COMPONENT,
        "6b58d301": CoreGNodeRole.OTHER,
        "86f21dd2": CoreGNodeRole.MARKET_MAKER,
        "9521af06": CoreGNodeRole.ATOMIC_METERING_NODE,
    }

    local_to_type_dict: Dict[CoreGNodeRole, str] = {
        CoreGNodeRole.CONDUCTOR_TOPOLOGY_NODE: "4502e355",
        CoreGNodeRole.ATOMIC_T_NODE: "d9823442",
        CoreGNodeRole.TERMINAL_ASSET: "0f8872f7",
        CoreGNodeRole.INTERCONNECTION_COMPONENT: "d67e564e",
        CoreGNodeRole.OTHER: "6b58d301",
        CoreGNodeRole.MARKET_MAKER: "86f21dd2",
        CoreGNodeRole.ATOMIC_METERING_NODE: "9521af06",
        #
    }
