"""This is the FastAPI implementation of the GNodeFactory, where the topological
and geographical information about the electric grid is stored in a database accessible
only to this python GNodeFactory and its developer support.

For every TerminalAsset presented by the `GNodeRegistry` with the appropriate set of
information from two actors - the asset owner (`Holly Homeowner`) and the asset validator
(`Molly Metermaid`) this factory creates two non-fungible tokens and returns pointers
for them to the `GNodeRegistry`. The tokens created are
    1) the `taDeed` NFT which, like a house deed, provides proof of ownership of the
    TerminalAsset for the asset owner; and
    2) the `taTradingRights` NFT, which the asset owner is expected to provide to
    another entity (the algo account associated to an `AtomicTransactiveNode`) as
    part of a ServiceLevelAgreement contract with an organization who will trade
    in electricity markets with the terminalAsset on behalf of the asset Owner.

This implementation of the factory requires that all stakeholders trust GridWorks
and its devs to not adjust/change the topological data. Since this data is foundational
for proof-of-origin for exchanges of electrical resource (ancillary services, energy)
for money, this is not ideal. The second

The data  in the `baseGNode` table of this database implementation is designed to
be moved into a publicly accessible stateful smart contract. For this reason all
location-related data is hashed, even though it belongs to a private database.
"""
import json
import logging
import pprint
from typing import List
from typing import Optional

import requests
from algosdk import encoding
from algosdk.future import transaction
from algosdk.v2client.algod import AlgodClient
from asgiref.sync import sync_to_async

import gnf.algo_utils as algo_utils
import gnf.api_utils as api_utils
import gnf.config as config
import gnf.property_format as property_format
import gnf.utils as utils
from gnf.algo_utils import BasicAccount
from gnf.algo_utils import MultisigAccount
from gnf.algo_utils import PendingTxnResponse
from gnf.data_classes import BaseGNode
from gnf.django_related.models import BaseGNodeDb
from gnf.django_related.models import BaseGNodeHistory
from gnf.django_related.models import GpsPointDb
from gnf.enums import CoreGNodeRole
from gnf.enums import GNodeStatus
from gnf.errors import RegistryError
from gnf.schemata import BasegnodeGt
from gnf.schemata import BasegnodeGt_Maker
from gnf.schemata import DiscoverycertAlgoCreate
from gnf.schemata import InitialTadeedAlgoCreate
from gnf.schemata import InitialTadeedAlgoTransfer
from gnf.schemata import NewTadeedAlgoOptin
from gnf.schemata import NewTadeedAlgoOptin_Maker
from gnf.schemata import NewTadeedSend
from gnf.schemata import NewTadeedSend_Maker
from gnf.schemata import OldTadeedAlgoReturn
from gnf.schemata import OldTadeedAlgoReturn_Maker
from gnf.schemata import TavalidatorcertAlgoCreate
from gnf.schemata import TavalidatorcertAlgoTransfer
from gnf.utils import RestfulResponse


LOGGER = logging.getLogger(__name__)

#####################
# Messages received
#####################


