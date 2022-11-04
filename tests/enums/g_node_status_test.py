"""Tests for schema enum g.node.status.100"""
from gnf.enums import GNodeStatus


def test_g_node_status():

    assert set(GNodeStatus.values()) == {
        "Unknown",
        "Active",
        "Pending",
        "PermanentlyDeactivated",
        "Suspended",
    }

    assert GNodeStatus.default() == GNodeStatus.Unknown
