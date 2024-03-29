"""Tests for schema enum algo.cert.type.000"""
from gnf.enums import AlgoCertType


def test_algo_cert_type() -> None:
    assert set(AlgoCertType.values()) == {
        "ASA",
        "SmartSig",
    }

    assert AlgoCertType.default() == AlgoCertType.ASA
