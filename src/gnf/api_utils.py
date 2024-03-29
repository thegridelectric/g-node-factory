import os
from typing import Dict
from typing import Optional

import django
import dotenv
import gridworks.algo_utils as algo_utils
from algosdk import encoding
from algosdk.future.transaction import MultisigTransaction
from algosdk.v2client.algod import AlgodClient

import gnf.config as config
import gnf.property_format as property_format
from gnf.errors import SchemaError
from gnf.utils import camel_to_snake


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gnf.django_related.settings")
django.setup()
from gnf.django_related.models import BaseGNodeDb
from gnf.types import BaseGNodeGt_Maker


def dict_to_db(d: Dict) -> BaseGNodeDb:
    gtuple = BaseGNodeGt_Maker.dict_to_tuple(d)
    d = {camel_to_snake(k): v for k, v in d.items()}
    d["status_value"] = gtuple.Status.value
    d["role_value"] = gtuple.Role.value
    del d["status_gt_enum_symbol"]
    del d["role_gt_enum_symbol"]
    del d["type_name"]
    del d["version"]
    gndb = BaseGNodeDb.objects.create(**d)
    return gndb


def get_discoverer_account_with_admin(
    discoverer_addr: str,
) -> Optional[algo_utils.MultisigAccount]:
    """2-sig multi [discoverer, admin]"""
    try:
        property_format.check_is_algo_address_string_format(discoverer_addr)
    except SchemaError:
        raise SchemaError(
            f"getValidatorAccountWithAdmin called with validatorAddr not of AlgoAddressStringFormat: \n{discoverer_addr}"
        )

    return algo_utils.MultisigAccount(
        version=1,
        threshold=2,
        addresses=[discoverer_addr, config.Public().gnf_admin_addr],
    )


def get_validator_account_with_admin(
    validatorAddr: str,
) -> Optional[algo_utils.MultisigAccount]:
    """2-sig multi [admin, validator]"""
    try:
        property_format.check_is_algo_address_string_format(validatorAddr)
    except SchemaError:
        raise SchemaError(
            f"getValidatorAccountWithAdmin called with validatorAddr not of AlgoAddressStringFormat: \n{validatorAddr}"
        )

    return algo_utils.MultisigAccount(
        version=1,
        threshold=2,
        addresses=[config.Public().gnf_admin_addr, validatorAddr],
    )


def check_validator_multi_has_enough_algos(validator_addr: str):
    """Raises exception if the 2-sig multi [gnf admin, validator] account does not have
    ta_validator_funding_threshold_algos
    (set publicly by the Gnf and available in config.Algo())

    Args:
        validatorAddr: the public address of the pending validator

    Raises:
        SchemaError if joint account does not have ta_validator_funding_threshold_algos.

    """
    try:
        property_format.check_is_algo_address_string_format(validator_addr)
    except SchemaError:
        raise Exception(
            f"called with validatorAddr not of AlgoAddressStringFormat: \n{validator_addr}"
        )
    min_algos = config.Public().ta_validator_funding_threshold_algos
    multi: algo_utils.MultisigAccount = get_validator_account_with_admin(validator_addr)
    if algo_utils.algos(multi.addr) is None:
        raise SchemaError(
            f"multi  ..{multi.addr[-6:]}  for validator ..{validator_addr[-6:]} is unfunded. Requires {min_algos} Algos."
        )
    if algo_utils.algos(multi.addr) < min_algos:
        raise SchemaError(
            f"multi  ..{multi.addr[-6:]}  for validator ..{validator_addr[-6:]} has {algo_utils.algos(multi.addr)} Algos. Requires {min_algos} Algos. "
        )


def check_mtx_subsig(mtx: MultisigTransaction, signer_addr):
    """Throws a SchemaError if the signerAddr is not a signer for mtx or did not sign.
    TODO: add error if the signature does not match the txn.
    """
    signer_pk = encoding.decode_address(signer_addr)
    sig_by_public_key = {}
    for subsig in mtx.multisig.subsigs:
        sig_by_public_key[subsig.public_key] = subsig.signature

    if not signer_pk in sig_by_public_key.keys():
        raise SchemaError(
            f"signerAddr ..{signer_addr[-6:]} not a signer for multisig!!"
        )
    if sig_by_public_key[signer_pk] == None:
        raise SchemaError(f"signerAddr ..{signer_addr[-6:]} did not sign!")
    # TODO: check that the signature is for THIS transaction


