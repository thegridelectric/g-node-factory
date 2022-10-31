"""Tests for schema enum registry.g.node.role"""
from gnf.enums import RegistryGNodeRole


def test_component_category():

    assert set(RegistryGNodeRole.values()) == {
        "GNodeFactory",
        "WorldInstanceRegistry",
        "WorldCoordinator",
        "GNodeRegistry",
        "GridWorks",
    }

    assert RegistryGNodeRole.default() == RegistryGNodeRole.GridWorks
