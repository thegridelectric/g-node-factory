"""Schema enum registry.g.node.role.100 definition.

This includes the definition of:
    - the local python enum RegistryGNodeRole
    - the SchemaEnum RegistryGNodeRole100SchemaEnum

The SchemaEnum is a list of symbols sent in API/ABI messages. Its symbols
are not supposed to be human readable.

The LocalEnum are intended to be human readable.

The two are in bijection via the ComponentCategoryMap."""

from typing import Dict

from enums.registry_g_node_role_100 import RegistryGNodeRole
from enums.registry_g_node_role_100 import RegistryGNodeRole100SchemaEnum
from errors import SchemaError


class RegistryGNodeRoleSchemaEnum(RegistryGNodeRole100SchemaEnum):
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

    @classmethod
    def is_symbol(cls, candidate) -> bool:
        if candidate in cls.symbols:
            return True
        return False


class RegistryGNodeRoleMap:
    @classmethod
    def type_to_local(cls, symbol):
        if not RegistryGNodeRoleSchemaEnum.is_symbol(symbol):
            raise SchemaError(
                f"{symbol} must belong to key of {RegistryGNodeRoleMap.type_to_local_dict}"
            )
        return cls.type_to_local_dict[symbol]

    @classmethod
    def local_to_type(cls, registry_g_node_role):
        if not isinstance(registry_g_node_role, RegistryGNodeRole):
            raise SchemaError(
                f"{registry_g_node_role} must be of type {RegistryGNodeRole}"
            )
        return cls.local_to_type_dict[registry_g_node_role]

    type_to_local_dict: Dict[str, RegistryGNodeRole] = {
        "79503448": RegistryGNodeRole.G_NODE_FACTORY,
        "baa537f6": RegistryGNodeRole.WORLD_INSTANCE_REGISTRY,
        "06469a3c": RegistryGNodeRole.WORLD_COORDINATOR,
        "63a78529": RegistryGNodeRole.G_NODE_REGISTRY,
        "f0f14c88": RegistryGNodeRole.GRID_WORKS,
    }

    local_to_type_dict: Dict[RegistryGNodeRole, str] = {
        RegistryGNodeRole.G_NODE_FACTORY: "79503448",
        RegistryGNodeRole.WORLD_INSTANCE_REGISTRY: "baa537f6",
        RegistryGNodeRole.WORLD_COORDINATOR: "06469a3c",
        RegistryGNodeRole.G_NODE_REGISTRY: "63a78529",
        RegistryGNodeRole.GRID_WORKS: "f0f14c88",
        #
    }
