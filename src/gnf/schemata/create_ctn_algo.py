"""create.ctn.algo.001 type"""

import json
from typing import List
from typing import NamedTuple

import gnf.property_format as property_format
from gnf.errors import SchemaError


class CreateCtnAlgo(NamedTuple):
    ChildAliasList: List[str]
    FromGNodeAlias: str  #
    MicroLat: int  #
    MicroLon: int  #
    CtnGNodeAlias: str  #
    GNodeRegistryAddr: str  #
    FromGNodeInstanceId: str  #
    TypeName: str = "create.ctn.algo.001"

    def as_type(self) -> str:
        return json.dumps(self.asdict())

    def asdict(self):
        d = self._asdict()
        return d

    def derived_errors(self) -> List[str]:
        errors = []
        if not isinstance(self.ChildAliasList, list):
            errors.append(f"ChildAliasList {self.ChildAliasList} must have type list.")
        else:
            for elt in self.ChildAliasList:
                if not isinstance(elt, str):
                    errors.append(f"elt {elt} of ChildAliasList must have type str.")
                try:
                    property_format.check_is_lrd_alias_format(elt)
                except ValueError as e:
                    errors.append(
                        f"elt {elt} of ChildAliasList must have format LrdAliasFormat; {e}"
                    )
        if not isinstance(self.FromGNodeAlias, str):
            errors.append(f"FromGNodeAlias {self.FromGNodeAlias} must have type str.")
        try:
            property_format.check_is_lrd_alias_format(self.FromGNodeAlias)
        except ValueError as e:
            errors.append(
                f"FromGNodeAlias {self.FromGNodeAlias}"
                " must have format LrdAliasFormat: {e}"
            )
        if not isinstance(self.MicroLat, int):
            errors.append(f"MicroLat {self.MicroLat} must have type int.")
        if not isinstance(self.MicroLon, int):
            errors.append(f"MicroLon {self.MicroLon} must have type int.")
        if not isinstance(self.CtnGNodeAlias, str):
            errors.append(f"CtnGNodeAlias {self.CtnGNodeAlias} must have type str.")
        try:
            property_format.check_is_lrd_alias_format(self.CtnGNodeAlias)
        except ValueError as e:
            errors.append(
                f"CtnGNodeAlias {self.CtnGNodeAlias}"
                " must have format LrdAliasFormat: {e}"
            )
        if not isinstance(self.GNodeRegistryAddr, str):
            errors.append(
                f"GNodeRegistryAddr {self.GNodeRegistryAddr} must have type str."
            )
        try:
            property_format.check_is_algo_address_string_format(self.GNodeRegistryAddr)
        except ValueError as e:
            errors.append(
                f"GNodeRegistryAddr {self.GNodeRegistryAddr}"
                " must have format AlgoAddressStringFormat: {e}"
            )
        if not isinstance(self.FromGNodeInstanceId, str):
            errors.append(
                f"FromGNodeInstanceId {self.FromGNodeInstanceId} must have type str."
            )
        try:
            property_format.check_is_uuid_canonical_textual(self.FromGNodeInstanceId)
        except ValueError as e:
            errors.append(
                f"FromGNodeInstanceId {self.FromGNodeInstanceId}"
                " must have format UuidCanonicalTextual: {e}"
            )
        if self.TypeName != "create.ctn.algo.001":
            errors.append(
                f"Type requires TypeName of create.ctn.algo.001, not {self.TypeName}."
            )

        return errors

    def check_for_errors(self):
        if self.derived_errors() == []:
            errors = self.hand_coded_errors()
        else:
            errors = self.derived_errors()
        if len(errors) > 0:
            raise SchemaError(f"Errors making create.ctn.algo.001 for {self}: {errors}")

    def __repr__(self):
        return "CreateCtnAlgo"

    def hand_coded_errors(self):
        return []


class CreateCtnAlgo_Maker:
    type_name = "create.ctn.algo.001"

    def __init__(
        self,
        child_alias_list: List[str],
        from_g_node_alias: str,
        micro_lat: int,
        micro_lon: int,
        ctn_g_node_alias: str,
        g_node_registry_addr: str,
        from_g_node_instance_id: str,
    ):

        gw_tuple = CreateCtnAlgo(
            ChildAliasList=child_alias_list,
            FromGNodeAlias=from_g_node_alias,
            MicroLat=micro_lat,
            MicroLon=micro_lon,
            CtnGNodeAlias=ctn_g_node_alias,
            GNodeRegistryAddr=g_node_registry_addr,
            FromGNodeInstanceId=from_g_node_instance_id,
            #
        )
        gw_tuple.check_for_errors()
        self.tuple = gw_tuple

    @classmethod
    def tuple_to_type(cls, tuple: CreateCtnAlgo) -> str:
        tuple.check_for_errors()
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> CreateCtnAlgo:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> CreateCtnAlgo:
        new_d = {}
        for key in d.keys():
            new_d[key] = d[key]
        if "TypeName" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TypeName")
        if "ChildAliasList" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing ChildAliasList")
        if "FromGNodeAlias" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing FromGNodeAlias")
        if "MicroLat" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing MicroLat")
        if "MicroLon" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing MicroLon")
        if "CtnGNodeAlias" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing CtnGNodeAlias")
        if "GNodeRegistryAddr" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing GNodeRegistryAddr")
        if "FromGNodeInstanceId" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing FromGNodeInstanceId")

        gw_tuple = CreateCtnAlgo(
            TypeName=new_d["TypeName"],
            ChildAliasList=new_d["ChildAliasList"],
            FromGNodeAlias=new_d["FromGNodeAlias"],
            MicroLat=new_d["MicroLat"],
            MicroLon=new_d["MicroLon"],
            CtnGNodeAlias=new_d["CtnGNodeAlias"],
            GNodeRegistryAddr=new_d["GNodeRegistryAddr"],
            FromGNodeInstanceId=new_d["FromGNodeInstanceId"],
            #
        )
        gw_tuple.check_for_errors()
        return gw_tuple
