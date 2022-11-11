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
from gnf.algo_utils import BasicAccount
from gnf.algo_utils import MultisigAccount
from gnf.algo_utils import PendingTxnResponse
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
from gnf.schemata import NewTadeedAlgoOptin_Maker
from gnf.schemata import NewTadeedSend
from gnf.schemata import NewTadeedSend_Maker
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
    client: AlgodClient = algo_utils.get_algod_client(settings.algo)
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
    client: AlgodClient = algo_utils.get_algod_client(settings.algo)
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
    admin_account: BasicAccount = BasicAccount(
        settings.admin_acct_sk.get_secret_value()
    )
    client: AlgodClient = algo_utils.get_algod_client(settings.algo)
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
    return await create_terminal_asset(payload, admin_account, client)


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
    client: AlgodClient = algo_utils.get_algod_client(settings.algo)

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
        ta_alias=ta_alias, ta_deed_idx=ta_deed_idx
    )
    return r


def discoverycert_algo_create_received(
    self, payload: DiscoverycertAlgoCreate, settings: config.GnfSettings
):
    admin_account: BasicAccount = BasicAccount(
        settings.admin_acct_sk.get_secret_value()
    )
    client: AlgodClient = algo_utils.get_algod_client(settings.algo)

    txn = transaction.AssetCreateTxn(
        sender=admin_account.addr,
        total=1,
        decimals=0,
        default_frozen=False,
        manager=admin_account.addr,
        asset_name=payload.GNodeAlias,
        unit_name="DISCOVER",
        sp=client.suggested_params(),
    )
    # TODO: create this and be ready to send it to discoverer, add  payload.SupportingMaterialHash

    role = payload.CoreGNodeRole
    if role != CoreGNodeRole.ConductorTopologyNode:
        raise NotImplementedError(f"Only create CTNS w discovery certs, not {role}")
    opt_in_payload = self.create_pending_ctn(payload)
    api_endpoint = f"http://0.0.0.0:8001/new-tadeed-algo-optin/"
    r = requests.post(url=api_endpoint, json=opt_in_payload.as_dict())
    pprint(r.json())
    r = RestfulResponse(**r.json())
    if not r.PayloadTypeName == NewTadeedSend_Maker.type_name:
        raise Exception(
            f"Expected r.PayloadTypeName to be 'new.tadeed.send' but got {r.PayloadTypeName}"
        )
    payload = NewTadeedSend_Maker.dict_to_tuple(r.PayloadAsDict)
    self.new_tadeed_send_received(payload)


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
    ta_alias: str, ta_deed_idx: int
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
        "g_node_registry_addr": config.SandboxDemo().gnr_addr,
        "ownership_deed_nft_id": ta_deed_idx,
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
    LOGGER.info(f"Just created a new GNode for {parent_alias}")
    atm_gt = BasegnodeGt_Maker.dc_to_tuple(atm_db.dc)
    r = RestfulResponse(
        Note="Successfully created pending Atomic Metering Node",
        PayloadTypeName="basegnode.gt",
        PayloadAsDict=atm_gt.as_dict(),
    )
    return r


async def create_terminal_asset(
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
    amn_alias = ".".join(ta_alias.split(".")[:-1])

    amn = await BaseGNodeDb.objects.filter(alias=amn_alias).afirst()
    amn.status_value = GNodeStatus.Active.value

    # This line is a problem if os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    # is removed

    async_save = sync_to_async(amn.save)
    await async_save()

    gps_d = {
        "lat": payload.MicroLat / 10**6,
        "lon": payload.MicroLon / 10**6,
    }
    gpsdb: GpsPointDb = await GpsPointDb.objects.acreate(**gps_d)

    gn = {
        "alias": ta_alias,
        "status_value": GNodeStatus.Pending.value,
        "role_value": CoreGNodeRole.TerminalAsset.value,
        "g_node_registry_addr": config.SandboxDemo().gnr_addr,
        "ownership_deed_nft_id": asset_idx,
        "ownership_deed_validator_addr": payload.ValidatorAddr,
        "owner_addr": payload.TaOwnerAddr,
        "daemon_addr": payload.TaDaemonAddr,
        "gps_point_id": gpsdb.gps_point_id,
    }

    try:
        ta: BaseGNodeDb = await BaseGNodeDb.objects.acreate(**gn)
    except RegistryError as e:
        note = f"Not creating pending terminal asset. Error making terminalasset: {e}"
        LOGGER.info(note)
        r = RestfulResponse(
            Note=note,
            HttpStatusCode=422,
        )
        return r

    ta.status_value = GNodeStatus.Active
    async_ta_save = sync_to_async(ta.save)
    await async_ta_save()
    note = (
        f"TerminalAsset created: {ta} and TaDeed {asset_idx}" " transferred to TaDaemon"
    )

    ta_gt = BasegnodeGt_Maker.dc_to_tuple(ta.dc)
    r = RestfulResponse(
        Note=note,
        PayloadTypeName="basegnode.gt",
        PayloadAsDict=ta_gt.as_dict(),
    )
    return r
