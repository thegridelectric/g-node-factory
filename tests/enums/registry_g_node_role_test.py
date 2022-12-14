"""Tests for schema enum registry.g.node.role.000"""
from gnf.enums import RegistryGNodeRole


def test_registry_g_node_role():

    assert set(RegistryGNodeRole.values()) == {
        "Unknown",
        "GNodeFactory",
        "GNodeRegistry",
        "WorldInstanceRegistry",
        "World",
        "GridWorks",
    }

    assert RegistryGNodeRole.default() == RegistryGNodeRole.Unknown
