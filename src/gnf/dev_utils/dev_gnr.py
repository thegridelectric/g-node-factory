import logging
from typing import Optional

from algosdk.future.transaction import MultisigTransaction
from algosdk.v2client.algod import AlgodClient

import gnf.algo_utils as algo_utils
import gnf.config as config
import gnf.dev_utils.algo_setup as algo_setup
from gnf.enums import RegistryGNodeRole
from gnf.errors import SchemaError

# Message types received by the GNodeRegistry
# Message types sent by GNodeRegistry
from gnf.schemata import BasegnodesBroadcast
from gnf.schemata import BasegnodeTerminalassetCreate
from gnf.schemata import BasegnodeTerminalassetCreate_Maker
from gnf.schemata import HeartbeatA


LOGGER = logging.getLogger(__name__)


class DevGnr:
    def __init__(self, settings: config.DevGNodeRegistrySettings):
        self.settings = settings
        self.alias = settings.g_node_alias
        self.g_node_instance_id = settings.g_node_instance_id
        self.algoClient: AlgodClient = algo_utils.get_algod_client(self.settings.algo)
        self.acct: algo_utils.BasicAccount = algo_utils.BasicAccount(
            private_key=self.settings.sk.get_secret_value()
        )
        self.mtxForCert: Optional[MultisigTransaction] = None
        self.seed_fund_own_account()
        LOGGER.info("DevGNodeRegistry Initialized")

    ########################
    # RabbitMq
    ########################

    def route_direct_message(
        self, from_g_node_role_value: str, from_g_node_alias: str, payload: HeartbeatA
    ):

        """Routes inbound messages to correct method"""
        LOGGER.info(f"Got {payload} from {from_g_node_alias}")
        type_name = payload.TypeName
        if from_g_node_role_value != RegistryGNodeRole.GNodeFactory.value:
            raise NotImplementedError
        if type_name == HeartbeatA.TypeName:
            self.heartbeat_a_received(payload, from_g_node_alias)
        elif type_name == BasegnodesBroadcast.TypeName:
            self.status_basegnode_algo_received(payload, from_g_node_alias)

    def prepare_for_death(self):
        """If there are threads running beyond the two designed for publishing and consuming messages,
        shut those down prior to setting actor_main_stopped to True"""
        self.actor_main_stopped = True

    def send_direct_message(
        self,
        payload: BasegnodeTerminalassetCreate,
        to_g_node_type_short_alias: str,
        to_g_node_alias: str,
    ):
        """Stub for actor_base send_direct_message"""
        LOGGER.info(
            f"Stub for sending BasegnodeTerminalassetCreate to {to_g_node_alias} via rabbit"
        )
        pass

    ##########################
    # Messages Received
    ##########################

    def heartbeat_a_received(self, payload: HeartbeatA, from_g_node_alias: str):
        """
        Args:
            payload: HeartbeatA
            from_g_node_alias (str): alias of the actor sending the heartbeat
        """
        if not isinstance(payload, HeartbeatA):
            raise SchemaError
        LOGGER.debug(f"HeartbeatA {payload} received from {from_g_node_alias}")

    def status_basegnode_algo_received(
        self, payload: BasegnodesBroadcast, from_g_node_alias: str
    ):
        """
        Args:
            payload: BasegnodesBroadcast
            from_g_node_alias (str): alias of the actor sending the heartbeat
        """
        if not isinstance(payload, BasegnodesBroadcast):
            raise SchemaError(f"Got type {type(payload)}, require BasegnodesBroadcast")

        gnf_alias = self.settings.algo.gnf_g_node_alias
        if not from_g_node_alias == gnf_alias:
            LOGGER.info(
                f"Got BasegnodesBroadcast from {from_g_node_alias}. Only pay attention to {gnf_alias} "
            )

        print(f"Got BasegnodesBroadcast {payload}. Now implement")
        pass

    ##########################
    # Messages sent
    ##########################

    def generate_create_terminalasset_algo_payload(
        self, ta_owner_addr: str, validator_addr: str, micro_lat: int, micro_lon: int
    ) -> BasegnodeTerminalassetCreate:
        """This method generates a payload to send to the GNodeFactory. The request
        triggers the creation of two GNodes:
            - the TerminalAsset GNode
            - its parent GNode, which starts out with the role of `AtomicMeteringNode` and
            once a `TaTradingRights` NFT exists the role transitions to `AtomicTNode`

        The Status of these GNodes is `pending` until the `TaDeed` has been transferred to
        the multi account [GnfAdmin, TaOwnerSmartDaemon, TaOwner]

        Args:
            ta_owner_addr (str): Algo Address of the TaOwner (owner of the actual physical
            device in the TerminalAsset, and the one accountable for financial transactions
            through the meter of the TerminalAsset)
            validator_addr (str): Algo Address of the TaValidator selected by the owner
            to validate their asset (prerequisite for the status to go to Active)
            micro_lat (int): Latitude of the TerminalAsset * 10**6
            micro_lon (int): Longitude of the TerminalAsset * 10**6

        Returns:
            BasegnodeTerminalassetCreate payload
        """
        payload = BasegnodeTerminalassetCreate_Maker(
            from_g_node_alias=self.alias,
            from_g_node_instance_id=self.g_node_instance_id,
            g_node_registry_addr=self.acct.addr,
            ta_g_node_alias=self.settings.algo.gnf_g_node_alias,
            ta_owner_addr=ta_owner_addr,
            validator_addr=validator_addr,
            micro_lat=micro_lat,
            micro_lon=micro_lon,
        ).tuple
        to_g_node_type_short_alias = "gnf"
        to_g_node_alias = self.settings.algo.gnf_g_node_alias
        self.send_direct_message(payload, to_g_node_type_short_alias, to_g_node_alias)
        return payload

    ##########################
    # dev methods
    ########################

    def seed_fund_own_account(self):
        algos = 1
        if algo_utils.algos(self.acct.addr) < algos:
            algo_setup.dev_fund_account(
                settings_algo=self.settings.algo,
                to_addr=self.acct.addr,
                amt_in_micros=10**6 * algos,
            )
        LOGGER.info(
            f"Dev Gnr acct {self.acct.addr_short_hand} balance: ~{algo_utils.algos(self.acct.addr)} Algos"
        )
