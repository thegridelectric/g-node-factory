"""Tests for scehma enum core.g.node.role.100"""

import pytest
from enums.core_g_node_role_map import CoreGNodeRole
from enums.core_g_node_role_map import CoreGNodeRoleMap as Map
from enums.core_g_node_role_map import CoreGNodeRoleSchemaEnum
from errors import SchemaError


def test_component_category():

    assert set(CoreGNodeRole.values()) == {
        "ConductorTopologyNode",
        "AtomicTNode",
        "TerminalAsset",
        "InterconnectionComponent",
        "Other",
        "MarketMaker",
        "AtomicMeteringNode",
    }

    assert set(CoreGNodeRoleSchemaEnum.symbols) == {
        "4502e355",
        "d9823442",
        "0f8872f7",
        "d67e564e",
        "6b58d301",
        "86f21dd2",
        "9521af06",
    }

    assert len(CoreGNodeRole.values()) == len(CoreGNodeRoleSchemaEnum.symbols)

    assert Map.type_to_local("4502e355") == CoreGNodeRole.CONDUCTOR_TOPOLOGY_NODE
    assert Map.type_to_local("d9823442") == CoreGNodeRole.ATOMIC_T_NODE
    assert Map.type_to_local("0f8872f7") == CoreGNodeRole.TERMINAL_ASSET
    assert Map.type_to_local("d67e564e") == CoreGNodeRole.INTERCONNECTION_COMPONENT
    assert Map.type_to_local("6b58d301") == CoreGNodeRole.OTHER
    assert Map.type_to_local("86f21dd2") == CoreGNodeRole.MARKET_MAKER
    assert Map.type_to_local("9521af06") == CoreGNodeRole.ATOMIC_METERING_NODE

    with pytest.raises(SchemaError):
        Map.type_to_local("aaa")

    with pytest.raises(SchemaError):
        Map.local_to_type("Load")

    for symbol in CoreGNodeRoleSchemaEnum.symbols:
        assert Map.local_to_type(Map.type_to_local(symbol)) == symbol
