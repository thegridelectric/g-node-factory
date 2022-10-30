"""create.terminalasset.algo.010 type"""

import json
from typing import NamedTuple

import gnf.property_format as property_format
from gnf.errors import SchemaError


class CreateTerminalassetAlgo(NamedTuple):
    TaGNodeAlias: str  #
    MicroLon: int  #
    ValidatorAddr: str  #
    TaOwnerAddr: str  #
    MicroLat: int  #
    GNodeRegistryAddr: str  #
    FromGNodeInstanceId: str  #
    FromGNodeAlias: str  #
    TypeName: str = "create.terminalasset.algo.010"

    def as_type(self) -> str:
        return json.dumps(self.asdict())

    def asdict(self):
        d = self._asdict()
        return d

    def derived_errors(self) -> List[str]:
        errors = []
        if not isinstance(self.TaGNodeAlias, str):
            errors.append(f"TaGNodeAlias {self.TaGNodeAlias} must have type str.")
        try:
            property_format.check_is_lrd_alias_format(self.TaGNodeAlias)
        except SchemaError as e:
            errors.append(
                f"TaGNodeAlias {self.TaGNodeAlias}"
                " must have format LrdAliasFormat: {e}"
            )
        if not isinstance(self.MicroLon, int):
            errors.append(f"MicroLon {self.MicroLon} must have type int.")
        if not isinstance(self.ValidatorAddr, str):
            errors.append(f"ValidatorAddr {self.ValidatorAddr} must have type str.")
        try:
            property_format.check_is_algo_address_string_format(self.ValidatorAddr)
        except SchemaError as e:
            errors.append(
                f"ValidatorAddr {self.ValidatorAddr}"
                " must have format AlgoAddressStringFormat: {e}"
            )
        if not isinstance(self.TaOwnerAddr, str):
            errors.append(f"TaOwnerAddr {self.TaOwnerAddr} must have type str.")
        try:
            property_format.check_is_algo_address_string_format(self.TaOwnerAddr)
        except SchemaError as e:
            errors.append(
                f"TaOwnerAddr {self.TaOwnerAddr}"
                " must have format AlgoAddressStringFormat: {e}"
            )
        if not isinstance(self.MicroLat, int):
            errors.append(f"MicroLat {self.MicroLat} must have type int.")
        if not isinstance(self.GNodeRegistryAddr, str):
            errors.append(
                f"GNodeRegistryAddr {self.GNodeRegistryAddr} must have type str."
            )
        try:
            property_format.check_is_algo_address_string_format(self.GNodeRegistryAddr)
        except SchemaError as e:
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
        except SchemaError as e:
            errors.append(
                f"FromGNodeInstanceId {self.FromGNodeInstanceId}"
                " must have format UuidCanonicalTextual: {e}"
            )
        if not isinstance(self.FromGNodeAlias, str):
            errors.append(f"FromGNodeAlias {self.FromGNodeAlias} must have type str.")
        try:
            property_format.check_is_lrd_alias_format(self.FromGNodeAlias)
        except SchemaError as e:
            errors.append(
                f"FromGNodeAlias {self.FromGNodeAlias}"
                " must have format LrdAliasFormat: {e}"
            )
        if self.TypeName != "create.terminalasset.algo.010":
            errors.append(
                f"Type requires TypeName of create.terminalasset.algo.010, not {self.TypeName}."
            )

        return errors

    def check_for_errors(self):
        if self.derived_errors() == []:
            errors = self.hand_coded_errors()
        else:
            errors = self.derived_errors()
        if len(errors) > 0:
            raise SchemaError(
                f"Errors making create.terminalasset.algo.010 for {self}: {errors}"
            )

    def __repr__(self):
        return "CreateTerminalassetAlgo"

    def hand_coded_errors(self):
        return []


class CreateTerminalassetAlgo_Maker:
    type_name = "create.terminalasset.algo.010"

    def __init__(
        self,
        ta_g_node_alias: str,
        micro_lon: int,
        validator_addr: str,
        ta_owner_addr: str,
        micro_lat: int,
        g_node_registry_addr: str,
        from_g_node_instance_id: str,
        from_g_node_alias: str,
    ):

        gw_tuple = CreateTerminalassetAlgo(
            TaGNodeAlias=ta_g_node_alias,
            MicroLon=micro_lon,
            ValidatorAddr=validator_addr,
            TaOwnerAddr=ta_owner_addr,
            MicroLat=micro_lat,
            GNodeRegistryAddr=g_node_registry_addr,
            FromGNodeInstanceId=from_g_node_instance_id,
            FromGNodeAlias=from_g_node_alias,
            #
        )
        gw_tuple.check_for_errors()
        self.tuple = gw_tuple

    @classmethod
    def tuple_to_type(cls, tuple: CreateTerminalassetAlgo) -> str:
        tuple.check_for_errors()
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> CreateTerminalassetAlgo:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> CreateTerminalassetAlgo:
        new_d = {}
        for key in d.keys():
            new_d[key] = d[key]
        if "TypeName" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TypeName")
        if "TaGNodeAlias" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TaGNodeAlias")
        if "MicroLon" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing MicroLon")
        if "ValidatorAddr" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing ValidatorAddr")
        if "TaOwnerAddr" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TaOwnerAddr")
        if "MicroLat" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing MicroLat")
        if "GNodeRegistryAddr" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing GNodeRegistryAddr")
        if "FromGNodeInstanceId" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing FromGNodeInstanceId")
        if "FromGNodeAlias" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing FromGNodeAlias")

        gw_tuple = CreateTerminalassetAlgo(
            TypeName=new_d["TypeName"],
            TaGNodeAlias=new_d["TaGNodeAlias"],
            MicroLon=new_d["MicroLon"],
            ValidatorAddr=new_d["ValidatorAddr"],
            TaOwnerAddr=new_d["TaOwnerAddr"],
            MicroLat=new_d["MicroLat"],
            GNodeRegistryAddr=new_d["GNodeRegistryAddr"],
            FromGNodeInstanceId=new_d["FromGNodeInstanceId"],
            FromGNodeAlias=new_d["FromGNodeAlias"],
            #
        )
        gw_tuple.check_for_errors()
        return gw_tuple