def tavalidatorcert_algo_create_received(
    payload: TavalidatorcertAlgoCreate, settings: config.GnfSettings
) -> RestfulResponse:
    """Co-signs and submits an AssetCreateTxn for a  Validator Certificate NFT.

        Args:
            payload: TavalidatorcertAlgoCreate. The validation of the type guarantees
        that payload.HalfSignedCertCreationMtx is the encoding of a MultisigTransaction
        for the 2-sig multi [Gnf Admin, payload.ValidatorAddr] signed by the validator
        that creates an appropriately-formatted Validator Certificate.
            settings: GNodeFactory's GnfSettings

        Returns RestfulResponse
            HttpStatusCode 422 if the payload has the wrong type or if there is an error submitting the
        transaction to the blockchain.
            HttpStatusCode 200 if successful, with 'PayloadTypeName': 'int',
    │     and 'PayloadAsDict': {'Value': ValidatorCertIdx}
    """
    admin_sk = settings.admin_acct_sk.get_secret_value()

    client: AlgodClient = AlgodClient(
        settings.algo_api_secrets.algod_token.get_secret_value(),
        settings.public.algod_address,
    )
    if not isinstance(payload, TavalidatorcertAlgoCreate):
        note = f"payload must be type TavalidatorcertAlgoCreate, got {type(payload)}. Ignoring!"
        r = RestfulResponse(
            Note=note,
            HttpStatusCode=422,
        )
        return r

    mtx = encoding.future_msgpack_decode(payload.HalfSignedCertCreationMtx)
    mtx.sign(admin_sk)
    try:
        response: PendingTxnResponse = algo_utils.send_signed_mtx(
            client=client, mtx=mtx
        )
    except Exception as e:
        note = f"Tried to sign transaction but there was an error.\n {e}"
        r = RestfulResponse(Note=note, HttpStatusCode=422)
        return r

    validator_cert_idx = response.asset_idx
    note = (
        f"ValidatorCert for ..{payload.ValidatorAddr[-6:]} created, asset_idx"
        f" {validator_cert_idx} \n tx_id {response.tx_id}"
    )
    r = RestfulResponse(
        Note=note, PayloadTypeName="int", PayloadAsDict={"Value": validator_cert_idx}
    )

    return r


def tavalidatorcert_algo_transfer_received(
    payload: TavalidatorcertAlgoTransfer, settings: config.GnfSettings
) -> RestfulResponse:
    """Signs and submits an AssetTransferTxn that sends a Validator Certificate
    to the payload.ValidatorAddr

    Args:
        payload: TavalidatorcertAlgoTransfer. The validation of the type guarantees
    that payload.HalfSignedCertTransferMtx is the encoding of a MultisigTransaction
    for the 2-sig multi [Gnf Admin, payload.ValidatorAddr] signed by the validator
    that transfers an appropriately-formatted Validator Certificate to the
    payload.ValidatorAddr. It also guarantees that the multi account is sufficiently
    funded.
        settings: GNodeFactory's GnfSettings

    Returns RestfulResponse:
        - HttpStatusCode 422 if the payload has the wrong type or if there is an error submitting the
    transaction to the blockchain.
        - HttpStatusCode 200 if successful, note has blockchain transaction id
    """
    admin_sk = settings.admin_acct_sk.get_secret_value()
    client: AlgodClient = AlgodClient(
        settings.algo_api_secrets.algod_token.get_secret_value(),
        settings.public.algod_address,
    )
    if not isinstance(payload, TavalidatorcertAlgoTransfer):
        note = f"payload must be type TavalidatorcertAlgoTransfer, got {type(payload)}. Ignoring!"
        r = RestfulResponse(Note=note, HttpStatusCode=422)
        return r

    mtx = encoding.future_msgpack_decode(payload.HalfSignedCertTransferMtx)
    mtx.sign(admin_sk)
    try:
        response: PendingTxnResponse = algo_utils.send_signed_mtx(
            client=client, mtx=mtx
        )
    except Exception as e:
        note = f"Tried to sign transaction but there was an error.\n {e}"
        r = RestfulResponse(Note=note, HttpStatusCode=422)
        return r
    note = f"ValidatorCert for ..{payload.ValidatorAddr[-6:]} transferred\n txId {response.tx_id}"
    r = RestfulResponse(Note=note)
    return r


