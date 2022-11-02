import logging
from re import L
from typing import Optional

from algosdk import encoding
from algosdk.future import transaction
from algosdk.v2client.algod import AlgodClient

import gnf.algo_utils as algo_utils
import gnf.api_utils as api_utils
import gnf.config as config
import gnf.dev_utils.algo_setup as algo_setup
from gnf.algo_utils import BasicAccount

# Schemata sent by discoverer
from gnf.schemata import DiscoverycertAlgoCreate


LOGGER = logging.getLogger(__name__)


class DevDiscoverer:
    def __init__(self, settings: config.AdaDiscovererSettings):
        self.settings = settings
        self.client: AlgodClient = algo_utils.get_algod_client(self.settings.algo)
        self.acct: algo_utils.BasicAccount = algo_utils.BasicAccount(
            private_key=self.settings.sk.get_secret_value()
        )
        self.multi: algo_utils.MultisigAccount = (
            api_utils.get_discoverer_account_with_admin(self.acct.addr)
        )
        self.seed_fund_own_account()
        self.seed_fund_validator_joint_account()
        LOGGER.info("DevDiscoverer Initialized")

    def send_message_to_gnf(self, payload: DiscoverycertAlgoCreate):
        """Stub for when there is a mechanism (probably FastAPI) for validators  sending
        messages to GNodeFactory.

        Args:
            payload: Any valid payload in the API for sending
        """
        pass

    ###################
    # Messages sent
    ###################

    def generate_create_discoverycert_algo(
        self, terminal_asset_alias: str
    ) -> DiscoverycertAlgoCreate:

        txn = transaction.AssetCreateTxn(
            sender=self.multi.address(),
            total=1,
            decimals=0,
            default_frozen=False,
            manager=self.settings.algo.gnf_admin_addr,
            asset_name=terminal_asset_alias,
            unit_name="TADEED",
            sp=self.client.suggested_params(),
        )
        mtx = self.multi.create_mtx(txn)
        mtx.sign(self.acct.sk)

        payload = CreateTadeedAlgo_Maker(
            validator_addr=self.acct.addr,
            half_signed_deed_creation_mtx=encoding.msgpack_encode(mtx),
        ).tuple
        self.send_message_to_gnf(payload)
        return payload

    def generate_create_tavalidatorcert_algo(self) -> CreateTavalidatorcertAlgo:

        txn = transaction.AssetCreateTxn(
            sender=self.multi.address(),
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

        mtx = self.multi.create_mtx(txn)
        mtx.sign(self.acct.sk)

        payload = CreateTavalidatorcertAlgo_Maker(
            validator_addr=self.acct.addr,
            half_signed_cert_creation_mtx=encoding.msgpack_encode(mtx),
        ).tuple
        self.send_message_to_gnf(payload)
        return payload

    def generate_transfer_tadeed_algo(
        self, ta_deed_idx: int, ta_owner: BasicAccount, ta_daemon: BasicAccount
    ) -> TransferTadeedAlgo:
        """
        This method is supposed to be called exactly for the FIRST time a TaDeed
        NFT is created for this ta_owner. For updated deeds, uses ExchangeTadeedAlgo

        Let ta_multi be 2-sig [GnfAdmin, ta_daemon, ta_owner] acct. This method:

         - Makes sure ta_multi account has at least TaDeedConsideration Algos
         - Has ta_multi account opt into the ta_deed_idx (requires
        ta_owner sk, and ta_daemon sk, which we are giving it for the sake of expediency
        in this dev version)

          - Creates the TransferTadeedAlgo payload and sends it to the Gnf
          - Returns the payload
        Args:
            ta_deed_idx (int): asset id of the TaDeed NFT
            ta_owner (BasicAccount): The owner of the TerminalAsset
            ta_daemon (BasicAccount): The Layer 1 contract supporting NFT ownership
            and creation (TaDeed, TaTradingRights)

        Returns:
            TransferTadeedAlgo
        """
        ta_multi: algo_utils.MultisigAccount = algo_utils.MultisigAccount(
            version=1,
            threshold=2,
            addresses=[config.Algo().gnf_admin_addr, ta_daemon.addr, ta_owner.addr],
        )

        # Make sure ta multi has consideration funds
        funding_algos = config.Algo().ta_deed_consideration_algos
        LOGGER.info(
            f"Making sure ta_multi addr has TaDeedConsideration algos {funding_algos} "
        )
        algo_setup.dev_fund_to_min(addr=ta_multi.addr, min_algos=funding_algos)

        LOGGER.info(f"ta_multi opted into asset and funded with {funding_algos} Algos")
        # Opts into the asset
        opt_in_txn = transaction.AssetOptInTxn(
            sender=ta_multi.addr,
            index=ta_deed_idx,
            sp=self.client.suggested_params(),
        )
        opt_in_mtx = ta_multi.create_mtx(opt_in_txn)
        opt_in_mtx.sign(ta_daemon.sk)
        opt_in_mtx.sign(ta_owner.sk)
        algo_utils.send_signed_mtx(self.client, opt_in_mtx)

        txn = transaction.AssetTransferTxn(
            sender=self.multi.addr,
            receiver=ta_multi.addr,
            amt=1,
            index=ta_deed_idx,
            sp=self.client.suggested_params(),
        )
        mtx = self.multi.create_mtx(txn)
        mtx.sign(self.acct.sk)
        payload = TransferTadeedAlgo_Maker(
            first_deed_transfer_mtx=encoding.msgpack_encode(mtx),
            deed_validator_addr=self.acct.addr,
            ta_owner_addr=ta_owner.addr,
            ta_daemon_addr=ta_daemon.addr,
        ).tuple
        self.send_message_to_gnf(payload)
        return payload

    def generate_transfer_tavalidatorcert_algo(
        self, cert_idx: int
    ) -> TransferTavalidatorcertAlgo:
        """First, opts in to the validator cert asset. Then, generates and signs the
        multsig transaction for transfer from the multi account self.multi (joint w
        gnf, threshold 2). Creates the TransferTavalidatorcertAlgopayload with this
        mtx and sends it to the gnf.

        Args:
            cert_idx (int): the asset index for this validator's cert

        Returns:
            TransferTavalidatorcertAlgo: the payload sent to the Gnf.
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
            sender=self.multi.addr,
            receiver=self.acct.addr,
            amt=1,
            index=cert_idx,
            sp=self.client.suggested_params(),
        )

        mtx = self.multi.create_mtx(transferTxn)
        mtx.sign(self.acct.sk)

        payload = TransferTavalidatorcertAlgo_Maker(
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
        current_algos = algo_utils.algos(self.multi.address())
        if current_algos >= required_algos:
            LOGGER.info(
                f"Joint account already has {current_algos} Algos. No more funding required"
            )
            return
        txn_response = algo_utils.pay_account(
            client=self.client,
            sender=self.acct,
            to_addr=self.multi.address(),
            amt_in_micros=required_algos * 10**6,
        )
        if algo_utils.algos(self.multi.address()) < required_algos:
            raise Exception(
                f"Failed to seed fund validator account {self.multi.address()[-6:]}"
            )
        return txn_response
