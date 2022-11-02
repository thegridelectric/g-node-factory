"""Tests for schema enum core.g.node.role.100"""
from gnf.enums import CoreGNodeRole


def test_core_g_node_role():

    assert set(CoreGNodeRole.values()) == {
        "Other",
        "TerminalAsset",
        "AtomicMeteringNode",
        "AtomicTNode",
        "MarketMaker",
        "ConductorTopologyNode",
        "InterconnectionComponent",
    }

    assert CoreGNodeRole.default() == CoreGNodeRole.Other