async def initial_tadeed_algo_transfer_received(
    payload: InitialTadeedAlgoTransfer, settings: config.GnfSettings
) -> RestfulResponse:
    """
        - Checks  consistency for the GNodeAlias in the deed:
            - in the BaseGNodeDb, there is a BaseGNode gn with this alias
            - gn.role = TerminalAsset
            - gn.status = Pending
            - gn.lat and gn.lon exist
            - gn.ownership_deed_nft_id does not exist
            - gn.ownership_deed_nft_creator_addr exists and matches
            2-sig [GnfAdmin, payload.ValidatorAddr]

        - Sends TaDeed to the TaDaemon.
        - On confirmation, updates the GNodeDb gn:
            - gn.ownership_deed_nft_id = ta_asset_id
            - gn.status_value = Active.value
            - gn parent (the AtomicMeteringNode) status = Active.value
        - Sends a StatusBaseGgnodeAlgo to the correct GNodeRegistry ,
        identified by gn.g_node_registry_addr. Status.TopGNodeAlias = gn parent
        - Returns that StatusBaseGgnodeAlgo payload

    Args:
        payload: TavalidatorcertAlgoTransfer. The validation of the type guarantees
    that payload.HalfSignedCertTransferMtx is the encoding of a MultisigTransaction
    for the 1-sig multi [Gnf Admin, payload.ValidatorAddr] signed by the validator
    that transfers an appropriately-formatted Validator Certificate to the
    payload.ValidatorAddr. It also guarantees that the multi account is sufficiently
    funded and opted in.

    Returns RestfulResponse:
        - None if transferring deed does not happen.
        - BaseGnodeGt for the TerminalAssetotherwise
    """
    admin_account: BasicAccount = BasicAccount(
        settings.admin_acct_sk.get_secret_value()
    )
    client: AlgodClient = AlgodClient(
        settings.algo_api_secrets.algod_token.get_secret_value(),
        settings.public.algod_address,
    )
    mtx = encoding.future_msgpack_decode(payload.FirstDeedTransferMtx)

    # Figure out terminal_asset_alias
    asset_idx = mtx.transaction.dictify()["xaid"]
    v_multi = MultisigAccount(
        version=1,
        threshold=2,
        addresses=[admin_account.addr, payload.ValidatorAddr],
    )
    a = client.account_asset_info(v_multi.addr, asset_idx)
    terminal_asset_alias = a["created-asset"]["name"]
    words = terminal_asset_alias.split(".")
    amn_alias = ".".join(words[:-1])
    amn = await BaseGNodeDb.objects.filter(alias=amn_alias).afirst()
    if amn is None:
        note = (
            f"Transfer received for ta_deed {asset_idx} for ta {terminal_asset_alias}"
            " but parent AtomicMeteringNode was not created!"
        )
        LOGGER.info(note)
        r = RestfulResponse(Note=note, HttpStatusCode=422)
        return r

    mtx.sign(admin_account.sk)
    try:
        algo_utils.send_signed_mtx(client=client, mtx=mtx)
    except Exception as e:
        note = f"Tried to sign transaction but there was an error.\n {e}"
        LOGGER.info(note)
        r = RestfulResponse(Note=note, HttpStatusCode=422)
        return r
    return await activate_terminal_asset(payload, admin_account, client)


