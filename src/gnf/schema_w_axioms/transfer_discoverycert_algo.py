"""transfer.discoverycert.algo.001 type"""

import json
from typing import List
from typing import NamedTuple

import gnf.property_format as property_format
from gnf.errors import SchemaError


class TransferDiscoverycertAlgo(NamedTuple):
    GNodeAlias: str  #
    DiscovererAddr: str  #
    TypeName: str = "transfer.discoverycert.algo.001"

    def as_type(self) -> str:
        return json.dumps(self.asdict())

    def asdict(self):
        d = self._asdict()
        return d

    def derived_errors(self) -> List[str]:
        errors = []
        if not isinstance(self.GNodeAlias, str):
            errors.append(f"GNodeAlias {self.GNodeAlias} must have type str.")
        try:
            property_format.check_is_lrd_alias_format(self.GNodeAlias)
        except ValueError as e:
            errors.append(
                f"GNodeAlias {self.GNodeAlias}" " must have format LrdAliasFormat: {e}"
            )
        if not isinstance(self.DiscovererAddr, str):
            errors.append(f"DiscovererAddr {self.DiscovererAddr} must have type str.")
        try:
            property_format.check_is_algo_address_string_format(self.DiscovererAddr)
        except ValueError as e:
            errors.append(
                f"DiscovererAddr {self.DiscovererAddr}"
                " must have format AlgoAddressStringFormat: {e}"
            )
        if self.TypeName != "transfer.discoverycert.algo.001":
            errors.append(
                f"Type requires TypeName of transfer.discoverycert.algo.001, not {self.TypeName}."
            )

        return errors

    def check_for_errors(self):
        if self.derived_errors() == []:
            errors = self.hand_coded_errors()
        else:
            errors = self.derived_errors()
        if len(errors) > 0:
            raise SchemaError(
                f"Errors making transfer.discoverycert.algo.001 for {self}: {errors}"
            )

    def __repr__(self):
        return "TransferDiscoverycertAlgo"

    def hand_coded_errors(self):
        return []


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
