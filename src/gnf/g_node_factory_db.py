import logging
import os
from typing import Any
from typing import Optional
from typing import Tuple

import django
from algosdk import encoding
from algosdk.future import transaction
from algosdk.v2client.algod import AlgodClient

import gnf.algo_utils as algo_utils
import gnf.api_utils as api_utils
import gnf.config as config
from gnf.algo_utils import BasicAccount
from gnf.algo_utils import MultisigAccount
from gnf.algo_utils import PendingTxnResponse
from gnf.data_classes import BaseGNode
from gnf.enums import CoreGNodeRole
from gnf.enums import GNodeStatus
from gnf.enums import RegistryGNodeRole
from gnf.errors import RegistryError
from gnf.errors import SchemaError


LOG_FORMAT = (
    "%(levelname) -10s %(asctime)s %(name) -30s %(funcName) "
    "-35s %(lineno) -5d: %(message)s"
)
LOGGER = logging.getLogger(__name__)


# Messages sent by Factory
# Messages received by Factory
from gnf.schemata import BasegnodeCtnCreate
from gnf.schemata import BasegnodeTerminalassetCreate
from gnf.schemata import DiscoverycertAlgoCreate
from gnf.schemata import DiscoverycertAlgoTransfer
from gnf.schemata import HeartbeatA
from gnf.schemata import InitialTadeedAlgoCreate
from gnf.schemata import InitialTadeedAlgoTransfer
from gnf.schemata import NewTadeedAlgoOptin
from gnf.schemata import NewTadeedAlgoOptin_Maker
from gnf.schemata import OldTadeedAlgoReturn
from gnf.schemata import OldTadeedAlgoReturn_Maker
from gnf.schemata import TavalidatorcertAlgoCreate
from gnf.schemata import TavalidatorcertAlgoTransfer


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_related.settings")
django.setup()
from gnf.django_related.models import BaseGNodeDb
from gnf.django_related.models import GpsPointDb


