"""Tests for scehma enum g.node.status.100"""

import pytest
from enums.g_node_status_map import GNodeStatus
from enums.g_node_status_map import GNodeStatusMap as Map
from enums.g_node_status_map import GNodeStatusSchemaEnum
from errors import SchemaError


def test_component_category():

    assert set(GNodeStatus.values()) == {
        "PermanentlyDeactivated",
        "Pending",
        "Active",
        "Suspended",
    }

    assert set(GNodeStatusSchemaEnum.symbols) == {
        "839b38db",
        "153d3475",
        "8d92bebe",
        "f5831e1d",
    }

    assert len(GNodeStatus.values()) == len(GNodeStatusSchemaEnum.symbols)

    assert Map.type_to_local("839b38db") == GNodeStatus.PERMANENTLY_DEACTIVATED
    assert Map.type_to_local("153d3475") == GNodeStatus.PENDING
    assert Map.type_to_local("8d92bebe") == GNodeStatus.ACTIVE
    assert Map.type_to_local("f5831e1d") == GNodeStatus.SUSPENDED

    with pytest.raises(SchemaError):
        Map.type_to_local("aaa")

    with pytest.raises(SchemaError):
        Map.local_to_type("Load")

    for symbol in GNodeStatusSchemaEnum.symbols:
        assert Map.local_to_type(Map.type_to_local(symbol)) == symbol