async def initial_tadeed_algo_create_received(
    payload: InitialTadeedAlgoCreate, settings: config.GnfSettings
) -> RestfulResponse:
    """
    Co-signs and submits an AssetCreateTxn for a TaDeed. This method:
        - checks that the ValidatorAddr belongs to a Validator
        - checks that the asset_name in the unpacked mtx is the GNodeAlias of a
        BaseGNode object  `ta` of role TerminalAsset and status Pending
        - cosigns the ta_deed mtx
        - sends the mtx to the chain
        - on confirmation, changes the status of the TerminalAsset BaseGNode and its
        parent from `pending` to `active`
        - Creates a StatusBasegnode payload with information about these two roles
        - Sends that payload to the ta.g_node_registry_addr

    Args:
        payload: InitialTadeedAlgoCreate. The validation of the type guarantees
    that payload.HalfSignedCertCreationMtx is the encoding of a MultisigTransaction
    for the 2-sig multi [Gnf Admin, payload.ValidatorAddr] signed by the validator
    that creates an appropriately-formatted TaDeed

    Raises:
        SchemaError: if the payload does not have type InitialTadeedAlgoCreate

    Returns:
        Optional[BasegnodeGt]: None if the asset is not created
        otherwise the TerminalAsset database object
    """
    admin_sk = settings.admin_acct_sk.get_secret_value()
    client: AlgodClient = AlgodClient(
        settings.algo_api_secrets.algod_token.get_secret_value(),
        settings.public.algod_address,
    )

    if not isinstance(payload, InitialTadeedAlgoCreate):
        note = f"payload must be type InitialTadeedAlgoCreate, got {type(payload)}. Ignoring!"
        r = RestfulResponse(Note=note, HttpStatusCode=422)
        return r

    if not api_utils.is_validator(payload.ValidatorAddr):
        note = f"Address ..{payload.ValidatorAddr[-6:]} is not a Validator. Not making deed"
        r = RestfulResponse(Note=note, HttpStatusCode=422)
        return r

    mtx = encoding.future_msgpack_decode(payload.HalfSignedDeedCreationMtx)
    txn = mtx.transaction
    ta_alias: str = txn.dictify()["apar"]["an"]

    mtx.sign(admin_sk)
    try:
        response: PendingTxnResponse = algo_utils.send_signed_mtx(
            client=client, mtx=mtx
        )
    except Exception as e:
        note = f"Tried to sign transaction but there was an error.\n {e}"
        r = RestfulResponse(Note=note, HttpStatusCode=422)
        return r

    ta_deed_idx = response.asset_idx
    LOGGER.info(f"Initial TaDeed {ta_deed_idx} created for {ta_alias} ")
    r = await create_pending_atomic_metering_node(
        ta_alias=ta_alias, ta_deed_idx=ta_deed_idx, settings=settings
    )
    return r


async def create_updated_ta_deed(
    g_node: BaseGNodeDb,
    settings: config.GnfSettings,
) -> tuple[int, transaction.SignedTransaction]:
    """
    Creates a TADEED with asset name reflecting the updated
    GNodeAlias
    Returns:
        tuple[int, transaction.SignedTransaction]: asset_idx for new TADEED,
        signed transaction (by GnfAdmin) for creating new TADEED
    """
    admin_account: BasicAccount = BasicAccount(
        settings.admin_acct_sk.get_secret_value()
    )
    client: AlgodClient = AlgodClient(
        settings.algo_api_secrets.algod_token.get_secret_value(),
        settings.public.algod_address,
    )
    txn = transaction.AssetCreateTxn(
        sender=admin_account.addr,
        total=1,
        decimals=0,
        default_frozen=False,
        manager=admin_account.addr,
        asset_name=g_node.alias,
        unit_name="TADEED",
        sp=client.suggested_params(),
    )
    signed_txn = txn.sign(admin_account.sk)
    try:
        client.send_transaction(signed_txn)
    except:
        raise Exception(f"Failure sending transaction")
    r = algo_utils.wait_for_transaction(client, signed_txn.get_txid())
    LOGGER.info(f"New TaDeed {r.asset_idx} created for {g_node.alias}")
    return [r.asset_idx, signed_txn]


async def recursively_update_alias(
    g_node: BaseGNodeDb,
    new_parent_alias: str,
    settings: config.GnfSettings,
) -> str:

    orig_alias = g_node.alias
    final_word = orig_alias.split(".")[-1]
    new_alias = new_parent_alias + "." + final_word
    for dc_child in g_node.dc.children():
        child = await BaseGNodeDb.objects.filter(alias=dc_child.alias).afirst()
        await recursively_update_alias(
            g_node=child,
            new_parent_alias=new_alias,
            settings=settings,
        )

    g_node.prev_alias = g_node.alias
    g_node.alias = new_alias
    async_save = sync_to_async(g_node.save)
    await async_save()
    if g_node.dc.role == CoreGNodeRole.TerminalAsset:
        new_ta_deed_idx, signed_tadeed_creation_txn = await create_updated_ta_deed(
            g_node,
            settings,
        )

        payload = NewTadeedAlgoOptin_Maker(
            new_ta_deed_idx=new_ta_deed_idx,
            old_ta_deed_idx=g_node.ownership_deed_nft_id,
            ta_daemon_addr=g_node.daemon_addr,
            validator_addr=g_node.ownership_deed_validator_addr,
            signed_ta_deed_creation_txn=encoding.msgpack_encode(
                signed_tadeed_creation_txn
            ),
        ).tuple

        api_endpoint = f"http://0.0.0.0:8002/new-tadeed-algo-optin/"
        r = requests.post(url=api_endpoint, json=payload.as_dict())
        if r.status_code == 200:
            rr = RestfulResponse(**r.json())
            try:
                payload = NewTadeedSend_Maker.dict_to_tuple(rr.PayloadAsDict)
            except ValueError as e:
                LOGGER.info(f"Error in NewTadeedSend response: {e}")
                return

            r = await new_tadeed_send_received(payload, settings)


