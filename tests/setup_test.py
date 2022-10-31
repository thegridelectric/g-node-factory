from algosdk.kmd import KMDClient
from algosdk.v2client.algod import AlgodClient

import gnf.algo_utils as algo_utils
import gnf.config as config


def test_get_algod_client():
    client = algo_utils.get_algod_client(settings_algo=config.Algo())
    assert isinstance(client, AlgodClient)

    response = client.health()
    assert response is None


def test_get_kmd_client():
    client = algo_utils.get_kmd_client(settings_algo=config.Algo())
    assert isinstance(client, KMDClient)

    response = client.versions()
    expected = ["v1"]
    assert response == expected
