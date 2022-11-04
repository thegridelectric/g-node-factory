"""Type initial.tadeed.algo.optin, version 000"""
import json
from typing import Dict
from typing import Literal

from pydantic import BaseModel

import gnf.property_format as property_format
from gnf.errors import SchemaError
from gnf.property_format import predicate_validator


class InitialTadeedAlgoOptin(BaseModel):
    TerminalAssetAlias: str  #
    TaOwnerAddr: str  #
    ValidatorAddr: str  #
    SignedInitialDaemonFundingTxn: str  #
    TypeName: Literal["initial.tadeed.algo.optin"] = "initial.tadeed.algo.optin"
    Version: str = "000"

    _validator_terminal_asset_alias = predicate_validator(
        "TerminalAssetAlias", property_format.is_lrd_alias_format
    )

    _validator_ta_owner_addr = predicate_validator(
        "TaOwnerAddr", property_format.is_algo_address_string_format
    )

    _validator_validator_addr = predicate_validator(
        "ValidatorAddr", property_format.is_algo_address_string_format
    )

    _validator_signed_initial_daemon_funding_txn = predicate_validator(
        "SignedInitialDaemonFundingTxn", property_format.is_algo_msg_pack_encoded
    )

    def as_dict(self) -> Dict:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class InitialTadeedAlgoOptin_Maker:
    type_name = "initial.tadeed.algo.optin"
    version = "000"

    def __init__(
        self,
        terminal_asset_alias: str,
        ta_owner_addr: str,
        validator_addr: str,
        signed_initial_daemon_funding_txn: str,
    ):

        self.tuple = InitialTadeedAlgoOptin(
            TerminalAssetAlias=terminal_asset_alias,
            TaOwnerAddr=ta_owner_addr,
            ValidatorAddr=validator_addr,
            SignedInitialDaemonFundingTxn=signed_initial_daemon_funding_txn,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: InitialTadeedAlgoOptin) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> InitialTadeedAlgoOptin:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> InitialTadeedAlgoOptin:
        d2 = dict(d)
        if "TerminalAssetAlias" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TerminalAssetAlias")
        if "TaOwnerAddr" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TaOwnerAddr")
        if "ValidatorAddr" not in d2.keys():
            raise SchemaError(f"dict {d2} missing ValidatorAddr")
        if "SignedInitialDaemonFundingTxn" not in d2.keys():
            raise SchemaError(f"dict {d2} missing SignedInitialDaemonFundingTxn")
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return InitialTadeedAlgoOptin(
            TerminalAssetAlias=d2["TerminalAssetAlias"],
            TaOwnerAddr=d2["TaOwnerAddr"],
            ValidatorAddr=d2["ValidatorAddr"],
            SignedInitialDaemonFundingTxn=d2["SignedInitialDaemonFundingTxn"],
            TypeName=d2["TypeName"],
            Version="000",
        )
