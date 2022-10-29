"""Tests for scehma enum registry.g.node.role.100"""

import pytest
from enums.registry_g_node_role_map import RegistryGNodeRole
from enums.registry_g_node_role_map import RegistryGNodeRoleMap as Map
from enums.registry_g_node_role_map import RegistryGNodeRoleSchemaEnum
from errors import SchemaError


def test_component_category():

    assert set(RegistryGNodeRole.values()) == {
        "GNodeFactory",
        "WorldInstanceRegistry",
        "WorldCoordinator",
        "GNodeRegistry",
        "GridWorks",
    }

    assert set(RegistryGNodeRoleSchemaEnum.symbols) == {
        "79503448",
        "baa537f6",
        "06469a3c",
        "63a78529",
        "f0f14c88",
    }

    assert len(RegistryGNodeRole.values()) == len(RegistryGNodeRoleSchemaEnum.symbols)

    assert Map.type_to_local("79503448") == RegistryGNodeRole.G_NODE_FACTORY
    assert Map.type_to_local("baa537f6") == RegistryGNodeRole.WORLD_INSTANCE_REGISTRY
    assert Map.type_to_local("06469a3c") == RegistryGNodeRole.WORLD_COORDINATOR
    assert Map.type_to_local("63a78529") == RegistryGNodeRole.G_NODE_REGISTRY
    assert Map.type_to_local("f0f14c88") == RegistryGNodeRole.GRID_WORKS

    with pytest.raises(SchemaError):
        Map.type_to_local("aaa")

    with pytest.raises(SchemaError):
        Map.local_to_type("Load")

    for symbol in RegistryGNodeRoleSchemaEnum.symbols:
        assert Map.local_to_type(Map.type_to_local(symbol)) == symbol