async def new_tadeed_send_received(
    payload: NewTadeedSend, settings: config.GnfSettings
) -> RestfulResponse:
    admin_account: BasicAccount = BasicAccount(
        settings.admin_acct_sk.get_secret_value()
    )
    client: AlgodClient = AlgodClient(
        settings.algo_api_secrets.algod_token.get_secret_value(),
        settings.public.algod_address,
    )
    txn = transaction.AssetTransferTxn(
        sender=admin_account.addr,
        receiver=payload.TaDaemonAddr,
        amt=1,
        index=payload.NewTaDeedIdx,
        sp=client.suggested_params(),
    )
    signed_txn = txn.sign(admin_account.sk)
    try:
        client.send_transaction(signed_txn)
    except:
        note = f"Failure sending AssetTransfer txn for {payload.NewTaDeedIdx}"
        r = RestfulResponse(Note=note, HttpStatusCode=422)
        return r
    algo_utils.wait_for_transaction(client, signed_txn.get_txid())

    LOGGER.info(f"New TaDeed {payload.NewTaDeedIdx} sent to TaDaemon")
    return await post_old_tadeed_algo_return(
        old_ta_deed_idx=payload.OldTaDeedIdx,
        new_ta_deed_idx=payload.NewTaDeedIdx,
        validator_addr=payload.ValidatorAddr,
        ta_daemon_addr=payload.TaDaemonAddr,
        signed_new_deed_transfer_txn=signed_txn,
        settings=settings,
    )


async def post_old_tadeed_algo_return(
    old_ta_deed_idx: int,
    new_ta_deed_idx: int,
    validator_addr: str,
    ta_daemon_addr: str,
    signed_new_deed_transfer_txn: transaction.SignedTransaction,
    settings: config.GnfSettings,
) -> RestfulResponse:
    admin_account: BasicAccount = BasicAccount(
        settings.admin_acct_sk.get_secret_value()
    )
    client: AlgodClient = AlgodClient(
        settings.algo_api_secrets.algod_token.get_secret_value(),
        settings.public.algod_address,
    )

    # opt into old tadeed
    txn = transaction.AssetOptInTxn(
        sender=admin_account.addr,
        index=old_ta_deed_idx,
        sp=client.suggested_params(),
    )
    txn = txn.sign(admin_account.sk)
    try:
        client.send_transaction(txn)
    except:
        note = (
            f"In generate_old_tadeed_algo_return. Failure sending transaction to opt into"
            f" old_ta_deed_idx {old_ta_deed_idx}"
        )
        return RestfulResponse(Note=note, HttpStatusCode=422)
    algo_utils.wait_for_transaction(client, txn.get_txid())

    # ask for the old TaDeed back
    payload = OldTadeedAlgoReturn_Maker(
        old_ta_deed_idx=old_ta_deed_idx,
        ta_daemon_addr=ta_daemon_addr,
        validator_addr=validator_addr,
        signed_new_deed_transfer_txn=encoding.msgpack_encode(
            signed_new_deed_transfer_txn
        ),
    ).tuple
    api_endpoint = f"http://0.0.0.0:8002/old-tadeed-algo-return/"
    r = requests.post(url=api_endpoint, json=payload.as_dict())
    if r.status_code > 200:
        if r.status_code == 422:
            note = (
                f"OldTadeedAlgoReturn error for {old_ta_deed_idx}:" + r.json()["detail"]
            )
        else:
            note = r.reason
        r = RestfulResponse(Note=note, HttpStatusCode=422)
        return r
    ta_alias = utils.get_ta_alias_from_ta_deed_idx(new_ta_deed_idx)
    if ta_alias is None:
        note = (
            "In post_old_tadeed_algo_return ..."
            f"new_ta_deed_idx {new_ta_deed_idx} does not provide a GNodeAlias!!"
        )
        return RestfulResponse(Note=note, HttpStatusCode=422)
    ta_db: BaseGNodeDb = await BaseGNodeDb.objects.filter(alias=ta_alias).afirst()
    if ta_db is None:
        return RestfulResponse(
            Note=f"ta_alias {ta_alias} for deed {new_ta_deed_idx} not in GNodeFactory!",
            HttpStatusCode=422,
        )
    ta_db.ownership_deed_nft_id = new_ta_deed_idx
    async_ta_save = sync_to_async(ta_db.save)
    await async_ta_save()

    return RestfulResponse(
        Note=f"Old deed {old_ta_deed_idx} transferred back and GNodes updated"
    )


