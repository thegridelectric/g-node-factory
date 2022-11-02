"""Axioms for create.tadeed.algo.010"""
from typing import List
from typing import OrderedDict

from algosdk import encoding
from algosdk.future import transaction

import gnf.algo_utils as algo_utils
import gnf.api_utils as api_utils
import gnf.config as config
import gnf.property_format as property_format
from gnf.errors import SchemaError
from gnf.schemata import CreateTadeedAlgo


def create_tadeed_algo_axiom_errors(gtuple: CreateTadeedAlgo):
    errors = []
    errors += _axiom_1_errors(gtuple)
    if len(errors) != 0:
        return errors
    errors += _axiom_2_errors(gtuple)
    if len(errors) != 0:
        return errors
    errors += _axiom_3_errors(gtuple)
    errors += _axiom_4_errors(gtuple)
    errors += _axiom_5_errors(gtuple)
    errors += _axiom_6_errors(gtuple)
    return errors


def _axiom_1_errors(gtuple: CreateTadeedAlgo) -> List[str]:
    """Axiom 1: Decoded HalfSignedDeedCreationMtx must have type MultisigTransaction"""
    errors = []
    mtx = encoding.future_msgpack_decode(gtuple.HalfSignedDeedCreationMtx)
    if not isinstance(mtx, transaction.MultisigTransaction):
        errors.append(
            "Axiom 1: Decoded HalfSignedDeedCreationMtx must have type MultisigTransaction,"
            f" got {type(mtx)}"
        )
    return errors


def _axiom_2_errors(gtuple: CreateTadeedAlgo) -> List[str]:
    """Axiom 2: The HalfSignedDeedCreationMtx.txn must have type AssetConfigTxn"""
    errors = []
    mtx = encoding.future_msgpack_decode(gtuple.HalfSignedDeedCreationMtx)
    txn = mtx.transaction
    if not isinstance(txn, transaction.AssetConfigTxn):
        errors.append(
            f"Axiom 2: The HalfSignedDeedCreationMtx.txn must have type AssetConfigTxn, got {type(txn)}"
        )
    return errors


def _axiom_3_errors(gtuple: CreateTadeedAlgo) -> List[str]:
    """Axiom 3: The MultiSig must be the 2-sig multi [Gnf Admin, gtuple.ValidatorAddr]"""
    errors = []
    mtx = encoding.future_msgpack_decode(gtuple.HalfSignedDeedCreationMtx)
    msig = mtx.multisig
    gnf_admin_addr = config.Algo().gnf_admin_addr
    multi = algo_utils.MultisigAccount(
        version=1,
        threshold=2,
        addresses=[gnf_admin_addr, gtuple.ValidatorAddr],
    )
    if msig.address() != multi.addr:
        errors.append(
            "Axiom 3: The MultiSig must be the 2-sig multi"
            f"[Gnf Admin, gtuple.ValidatorAddr].\nGot ..{msig.address()[-6:]}.\nExpected ..{multi.addr[-6:]}"
        )

    return errors


def _axiom_4_errors(gtuple: CreateTadeedAlgo) -> List[str]:
    """Axiom 4: For the asset getting created: total = 1, unit_name=TADEED, asset_name
    must be <= 32 char, manager is Gnf Admin."""
    errors = []
    mtx = encoding.future_msgpack_decode(gtuple.HalfSignedDeedCreationMtx)
    txn = mtx.transaction
    gnf_admin_addr = config.Algo().gnf_admin_addr
    od = txn.dictify()
    try:
        apar: OrderedDict = od["apar"]
    except:
        raise Exception(
            "Unexpected error. AssetCreationTxn.dictify() did not have 'apar' key"
        )
    if apar["t"] != 1:
        errors.append(f"total must be 1, not {apar['t']}. ")
    if apar["un"] != "TADEED":
        errors.append(f"not a TaDeed - unit_name must be TADEED, not {apar['un']}. ")
    if apar["m"] != encoding.decode_address(gnf_admin_addr):
        errors.append(
            f"Manager must be GnfAdmin ..{gnf_admin_addr[-6:]}, got ..{encoding.encode_address(apar['m'])[-6:]}. "
        )
    if len(apar["an"]) > 32:
        errors.append(f"asset name must be <= 32 char. Got {len(apar['an'])} ")
    return errors


def _axiom_5_errors(gtuple: CreateTadeedAlgo) -> List[str]:
    """The asset name must have valid GNodeAlias format, with the world_alias (first
    word of asset name matching the universe (e.g. dev universe -> world starts with `d`).
    Additionally, the final word of the asset name must be `ta`"""
    errors = []
    mtx = encoding.future_msgpack_decode(gtuple.HalfSignedDeedCreationMtx)
    txn = mtx.transaction
    asset_name = txn.dictify()["apar"]["an"]

    try:
        property_format.check_is_lrd_alias_format(asset_name)
    except SchemaError as e:
        errors.append(f"The asset name must have valid GNode format: {e}")
    universe = config.Algo().universe
    try:
        property_format.check_world_alias_matches_universe(
            g_node_alias=asset_name, universe=universe
        )
    except SchemaError as e:
        errors.append(
            f"The asset name must be a potential GNodeAlias in a {universe} universe. {e}"
        )
    words = asset_name.split(".")
    if words[-1] != "ta":
        errors.append(f"TerminalAsset aliases must end in ta. Got {asset_name}")
    return errors


def _axiom_6_errors(gtuple: CreateTadeedAlgo) -> List[str]:
    """Axiom 6: ValidatorAddr must have signed the mtx, and the signature must match the txn"""
    errors = []
    mtx = encoding.future_msgpack_decode(gtuple.HalfSignedDeedCreationMtx)
    try:
        api_utils.check_mtx_subsig(mtx, gtuple.ValidatorAddr)
    except SchemaError as e:
        errors.append(
            "Axiom 5: ValidatorAddr must have signed the mtx, and the signature must"
            f" match the txn: {e}"
        )
    return errors
