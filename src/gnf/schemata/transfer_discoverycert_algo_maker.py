"""Makes transfer.discoverycert.algo.001 type"""
import json

from errors import SchemaError
from schemata.transfer_discoverycert_algo import TransferDiscoverycertAlgo


class TransferDiscoverycertAlgo_Maker:
    type_name = "transfer.discoverycert.algo.001"

    def __init__(self, g_node_alias: str, discoverer_addr: str):

        gw_tuple = TransferDiscoverycertAlgo(
            GNodeAlias=g_node_alias,
            DiscovererAddr=discoverer_addr,
            #
        )
        gw_tuple.check_for_errors()
        self.tuple = gw_tuple

    @classmethod
    def tuple_to_type(cls, tuple: TransferDiscoverycertAlgo) -> str:
        tuple.check_for_errors()
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> TransferDiscoverycertAlgo:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> TransferDiscoverycertAlgo:
        new_d = {}
        for key in d.keys():
            new_d[key] = d[key]
        if "TypeName" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TypeName")
        if "GNodeAlias" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing GNodeAlias")
        if "DiscovererAddr" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing DiscovererAddr")

        gw_tuple = TransferDiscoverycertAlgo(
            TypeName=new_d["TypeName"],
            GNodeAlias=new_d["GNodeAlias"],
            DiscovererAddr=new_d["DiscovererAddr"],
            #
        )
        gw_tuple.check_for_errors()
        return gw_tuple