async def create_pending_ctn(
    payload: DiscoverycertAlgoCreate, settings: config.GnfSettings
) -> RestfulResponse:
    """Given a ctn alias and the list of the aliases of the gnodes that
    will become its children, creates a pending ctn."""
    ctn_alias = payload.GNodeAlias
    if payload.CoreGNodeRole != CoreGNodeRole.ConductorTopologyNode:
        note = f"create_pending_ctn called for role {payload.CoreGNodeRole}!"
        return RestfulResponse(Note=note, HttpStatusCode=422)

    existing = await BaseGNodeDb.objects.filter(alias=ctn_alias).afirst()
    if existing is not None:
        note = f"Ctn {ctn_alias} already exists. Not issuing cert"
        return RestfulResponse(Note=note, HttpStatusCode=422)

    original_child_alias_list = payload.OldChildAliasList

    gps_d = {
        "lat": payload.MicroLat / 10**6,
        "lon": payload.MicroLon / 10**6,
    }
    gpsdb: GpsPointDb = await GpsPointDb.objects.acreate(**gps_d)

    gn = {
        "alias": ctn_alias,
        "status_value": GNodeStatus.Pending.value,
        "role_value": CoreGNodeRole.ConductorTopologyNode.value,
        "g_node_registry_addr": settings.public.gnr_addr,
        "gps_point_id": gpsdb.gps_point_id,
    }

    try:
        await BaseGNodeDb.objects.acreate(**gn)
    except RegistryError as e:
        return RestfulResponse(
            Note=f"Not creating pending ctn. Errors: {e}", HttpStatusCode=422
        )

    for child_alias in original_child_alias_list:
        try:
            dc_child = BaseGNode.by_alias[child_alias]
        except KeyError:
            raise Exception(f"Child alias {child_alias} not in GNodeFactory!")
        child = await BaseGNodeDb.objects.filter(alias=dc_child.alias).afirst()
        await recursively_update_alias(
            g_node=child,
            new_parent_alias=ctn_alias,
            settings=settings,
        )

    return RestfulResponse(Note=f"Created {ctn_alias}")


async def discoverycert_algo_create_received(
    payload: DiscoverycertAlgoCreate, settings: config.GnfSettings
) -> RestfulResponse:

    role = payload.CoreGNodeRole
    if role != CoreGNodeRole.ConductorTopologyNode:
        raise NotImplementedError(f"Only create CTNS w discovery certs, not {role}")
    await load_g_nodes_as_data_classes()
    return await create_pending_ctn(payload, settings)