class GNodeFactoryDb:
    """This is the database implementation of the GNodeFactory, where the topological
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

    def __init__(self, settings: config.GnfSettings):
        # super(GNodeFactoryBase, self).__init__(
        #     settings=settings,
        #     g_node_type_short_alias="gnf",
        # )
        self.settings = settings
        self.client: AlgodClient = algo_utils.get_algod_client(settings.algo)
        self.admin_account: BasicAccount = BasicAccount(
            settings.admin_acct_sk.get_secret_value()
        )
        algo_utils.verify_account_exists_and_funded(self.admin_account.addr)
        self.graveyard_account: BasicAccount = BasicAccount(
            settings.graveyard_acct_sk.get_secret_value()
        )
        algo_utils.verify_account_exists_and_funded(self.graveyard_account.addr)
        self.load_g_nodes_as_data_classes()
        LOGGER.info(f"Database GNodeFactory initialized")

    def load_g_nodes_as_data_classes(self):
        """Loads all objects in GNodeFactoryDb and GpsPointDb into
        the respective class Dicts
        """
        for gpsdb in GpsPointDb.objects.all():
            gpsdb.dc
        for gndb in BaseGNodeDb.objects.all():
            gndb.dc

    ########################
    # RabbitMq router gb
    ########################

    def route_direct_message(
        self,
        from_g_node_role_value: str,
        from_g_node_alias: str,
        payload: BasegnodeTerminalassetCreate,
    ):
        LOGGER.info(f"Got {payload} from {from_g_node_alias}")
        if from_g_node_role_value != RegistryGNodeRole.GNodeRegistry.value:
            raise Exception(f"GNodeFactory only listens to GNodeRegistries")
        if payload.TypeName == BasegnodeTerminalassetCreate.TypeName:
            if payload.FromGNodeAlias != from_g_node_alias:
                # Note: this validation should move to actor_base
                LOGGER.info(
                    f"payload.FromGNodeAlias must be from_g_node_alias {from_g_node_alias} "
                )
                return
            self.create_terminalasset_algo_received(payload)
        elif payload.TypeName == HeartbeatA.TypeName:
            self.sample_payload_received(payload)

    ##########################
    # Messages Sent
    ##########################

    def generate_old_tadeed_algo_return(
        self,
        old_ta_deed_idx: int,
        new_ta_deed_idx: int,
        validator_addr: str,
        ta_owner_addr: str,
        ta_daemon_addr: str,
    ) -> OldTadeedAlgoReturn:
        if new_ta_deed_idx is None:
            raise Exception(f"new_ta_deed_idx is None!")
        if old_ta_deed_idx is None:
            raise Exception(f"old_ta_deed_idx is None!")

        # opt into old tadeed
        txn = transaction.AssetOptInTxn(
            sender=self.admin_account.addr,
            index=old_ta_deed_idx,
            sp=self.client.suggested_params(),
        )
        signed_txn = txn.sign(self.admin_account.sk)
        try:
            self.client.send_transaction(signed_txn)
        except:
            raise Exception(f"Failure sending transaction")
        algo_utils.wait_for_transaction(self.client, signed_txn.get_txid())

        # transfer new deed to ta_daeomon
        txn = transaction.AssetTransferTxn(
            sender=self.admin_account.addr,
            receiver=ta_daemon_addr,
            amt=1,
            index=new_ta_deed_idx,
            sp=self.client.suggested_params(),
        )

        signed_new_deed_transafer_txn = txn.sign(self.admin_account.sk)
        try:
            self.client.send_transaction(signed_new_deed_transafer_txn)
        except:
            raise Exception(f"Failure sending transaction")
        algo_utils.wait_for_transaction(
            self.client, signed_new_deed_transafer_txn.get_txid()
        )

        # ask TaDaemon to transfer back the old deed
        payload = OldTadeedAlgoReturn_Maker(
            old_ta_deed_idx=old_ta_deed_idx,
            ta_daemon_addr=ta_daemon_addr,
            validator_addr=validator_addr,
            signed_new_deed_transfer_txn=encoding.msgpack_encode(
                signed_new_deed_transafer_txn
            ),
        ).tuple
        return payload

    ##########################
    # Messages Received
    ##########################

    def create_updated_ta_deed(
        self, g_node: BaseGNodeDb
    ) -> tuple[int, transaction.SignedTransaction]:
        """
        Creates a TADEED with asset name reflecting the updated
        GNodeAlias
        Returns:
            tuple[int, transaction.SignedTransaction]: asset_idx for new TADEED,
            signed transaction (by GnfAdmin) for creating new TADEED
        """
        txn = transaction.AssetCreateTxn(
            sender=self.admin_account.addr,
            total=1,
            decimals=0,
            default_frozen=False,
            manager=self.admin_account.addr,
            asset_name=g_node.alias,
            unit_name="TADEED",
            sp=self.client.suggested_params(),
        )
        signed_txn = txn.sign(self.admin_account.sk)
        try:
            tx_id = self.client.send_transaction(signed_txn)
        except:
            raise Exception(f"Failure sending transaction")
        r = algo_utils.wait_for_transaction(self.client, signed_txn.get_txid())
        return [r.asset_idx, signed_txn]

    def recursively_update_alias(
        self, g_node: BaseGNodeDb, new_parent_alias: str
    ) -> Optional[NewTadeedAlgoOptin]:
        payload_hack = None
        orig_alias = g_node.alias
        final_word = orig_alias.split(".")[-1]
        new_alias = new_parent_alias + "." + final_word
        for dc_child in g_node.dc.children():
            child = BaseGNodeDb.objects.filter(alias=dc_child.alias)[0]
            hack = self.recursively_update_alias(
                g_node=child, new_parent_alias=new_alias
            )
            if hack is not None:
                payload_hack = hack

        g_node.prev_alias = g_node.alias
        g_node.alias = new_alias
        g_node.save()
        if g_node.dc.role == CoreGNodeRole.TerminalAsset:
            new_ta_deed_idx, signed_tadeed_creation_txn = self.create_updated_ta_deed(
                g_node
            )
            payload_hack = NewTadeedAlgoOptin_Maker(
                ta_daemon_addr=g_node.daemon_addr,
                new_deed_idx=new_ta_deed_idx,
                validator_addr=g_node.ownership_deed_validator_addr,
                signed_ta_deed_creation_txn=encoding.msgpack_encode(
                    signed_tadeed_creation_txn
                ),
            ).tuple
            print("Just created NewTadeedAlgoOptin payload" f"{payload_hack}")
        return payload_hack

    def create_pending_ctn(
        self, payload: DiscoverycertAlgoCreate
    ) -> Optional[NewTadeedAlgoOptin]:
        """Given a ctn alias and the list of the aliases of the gnodes that
        will become its children, creates a pending ctn."""
        ctn_alias = payload.GNodeAlias
        if payload.CoreGNodeRole != CoreGNodeRole.ConductorTopologyNode:
            raise Exception(
                f"create_pending_ctn called for role {payload.CoreGNodeRole}!"
            )
        original_child_alias_list = payload.OldChildAliasList

        gpsdb: GpsPointDb = GpsPointDb(
            lat=payload.MicroLat / 10**6, lon=payload.MicroLon / 10**6
        )
        gpsdb.save()

        gn = {
            "alias": ctn_alias,
            "status_value": GNodeStatus.Pending.value,
            "role_value": CoreGNodeRole.ConductorTopologyNode.value,
            "g_node_registry_addr": config.SandboxDemo().gnr_addr,
            "gps_point_id": gpsdb.gps_point_id,
        }

        try:
            ctn = BaseGNodeDb.objects.create(**gn)
        except RegistryError as e:
            LOGGER.info(f"Not creating pending ctn. Errors: {e}")
            return None
        LOGGER.info(f"Pending Ctn created: {ctn}")
        for child_alias in original_child_alias_list:
            try:
                dc_child = BaseGNode.by_alias[child_alias]
            except KeyError:
                raise Exception(f"Child alias {child_alias} not in GNodeFactory!")
            child = BaseGNodeDb.objects.filter(alias=dc_child.alias)[0]
            opt_in_payload = self.recursively_update_alias(
                g_node=child, new_parent_alias=ctn_alias
            )
        return opt_in_payload

    def discoverycert_algo_create_received(
        self, payload: DiscoverycertAlgoCreate
    ) -> Optional[NewTadeedAlgoOptin]:
        if not isinstance(payload, DiscoverycertAlgoCreate):
            LOGGER.warning(
                f"payload must be type DiscoverycertAlgoCreate, got {type(payload)}. Ignoring!"
            )
            return None
        txn = transaction.AssetCreateTxn(
            sender=self.admin_account.addr,
            total=1,
            decimals=0,
            default_frozen=False,
            manager=self.admin_account.addr,
            asset_name=payload.GNodeAlias,
            unit_name="DISCOVER",
            sp=self.client.suggested_params(),
        )
        # TODO: create this and be ready to send it to discoverer, add  payload.SupportingMaterialHash

        role = payload.CoreGNodeRole
        if role != CoreGNodeRole.ConductorTopologyNode:
            raise NotImplementedError(f"Only create CTNS w discovery certs, not {role}")
        opt_in_payload = self.create_pending_ctn(payload)
        return opt_in_payload

    def create_pending_atomic_metering_node(
        self, ta_alias: str, ta_deed_idx
    ) -> Optional[BaseGNodeDb]:
        words = ta_alias.split(".")
        parent_alias = ".".join(words[:-1])
        gn = {
            "alias": parent_alias,
            "status_value": GNodeStatus.Pending.value,
            "role_value": CoreGNodeRole.AtomicMeteringNode.value,
            "g_node_registry_addr": config.SandboxDemo().gnr_addr,
            "ownership_deed_nft_id": ta_deed_idx,
        }

        try:
            atomic_metering_node = BaseGNodeDb.objects.create(**gn)
        except RegistryError as e:
            LOGGER.info(
                f"Not creating pending AtomicMeteringNode. Error making parent: {e}"
            )
            return None
        return atomic_metering_node

    def initial_tadeed_algo_create_received(
        self, payload: InitialTadeedAlgoCreate
    ) -> Optional[BaseGNodeDb]:
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
            Optional[BaseGNodeDb]: None if the asset is not created
            otherwise the TerminalAsset database object
        """
        self.client.account_info(payload.ValidatorAddr)
        if not isinstance(payload, InitialTadeedAlgoCreate):
            LOGGER.warning(
                f"payload must be type InitialTadeedAlgoCreate, got {type(payload)}. Ignoring!"
            )
            return None

        if not api_utils.is_validator(payload.ValidatorAddr):
            LOGGER.info(
                f"Address ..{payload.ValidatorAddr[-6:]} is not a Validator. Not making deed"
            )
            return None

        mtx = encoding.future_msgpack_decode(payload.HalfSignedDeedCreationMtx)
        txn = mtx.transaction
        ta_deed_alias = txn.dictify()["apar"]["an"]

        mtx.sign(self.admin_account.sk)
        try:
            response: PendingTxnResponse = algo_utils.send_signed_mtx(
                client=self.client, mtx=mtx
            )
        except Exception as e:
            LOGGER.warning(f"Tried to sign transaction but there was an error.\n {e}")
            return None

        ta_deed_idx = response.asset_idx
        LOGGER.info(
            f"TaDeed created for {ta_deed_alias} with ta_deed_idx {ta_deed_idx}"
        )

        atomic_metering_node = self.create_pending_atomic_metering_node(
            ta_alias=ta_deed_alias, ta_deed_idx=ta_deed_idx
        )

        if atomic_metering_node is None:
            # TODO: destroy deed!
            return None
        # TODO: send StatusBasegnode update to relevant GNodeRegistry
        return atomic_metering_node

    def sample_payload_received(self, payload: HeartbeatA):
        """Used for testing the rabbitmq actor base"""
        if not isinstance(payload, HeartbeatA):
            raise SchemaError(f"payload must be HeartbeatA, got {type(payload)}")
        LOGGER.info(f"just received HeartbeatA {payload}")

    def create_tavalidatorcert_algo_received(
        self, payload: TavalidatorcertAlgoCreate
    ) -> Optional[int]:
        """Co-signs and submits an AssetCreateTxn for a  Validator Certificate NFT.

        Args:
            payload: TavalidatorcertAlgoCreate. The validation of the type guarantees
        that payload.HalfSignedCertCreationMtx is the encoding of a MultisigTransaction
        for the 2-sig multi [Gnf Admin, payload.ValidatorAddr] signed by the validator
        that creates an appropriately-formatted Validator Certificate.

        Returns Optional[str]:
            - None if the payload has the wrong type or if there is an error submitting the
        transaction to the blockchain.
            - validator_cert_idx otherwise
        """

        if not isinstance(payload, TavalidatorcertAlgoCreate):
            LOGGER.warning(
                f"payload must be type TavalidatorcertAlgoCreate, got {type(payload)}. Ignoring!"
            )
            return None

        mtx = encoding.future_msgpack_decode(payload.HalfSignedCertCreationMtx)
        mtx.sign(self.admin_account.sk)
        try:
            response: PendingTxnResponse = algo_utils.send_signed_mtx(
                client=self.client, mtx=mtx
            )
        except Exception as e:
            LOGGER.warning(f"Tried to sign transaction but there was an error.\n {e}")
            return None

        valdiator_cert_idx = response.asset_idx
        LOGGER.info(
            f"ValidatorCert for ..{payload.ValidatorAddr[-6:]} created, asset_idx"
            f" {valdiator_cert_idx} \n tx_id {response.tx_id}"
        )

        return valdiator_cert_idx

    def update_ctn_to_active(self, payload: DiscoverycertAlgoTransfer) -> BaseGNodeDb:
        """
        Payload will be DiscoverycertAlgoTransfer.

        """

        ctn = BaseGNodeDb.objects.filter(alias=payload.GNodeAlias)[0]
        if ctn.dc.role != CoreGNodeRole.ConductorTopologyNode:
            raise Exception(f"Expected Ctn, got {ctn.dc.role}!")
        ctn.status_value = GNodeStatus.Active.value
        ctn.save()
        LOGGER.info(f"Ctn is now Active: {ctn}")
        return ctn

    def transfer_discoverycert_algo_received(
        self, payload: DiscoverycertAlgoTransfer
    ) -> Optional[BaseGNode]:
        """
        TODO: ADD!
        """

        if not isinstance(payload, DiscoverycertAlgoTransfer):
            LOGGER.warning(
                f"payload must be type DiscoverycertAlgoTransfer, got {type(payload)}. Ignoring!"
            )
            return None

        # TODO: find discovery cert that was already created and send it to discoverer
        txn = transaction.AssetTransferTxn(
            sender=self.admin_account.addr,
            receiver=payload.DiscovererAddr,
            amt=1,
            index=50,
        )
        ctn = self.update_ctn_to_active(payload)
        return ctn.dc

    def create_terminal_asset(self, payload: InitialTadeedAlgoTransfer) -> BaseGNodeDb:
        mtx = encoding.future_msgpack_decode(payload.FirstDeedTransferMtx)
        asset_idx = mtx.transaction.dictify()["xaid"]
        v_multi = MultisigAccount(
            version=1,
            threshold=2,
            addresses=[self.admin_account.addr, payload.DeedValidatorAddr],
        )
        a = self.client.account_asset_info(v_multi.addr, asset_idx)
        ta_alias: str = a["created-asset"]["name"]
        atomic_metering_node_alias = ".".join(ta_alias.split(".")[:-1])

        atomic_metering_node = BaseGNodeDb.objects.filter(
            alias=atomic_metering_node_alias
        )[0]
        atomic_metering_node.status_value = GNodeStatus.Active.value
        atomic_metering_node.save()

        gpsdb: GpsPointDb = GpsPointDb(
            lat=payload.MicroLat / 10**6, lon=payload.MicroLon / 10**6
        )
        gpsdb.save()

        gn = {
            "alias": ta_alias,
            "status_value": GNodeStatus.Pending.value,
            "role_value": CoreGNodeRole.TerminalAsset.value,
            "g_node_registry_addr": config.SandboxDemo().gnr_addr,
            "ownership_deed_nft_id": asset_idx,
            "ownership_deed_validator_addr": payload.DeedValidatorAddr,
            "owner_addr": payload.TaOwnerAddr,
            "daemon_addr": payload.TaDaemonAddr,
            "gps_point_id": gpsdb.gps_point_id,
        }

        try:
            terminal_asset = BaseGNodeDb.objects.create(**gn)
        except RegistryError as e:
            LOGGER.info(
                f"Not creating pending terminal asset. Error making terminalasset: {e}"
            )
            return None
        LOGGER.info(f"Pending TerminalAsset created: {terminal_asset}")

        terminal_asset.status_value = GNodeStatus.Active
        terminal_asset.save()
        LOGGER.info(f"TerminalAsset is now Active: {terminal_asset}")
        return terminal_asset

    def initial_tadeed_algo_transfer_received(
        self, payload: InitialTadeedAlgoTransfer
    ) -> Optional[BaseGNode]:
        """
            - Checks  consistency for the GNodeAlias in the deed:
                - in the BaseGNodeDb, there is a BaseGNode gn with this alias
                - gn.role = TerminalAsset
                - gn.status = Pending
                - gn.lat and gn.lon exist
                - gn.smart_daemon_addr =
                - gn.ownernship_deed_fnt_id does not exist
                - gn.ownership_deed_nft_creator_addr exists and matches
                2-sig [GnfAdmin, payload.DeedValidatorAddr]


            - Signs and submits an AssetTransferTxn that sends a TaDeed to the
        2-sig [GnfAdmin, TaDaemon, TaOwner] multi.
            - On confirmation, updates the GNodeDb gn:
                - gn.ownership_deed_nft_id = ta_asset_id
                - gn.status_value = Active.value
                - gn parent (the AtomicMeteringNode) status = Active.value
            - Sends a StatusBaseGgnodeAlgo to the correct GNodeREgistry ,
            identified by gn.g_node_registry_addr. Status.TopGNodeAlias = gn parent
            - Returns that StatusBaseGgnodeAlgo payload

        Args:
            payload: TavalidatorcertAlgoTransfer. The validation of the type guarantees
        that payload.HalfSignedCertTransferMtx is the encoding of a MultisigTransaction
        for the 1-sig multi [Gnf Admin, payload.ValidatorAddr] signed by the validator
        that transfers an appropriately-formatted Validator Certificate to the
        payload.ValidatorAddr. It also guarantees that the multi account is sufficiently
        funded and opted in.

        Returns Optional[str]:
            - None if transferring deed does not happen.
            - StatusBaseGgnodeAlgo otherwise
        """

        if not isinstance(payload, InitialTadeedAlgoTransfer):
            LOGGER.warning(
                f"payload must be type TavalidatorcertAlgoTransfer, got {type(payload)}. Ignoring!"
            )
            return None

        mtx = encoding.future_msgpack_decode(payload.FirstDeedTransferMtx)

        # Figure out terminal_asset_alias
        asset_idx = mtx.transaction.dictify()["xaid"]
        v_multi = MultisigAccount(
            version=1,
            threshold=2,
            addresses=[self.admin_account.addr, payload.DeedValidatorAddr],
        )
        a = self.client.account_asset_info(v_multi.addr, asset_idx)
        terminal_asset_alias = a["created-asset"]["name"]
        words = terminal_asset_alias.split(".")
        atomic_metering_node_alias = ".".join(words[:-1])
        if atomic_metering_node_alias not in BaseGNode.by_alias.keys():
            LOGGER.info(
                f"Transfer received for ta_deed {asset_idx} for ta {terminal_asset_alias}"
                " but parent AtomicMeteringNode was not created!"
            )
            return None

        mtx.sign(self.admin_account.sk)
        try:
            response: PendingTxnResponse = algo_utils.send_signed_mtx(
                client=self.client, mtx=mtx
            )
        except:
            LOGGER.warning(f"Tried to sign transaction but there was an error.\n {e}")
            return None
        LOGGER.info(
            f"TaDeed for {terminal_asset_alias}, asset-index {asset_idx} transferred to owner multi!"
        )
        terminal_asset = self.create_terminal_asset(payload)
        return terminal_asset.dc

    def transfer_tavalidatorcert_algo_received(
        self, payload: TavalidatorcertAlgoTransfer
    ):
        """Signs and submits an AssetTransferTxn that sends a Validator Certificate
        to the payload.ValidatorAddr

        Args:
            payload: TavalidatorcertAlgoTransfer. The validation of the type guarantees
        that payload.HalfSignedCertTransferMtx is the encoding of a MultisigTransaction
        for the 2-sig multi [Gnf Admin, payload.ValidatorAddr] signed by the validator
        that transfers an appropriately-formatted Validator Certificate to the
        payload.ValidatorAddr. It also guarantees that the multi account is sufficiently
        funded.

        Returns Optional[str]:
            - None if the payload has the wrong type or if there is an error submitting the
        transaction to the blockchain.
            - validator_cert_idx otherwise
        """

        if not isinstance(payload, TavalidatorcertAlgoTransfer):
            LOGGER.warning(
                f"payload must be type TavalidatorcertAlgoTransfer, got {type(payload)}. Ignoring!"
            )
            return None

        mtx = encoding.future_msgpack_decode(payload.HalfSignedCertTransferMtx)
        mtx.sign(self.admin_account.sk)
        try:
            response: PendingTxnResponse = algo_utils.send_signed_mtx(
                client=self.client, mtx=mtx
            )
        except:
            LOGGER.warning(f"Tried to sign transaction but there was an error.\n {e}")
            return None
        LOGGER.info(
            f"ValidatorCert for ..{payload.ValidatorAddr[-6:]} transferred\n txId {response.tx_id}"
        )
