import logging
from typing import Optional

from algosdk import encoding
from algosdk.future import transaction
from algosdk.v2client.algod import AlgodClient

import gnf.algo_utils as algo_utils
import gnf.api_utils as api_utils
import gnf.config as config
import gnf.dev_utils.algo_setup as algo_setup
from gnf.algo_utils import BasicAccount
from gnf.algo_utils import MultisigAccount

# Schemata sent by validator
from gnf.schemata import TadeedAlgoCreate
from gnf.schemata import TadeedAlgoCreate_Maker
from gnf.schemata import TadeedAlgoTransfer
from gnf.schemata import TadeedAlgoTransfer_Maker
from gnf.schemata import TavalidatorcertAlgoCreate
from gnf.schemata import TavalidatorcertAlgoCreate_Maker
from gnf.schemata import TavalidatorcertAlgoTransfer
from gnf.schemata import TavalidatorcertAlgoTransfer_Maker


LOGGER = logging.getLogger(__name__)


class DevValidator:
    def __init__(self, settings: config.MollyMetermaidSettings):
        self.settings = settings
        self.client: AlgodClient = algo_utils.get_algod_client(self.settings.algo)
        self.acct: BasicAccount = BasicAccount(
            private_key=self.settings.acct_sk.get_secret_value()
        )
        self.validator_multi: MultisigAccount = (
            api_utils.get_validator_account_with_admin(self.acct.addr)
        )
        self.seed_fund_own_account()
        self.seed_fund_validator_joint_account()
        LOGGER.info("DevValidator Initialized")

    def send_message_to_gnf(self, payload: TavalidatorcertAlgoCreate):
        """Stub for when there is a mechanism (probably FastAPI) for validators  sending
        messages to GNodeFactory.

        Args:
            payload: Any valid payload in the API for sending
        """
        pass

    ###################
    # Messages sent
    ###################

    def generate_create_tadeed_algo(
        self, terminal_asset_alias: str
    ) -> TadeedAlgoCreate:

        txn = transaction.AssetCreateTxn(
            sender=self.validator_multi.address(),
            total=1,
            decimals=0,
            default_frozen=False,
            manager=self.settings.algo.gnf_admin_addr,
            asset_name=terminal_asset_alias,
            unit_name="TADEED",
            sp=self.client.suggested_params(),
        )
        mtx = self.validator_multi.create_mtx(txn)
        mtx.sign(self.acct.sk)

        payload = TadeedAlgoCreate_Maker(
            validator_addr=self.acct.addr,
            half_signed_deed_creation_mtx=encoding.msgpack_encode(mtx),
        ).tuple
        self.send_message_to_gnf(payload)
        return payload

    def generate_create_tavalidatorcert_algo(self) -> TavalidatorcertAlgoCreate:

        txn = transaction.AssetCreateTxn(
            sender=self.validator_multi.address(),
            total=1,
            decimals=0,
            default_frozen=False,
            manager=self.settings.algo.gnf_admin_addr,
            asset_name=self.settings.validator_cert_name,
            unit_name="VLDTR",
            note=self.settings.validator_name,
            url=self.settings.validator_web_page,
            sp=self.client.suggested_params(),
        )

        mtx = self.validator_multi.create_mtx(txn)
        mtx.sign(self.acct.sk)

        payload = TavalidatorcertAlgoCreate_Maker(
            validator_addr=self.acct.addr,
            half_signed_cert_creation_mtx=encoding.msgpack_encode(mtx),
        ).tuple
        self.send_message_to_gnf(payload)
        return payload

    def generate_transfer_tadeed_algo(
        self,
        ta_deed_idx: int,
        ta_owner_addr: str,
        ta_daemon_addr: str,
        micro_lat: int,
        micro_lon: int,
    ) -> Optional[TadeedAlgoTransfer]:
        """
        This method is supposed to be called exactly for the FIRST time a TaDeed
        NFT is created for this ta_owner. For updated deeds, uses ExchangeTadeedAlgo

        Let ta_multi be 2-sig [GnfAdmin, ta_daemon, ta_owner] acct. This method:

         - Makes sure ta_multi account has at least TaDeedConsideration Algos
         - Has ta_multi account opt into the ta_deed_idx (requires
        ta_owner sk, and ta_daemon sk, which we are giving it for the sake of expediency
        in this dev version)

          - Creates the TadeedAlgoTransfer payload and sends it to the Gnf
          - Returns the payload
        Args:
            ta_deed_idx (int): asset id of the TaDeed NFT
            ta_owner (BasicAccount): The owner of the TerminalAsset
            ta_daemon (BasicAccount): The Layer 1 contract supporting NFT ownership
            and creation (TaDeed, TaTradingRights)

        Returns:
            TadeedAlgoTransfer if sent,
            None if ta_multi does not have ta_deed_consideration_algos
        """
        ta_multi: algo_utils.MultisigAccount = algo_utils.MultisigAccount(
            version=1,
            threshold=2,
            addresses=[
                config.Algo().gnf_admin_addr,
                ta_daemon_addr,
                ta_owner_addr,
            ],
        )
        required_algos = config.Algo().ta_deed_consideration_algos
        if algo_utils.algos(ta_multi.addr) < required_algos:
            return None
        txn = transaction.AssetTransferTxn(
            sender=self.validator_multi.addr,
            receiver=ta_multi.addr,
            amt=1,
            index=ta_deed_idx,
            sp=self.client.suggested_params(),
        )
        mtx = self.validator_multi.create_mtx(txn)
        mtx.sign(self.acct.sk)
        payload = TadeedAlgoTransfer_Maker(
            first_deed_transfer_mtx=encoding.msgpack_encode(mtx),
            deed_validator_addr=self.acct.addr,
            ta_owner_addr=ta_owner_addr,
            ta_daemon_addr=ta_daemon_addr,
            micro_lat=micro_lat,
            micro_lon=micro_lon,
        ).tuple
        self.send_message_to_gnf(payload)
        return payload

    def generate_transfer_tavalidatorcert_algo(
        self, cert_idx: int
    ) -> TavalidatorcertAlgoTransfer:
        """First, opts in to the validator cert asset. Then, generates and signs the
        multsig transaction for transfer from the multi account self.multi (joint w
        gnf, threshold 2). Creates the TavalidatorcertAlgoTransferpayload with this
        mtx and sends it to the gnf.

        Args:
            cert_idx (int): the asset index for this validator's cert

        Returns:
            TavalidatorcertAlgoTransfer: the payload sent to the Gnf.
        """

        # Opting in to the cert
        opt_in_txn = transaction.AssetOptInTxn(
            sender=self.acct.addr,
            index=cert_idx,
            sp=self.client.suggested_params(),
        )
        signed_txn = opt_in_txn.sign(self.acct.sk)
        self.client.send_transaction(signed_txn)
        LOGGER.info(f"Molly has opted into asset idx {cert_idx}")
        algo_utils.wait_for_transaction(self.client, signed_txn.get_txid())

        transferTxn = transaction.AssetTransferTxn(
            sender=self.validator_multi.addr,
            receiver=self.acct.addr,
            amt=1,
            index=cert_idx,
            sp=self.client.suggested_params(),
        )

        mtx = self.validator_multi.create_mtx(transferTxn)
        mtx.sign(self.acct.sk)

        payload = TavalidatorcertAlgoTransfer_Maker(
            validator_addr=self.acct.addr,
            half_signed_cert_transfer_mtx=encoding.msgpack_encode(mtx),
        ).tuple
        self.send_message_to_gnf(payload)
        return payload

    ##########################
    # dev methods
    ########################
    def seed_fund_own_account(self):
        algos = config.Algo().gnf_validator_funding_threshold_algos + 1
        if algo_utils.algos(self.acct.addr) < algos:
            algo_setup.dev_fund_account(
                settings_algo=self.settings.algo,
                to_addr=self.acct.addr,
                amt_in_micros=10**6 * algos,
            )
        LOGGER.info(
            f"mollyMetermaid acct {self.acct.addr_short_hand} balance: ~{algo_utils.algos(self.acct.addr)} Algos"
        )

    def seed_fund_validator_joint_account(
        self,
    ) -> Optional[algo_utils.PendingTxnResponse]:
        """Becoming a validator requires this"""
        required_algos = config.Algo().gnf_validator_funding_threshold_algos
        current_algos = algo_utils.algos(self.validator_multi.address())
        if current_algos >= required_algos:
            LOGGER.info(
                f"ValidatorMulti account already has {current_algos} Algos. No more funding required"
            )
            return
        txn_response = algo_utils.pay_account(
            client=self.client,
            sender=self.acct,
            to_addr=self.validator_multi.address(),
            amt_in_micros=required_algos * 10**6,
        )
        if algo_utils.algos(self.validator_multi.address()) < required_algos:
            raise Exception(
                f"Failed to seed fund validator account {self.validator_multi.address()[-6:]}"
            )
        return txn_response