async def load_g_nodes_as_data_classes():
    """Loads all objects in GNodeFactoryDb and GpsPointDb into
    the respective class Dicts
    """
    async for gpsdb in GpsPointDb.objects.all():
        gpsdb.dc
    async for gndb in BaseGNodeDb.objects.all():
        gndb.dc


async def retrieve_all_gns() -> List[BasegnodeGt]:
    gn_gt_list: List[BasegnodeGt] = []
    async for gn in BaseGNodeDb.objects.all():
        gn_gt = BasegnodeGt_Maker.dc_to_tuple(gn.dc)
        gn_gt_list.append(gn_gt)
    return gn_gt_list


async def g_node_from_alias(lrh_g_node_alias: str) -> Optional[BasegnodeGt]:
    if not property_format.is_lrh_alias_format(lrh_g_node_alias):
        raise ValueError(f"{lrh_g_node_alias} must have LRH Alias Format")
    g_node_alias = lrh_g_node_alias.replace("-", ".")
    gn = await BaseGNodeDb.objects.filter(alias=g_node_alias).afirst()
    if not gn:
        old_gn = await BaseGNodeHistory.objects.filter(alias=g_node_alias).afirst()
        if not old_gn:
            return None
        gn = await BaseGNodeDb.objects.filter(g_node_id=old_gn.g_node_id).afirst()

    gn_gt = BasegnodeGt_Maker.dc_to_tuple(gn.dc)
    return gn_gt


async def g_node_from_id(g_node_id: str) -> Optional[BasegnodeGt]:
    gn = await BaseGNodeDb.objects.filter(g_node_id=g_node_id).afirst()
    if not gn:
        return None
    gn_gt = BasegnodeGt_Maker.dc_to_tuple(gn.dc)
    return gn_gt


async def create_pending_atomic_metering_node(
    ta_alias: str, ta_deed_idx: int, settings: config.GnfSettings
) -> RestfulResponse:
    if not property_format.is_lrd_alias_format(ta_alias):
        r = RestfulResponse(
            Note=f"{ta_alias} must have LRD Alias Format",
            HttpStatusCode=422,
        )
        return r
    await load_g_nodes_as_data_classes()
    words = ta_alias.split(".")
    if words[-1] != "ta":
        r = RestfulResponse(
            Note=f"{ta_alias} must end in '.ta'",
            HttpStatusCode=422,
        )
        return r
    if len(words) == 1:
        r = RestfulResponse(
            Note=f"{ta_alias} does not have a parent; ignoring",
            HttpStatusCode=422,
        )
        return r
    parent_alias = ".".join(words[:-1])
    gn = {
        "alias": parent_alias,
        "status_value": GNodeStatus.Pending.value,
        "role_value": CoreGNodeRole.AtomicMeteringNode.value,
        "g_node_registry_addr": settings.public.gnr_addr,
    }
    LOGGER.info(f"About to try and create a new GNode w alias {parent_alias}")
    try:
        atm_db: BaseGNodeDb = await BaseGNodeDb.objects.acreate(**gn)
    except RegistryError as e:
        note = f"Not creating pending AtomicMeteringNode. Error making parent: {e}"
        LOGGER.info(note)
        r = RestfulResponse(
            Note=note,
            HttpStatusCode=422,
        )
        return r
    atm_db.status_value = GNodeStatus.Active.value
    async_save = sync_to_async(atm_db.save)
    await async_save()

    gn = {
        "alias": ta_alias,
        "status_value": GNodeStatus.Pending.value,
        "role_value": CoreGNodeRole.TerminalAsset.value,
        "g_node_registry_addr": settings.public.gnr_addr,
        "ownership_deed_nft_id": ta_deed_idx,
    }

    try:
        ta_db: BaseGNodeDb = await BaseGNodeDb.objects.acreate(**gn)
    except RegistryError as e:
        note = f"Not creating pending terminal asset. Error making terminalasset: {e}"
        LOGGER.info(note)
        r = RestfulResponse(
            Note=note,
            HttpStatusCode=422,
        )
        return r
    ta_gt = BasegnodeGt_Maker.dc_to_tuple(ta_db.dc)
    r = RestfulResponse(
        Note="Successfully created pending TerminalAsset",
        PayloadTypeName="basegnode.gt",
        PayloadAsDict=ta_gt.as_dict(),
    )
    return r


