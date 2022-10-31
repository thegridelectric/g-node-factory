"""Tests for schema enum core.g.node.role"""
from gnf.enums import CoreGNodeRole


def test_core_g_node_role():

    assert set(CoreGNodeRole.values()) == {
        "ConductorTopologyNode",
        "AtomicTNode",
        "TerminalAsset",
        "InterconnectionComponent",
        "Other",
        "MarketMaker",
        "AtomicMeteringNode",
    }

    assert CoreGNodeRole.default() == CoreGNodeRole.Other
