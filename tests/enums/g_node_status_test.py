"""Tests for scehma enum g.node.status"""

from gnf.enums import GNodeStatus


def test_g_node_status():

    assert set(GNodeStatus.values()) == {
        "PermanentlyDeactivated",
        "Pending",
        "Active",
        "Suspended",
    }

    assert GNodeStatus.default() == GNodeStatus.Active