async def activate_terminal_asset(
    payload: InitialTadeedAlgoTransfer, admin_account: BasicAccount, client: AlgodClient
) -> RestfulResponse:
    mtx = encoding.future_msgpack_decode(payload.FirstDeedTransferMtx)
    asset_idx = mtx.transaction.dictify()["xaid"]
    v_multi = MultisigAccount(
        version=1,
        threshold=2,
        addresses=[admin_account.addr, payload.ValidatorAddr],
    )
    a = client.account_asset_info(v_multi.addr, asset_idx)
    ta_alias: str = a["created-asset"]["name"]

    gps_d = {
        "lat": payload.MicroLat / 10**6,
        "lon": payload.MicroLon / 10**6,
    }
    gpsdb: GpsPointDb = await GpsPointDb.objects.acreate(**gps_d)

    ta_db: BaseGNodeDb = await BaseGNodeDb.objects.filter(alias=ta_alias).afirst()
    if ta_db is None:
        note = f"In activate_terminal_asset. Could not find {ta_alias}!"
        r = RestfulResponse(
            Note=note,
            HttpStatusCode=422,
        )
        return r
    ta_db.ownership_deed_validator_addr = payload.ValidatorAddr
    ta_db.owner_addr = payload.TaOwnerAddr
    ta_db.daemon_addr = payload.TaDaemonAddr
    ta_db.gps_point_id = gpsdb.gps_point_id
    ta_db.status_value = GNodeStatus.Active.value
    async_save = sync_to_async(ta_db.save)
    await async_save()

    note = f" TaDeed {asset_idx} transferred to TaDaemon and Ta {ta_alias} activated"

    ta_gt = BasegnodeGt_Maker.dc_to_tuple(ta_db.dc)
    r = RestfulResponse(
        Note=note,
        PayloadTypeName="basegnode.gt",
        PayloadAsDict=ta_gt.as_dict(),
    )
    return r


async def parent_from_alias(alias: str) -> Optional["BaseGNodeDb"]:
    """
    Returns:
        - BaseGNodeDb. If the parent as suggested by the alias exists as an
        Active BaseGNode, returns that.
        - None. If alias is one word long (i.e. root of world), or if the
        parent suggested by the alias is not Active
    """
    alias_list = alias.split(".")
    alias_list.pop()
    parent_alias = ".".join(alias_list)
    parent = await BaseGNodeDb.objects.filter(
        alias=parent_alias, status_value="Active"
    ).afirst()
    return parent


async def parent(gndb: BaseGNodeDb) -> Optional["BaseGNodeDb"]:
    """
    Raises: DcError if "natural" parent (as suggested by alias) is not Active,
    and either
        - prev_alias is None, OR
        - the parent as suggested by prev_alias is not Active and/or
        does not exist.
    Returns:
        BaseGNode.   Parent BaseGNode
            - If the parent as suggested by the alias exists as an
        Active BaseGNode, returns that ("natural" parent)
            - Else, if the parent as suggested by the prev_alais exists
            as an active BaseGNode, returns that.
        None.
            - If alias is one word long (i.e. root of world)
    """
    if len(gndb.alias.split(".")) == 1:
        return None
    natural_parent = await parent_from_alias(gndb.alias)
    if natural_parent is not None:
        return natural_parent

    # alias may point to incorrect parent if getting updated
    if gndb.prev_alias is None:
        raise RegistryError(f"error finding parent for {gndb.alias}!")

    parent_pending_alias_update = await parent_from_alias(gndb.prev_alias)
    if parent_pending_alias_update is None:
        raise RegistryError(f"error finding parent for {gndb.alias}!")
    return parent_pending_alias_update