def get_validator_cert_idx(validator_addr: str) -> Optional[int]:
    """Looks for an asset in the validatorMsig account that is a
    validator certificate (based on unit name).

    Args:
        validatorAddr: the public address of the validator (NOT the multi)

    Returns:
        Optional[int]: returns None if no validatorCert is found, otherwise
        the asset index of the cert
    """
    multi: algo_utils.MultisigAccount = get_validator_account_with_admin(validator_addr)
    settings = config.VanillaSettings(_env_file=dotenv.find_dotenv())
    client: AlgodClient = AlgodClient(
        settings.algo_api_secrets.algod_token.get_secret_value(),
        settings.public.algod_address,
    )
    try:
        created_assets = client.account_info(multi.addr)["created-assets"]
    except:
        return None
    certs = list(filter(lambda x: x["params"]["unit-name"] == "VLDTR", created_assets))
    if len(certs) == 0:
        return None
    else:
        return certs[0]["index"]


def is_validator(acct_addr: str) -> bool:
    """
    A validator is a tuple of 3 things:
        - single owner funded Algorand account belonging to validator
        - funded, joint, two-sig-required account with gnf admin
        - Validator token owned by joint account


    Returns:
        True if the accountAddress is a validator
        False otherwise

    """
    settings = config.VanillaSettings(_env_file=dotenv.find_dotenv())
    client: AlgodClient = AlgodClient(
        settings.algo_api_secrets.algod_token.get_secret_value(),
        settings.public.algod_address,
    )
    cert_asset_idx = get_validator_cert_idx(acct_addr)
    if cert_asset_idx is None:
        return False
    else:
        asset_dicts = client.account_info(acct_addr)["assets"]
        opt_in_ids = list(map(lambda x: x["asset-id"], asset_dicts))
        if cert_asset_idx not in opt_in_ids:
            return False
        our_dict = list(filter(lambda x: x["asset-id"] == cert_asset_idx, asset_dicts))[
            0
        ]
        if our_dict["amount"] == 0:
            return False
        return True


def get_tatrading_rights_idx(terminal_asset_alias: str) -> Optional[int]:
    settings = config.VanillaSettings(_env_file=dotenv.find_dotenv())
    client: AlgodClient = AlgodClient(
        settings.algo_api_secrets.algod_token.get_secret_value(),
        settings.public.algod_address,
    )
    try:
        created_assets = client.account_info(settings.public.gnf_admin_addr)[
            "created-assets"
        ]
    except:
        return None
    ta_trading_rights = list(
        filter(lambda x: x["params"]["unit-name"] == "TATRADE", created_assets)
    )
    this_ta_trading_rights = list(
        filter(lambda x: x["params"]["name"] == terminal_asset_alias, ta_trading_rights)
    )
    if len(this_ta_trading_rights) == 0:
        return None
    else:
        return this_ta_trading_rights[0]["index"]


def get_tadeed_idx(terminal_asset_alias, validator_addr: str) -> Optional[int]:
    """Looks for an asset created in the 2-sig [Gnf Admin, validator_addr] account
     that is a tadeed for terminal_asset_alias.

    Args:
        terminal_asset_alias (str): the alias of the Terminal Asset
        validator_addr (str):

    Returns:
        Optional[int]: returns None if no validatorCert is found, otherwise
        the asset index of the cert
    """
    settings = config.VanillaSettings(_env_file=dotenv.find_dotenv())
    client: AlgodClient = AlgodClient(
        settings.algo_api_secrets.algod_token.get_secret_value(),
        settings.public.algod_address,
    )

    multi: algo_utils.MultisigAccount = get_validator_account_with_admin(validator_addr)
    try:
        created_assets = client.account_info(multi.addr)["created-assets"]
    except:
        return None
    ta_deeds = list(
        filter(lambda x: x["params"]["unit-name"] == "TADEED", created_assets)
    )
    this_ta_deed = list(
        filter(lambda x: x["params"]["name"] == terminal_asset_alias, ta_deeds)
    )
    if len(this_ta_deed) == 0:
        return None
    else:
        return this_ta_deed[0]["index"]


def is_ta_deed(asset_idx: int) -> bool:
    settings = config.VanillaSettings(_env_file=dotenv.find_dotenv())
    client: AlgodClient = AlgodClient(
        settings.algo_api_secrets.algod_token.get_secret_value(),
        settings.public.algod_address,
    )
    try:
        info = client.asset_info(asset_idx)
    except:
        return False
    try:
        unit_name = info["params"]["unit-name"]
    except:
        return False
    if unit_name == "TADEED":
        return True
    return False


def alias_from_deed_idx(asset_idx: int) -> Optional[str]:
    if not is_ta_deed(asset_idx):
        return None
    settings = config.VanillaSettings(_env_file=dotenv.find_dotenv())
    client: AlgodClient = AlgodClient(
        settings.algo_api_secrets.algod_token.get_secret_value(),
        settings.public.algod_address,
    )
    info = client.asset_info(asset_idx)
    return info["params"]["name"]
