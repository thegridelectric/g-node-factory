import logging
from typing import Optional

import requests
from algosdk import encoding
from algosdk.future import transaction
from algosdk.v2client.algod import AlgodClient
from rich.pretty import pprint

import gnf.algo_utils as algo_utils
import gnf.api_utils as api_utils
import gnf.config as config
import gnf.dev_utils.algo_setup as algo_setup
from gnf.algo_utils import BasicAccount
from gnf.algo_utils import MultisigAccount

# Schemata sent by validator
from gnf.schemata import InitialTadeedAlgoCreate
from gnf.schemata import InitialTadeedAlgoCreate_Maker
from gnf.schemata import InitialTadeedAlgoTransfer
from gnf.schemata import InitialTadeedAlgoTransfer_Maker
from gnf.schemata import TavalidatorcertAlgoCreate
from gnf.schemata import TavalidatorcertAlgoCreate_Maker
from gnf.schemata import TavalidatorcertAlgoTransfer
from gnf.schemata import TavalidatorcertAlgoTransfer_Maker
from gnf.utils import RestfulResponse


LOGGER = logging.getLogger(__name__)

GNF_API_ROOT = "http://127.0.0.1:8000"


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

    def post_initial_tadeed_algo_create(
        self, terminal_asset_alias: str
    ) -> RestfulResponse:

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

        payload = InitialTadeedAlgoCreate_Maker(
            validator_addr=self.acct.addr,
            half_signed_deed_creation_mtx=encoding.msgpack_encode(mtx),
        ).tuple
        LOGGER.info(
            f"Posting request to GnfRestAPI to create a TaDeed for {terminal_asset_alias}"
        )
        api_endpoint = f"{GNF_API_ROOT}/initial-tadeed-algo-create/"
        r = requests.post(url=api_endpoint, json=payload.as_dict())
        LOGGER.info("Response from GnfRestAPI:")
        pprint(r.json())
        if r.status_code > 200:
            LOGGER.warning(r.json())
            if "detail" in r.json().keys():
                note = "TavalidatorcertAlgoCreate error:" + r.json()["detail"]
            else:
                note = r.reason
            r = RestfulResponse(Note=note, HttpStatusCode=422)
            return r
        r = RestfulResponse(**r.json())
        return r

    def post_tavalidatorcert_algo_create(self) -> RestfulResponse:

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
        LOGGER.info("Posting request to GnfRestAPI to create new TaValidatorCert")
        api_endpoint = f"{self.settings.algo.gnf_api_root}/tavalidatorcert-algo-create/"

        r = requests.post(url=api_endpoint, json=payload.as_dict())
        LOGGER.info("Response from GnfRestAPI:")
        pprint(r.json())

        if r.status_code > 200:
            LOGGER.warning(r.json())
            if "detail" in r.json().keys():
                note = "TavalidatorcertAlgoCreate error:" + r.json()["detail"]
            else:
                note = r.reason
            r = RestfulResponse(Note=note, HttpStatusCode=422)
            return r

        r = RestfulResponse(**r.json())
        cert_idx = r.PayloadAsDict["Value"]

        payload = self.generate_transfer_tavalidatorcert_algo(cert_idx=cert_idx)
        LOGGER.info(
            f"Posting request to GnfRestAPI to transfer TaValidatorCert {cert_idx}"
        )

        api_endpoint = (
            f"{self.settings.algo.gnf_api_root}/tavalidatorcert-algo-transfer/"
        )
        r = requests.post(url=api_endpoint, json=payload.as_dict())
        LOGGER.info("Response from GnfRestAPI:")
        pprint(r.json())

        if r.status_code > 200:
            if "detail" in r.json().keys():
                note = "TavalidatorcertAlgoTransfer error:" + r.json()["detail"]
            else:
                note = r.reason
            r = RestfulResponse(Note=note, HttpStatusCode=422)
            return r
        r = RestfulResponse(**r.json())
        return r

    def post_initial_tadeed_algo_transfer(
        self,
        ta_deed_idx: int,
        ta_daemon_addr: str,
        ta_owner_addr: str,
        micro_lat: int,
        micro_lon: int,
    ) -> RestfulResponse:
        """
        This method is supposed to be called exactly for the FIRST time a TaDeed
        NFT is created for this ta_owner. For updated deeds, uses ExchangeTadeedAlgo

          - Creates the InitialTadeedAlgoTransfer payload and sends it to the Gnf
          - Returns the payload
        Args:
            ta_deed_idx (int): asset id of the TaDeed NFT
            ta_daemon (BasicAccount): The Layer 1 contract supporting NFT ownership
            and creation (TaDeed, TaTradingRights)

        Returns:
            InitialTadeedAlgoTransfer if sent,
            None if ta_multi does not have ta_deed_consideration_algos
        """

        required_algos = config.Algo().ta_deed_consideration_algos
        if algo_utils.algos(ta_daemon_addr) < required_algos:
            Exception(f"ta_daemon_addr not sufficiently funded!")
            return None
        txn = transaction.AssetTransferTxn(
            sender=self.validator_multi.addr,
            receiver=ta_daemon_addr,
            amt=1,
            index=ta_deed_idx,
            sp=self.client.suggested_params(),
        )
        mtx = self.validator_multi.create_mtx(txn)
        mtx.sign(self.acct.sk)
        payload = InitialTadeedAlgoTransfer_Maker(
            micro_lat=micro_lat,
            micro_lon=micro_lon,
            validator_addr=self.acct.addr,
            ta_daemon_addr=ta_daemon_addr,
            ta_owner_addr=ta_owner_addr,
            first_deed_transfer_mtx=encoding.msgpack_encode(mtx),
        ).tuple

        api_endpoint = (
            f"{self.settings.algo.gnf_api_root}/initial-tadeed-algo-transfer/"
        )
        r = requests.post(url=api_endpoint, json=payload.as_dict())

        LOGGER.info("Response from GnfRestAPI:")
        pprint(r.json())

        if r.status_code > 200:
            if "detail" in r.json().keys():
                note = "TavalidatorcertAlgoTransfer error:" + r.json()["detail"]
            else:
                note = r.reason
            r = RestfulResponse(Note=note, HttpStatusCode=422)
            return r
        r = RestfulResponse(**r.json())
        return r

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
