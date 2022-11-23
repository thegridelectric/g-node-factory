"""Tests for schema enum universe.type.000"""
from gnf.enums import UniverseType


def test_universe_type():

    assert set(UniverseType.values()) == {
        "Dev",
        "Hybrid",
    }

    assert UniverseType.default() == UniverseType.Dev
