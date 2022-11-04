"""Tests for schema enum registry.g.node.role.100"""
from gnf.enums import RegistryGNodeRole


def test_registry_g_node_role():

    assert set(RegistryGNodeRole.values()) == {
        "Unknown",
        "GNodeFactory",
        "GNodeRegistry",
        "WorldInstanceRegistry",
        "WorldCoordinator",
        "GridWorks",
    }

    assert RegistryGNodeRole.default() == RegistryGNodeRole.Unknown
