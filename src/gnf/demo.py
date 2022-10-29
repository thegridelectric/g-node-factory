import logging
import pprint
import time

import algo_utils
import api_utils
import config
import dev_utils.algo_setup
import load_dev_data
from algosdk.v2client.algod import AlgodClient
from data_classes.base_g_node import BaseGNode
from dev_utils.dev_homeowner import DevHomeowner
from dev_utils.dev_validator import DevValidator
from g_node_factory_db import GNodeFactoryDb
from python_ta_daemon import PythonTaDaemon


pp = pprint.PrettyPrinter(indent=4)

SCRIPT_SLEEP_S = 5  # replace with keyboard prompt to continue?


logging.basicConfig(level="INFO")

settingsAlgo = config.Algo()

client: AlgodClient = algo_utils.get_algod_client(settingsAlgo)

if api_utils.is_validator(config.SandboxDemo().molly_metermaid_addr):
    raise Exception(
        f"molly is already a validator. Reset the sandbox and start again! Also, run ./reset-dev-db.sh"
    )


print("")
print("")

print("##########################################################")
print("# The Demo is organized as a series of transaction flows:")
print("#   (1) Validator Certification Flow ")
print("#   (2) TerminalAsset Creation Flow ")
print("#   (3) Deed Change Flow ")
print("##########################################################")


print("")
print("")
time.sleep(SCRIPT_SLEEP_S)

print("##########################################################")
print("# Starting TaValidator Certification Flow (Flow 1)")
print("##########################################################")
print("")
print("")
time.sleep(SCRIPT_SLEEP_S)
print("MollyMetermaid wants to become a TaValidator")

print("")
print("")
time.sleep(SCRIPT_SLEEP_S)
print("First, we need to initialize and fund various actors.")
print("")
print("")
time.sleep(SCRIPT_SLEEP_S)

print(f"Start by funding the Gnf accounts")
print("")
print("")
dev_utils.algo_setup.dev_fund_admin_and_graveyard(config.GnfSettings())
print("")
print("")
print(f"Now that these accounts are funded, starting the GNodeFactory")
print("")
print("")
gnf = GNodeFactoryDb(config.GnfSettings())


if len(BaseGNode.by_alias) > 0:
    raise Exception("Please reset GNode data by running ./reset-dev-db.sh ")

load_dev_data.main()
# shorthand names for the relevant algo accounts
graveyard = gnf.graveyard_account
admin = gnf.admin_account

holly = DevHomeowner(
    settings=config.HollyHomeownerSettings(),
    ta_daemon_addr=config.SandboxDemo().holly_ta_daemon_addr,
    validator_addr=config.SandboxDemo().molly_metermaid_addr,
    initial_terminal_asset_alias=config.SandboxDemo().initial_holly_ta_alias,
)

ta_multi = algo_utils.MultisigAccount(
    version=1,
    threshold=2,
    addresses=[admin.addr, holly.ta_daemon_addr, holly.acct.addr],
)


print("")
print("")
print(
    "We start up a simple class that mocks up a dapp for Molly that interacts with the GNodeFactory"
)
print("")
print("")
print("molly = DevValidator(config.MollyMetermaidSettings())")
molly = DevValidator(config.MollyMetermaidSettings())
print("")
print("")
time.sleep(SCRIPT_SLEEP_S)
print(
    "Being a TaValidator means Molly can validate TaDeeds for people who own TerminalAssets "
)
print(
    "The GNodeFactory enforces that validation by a TaValidator must happen before the TaDeed"
)
print(
    "can owned by the TaOwner. Just like with house deeds, these TaDeeds are a representation"
)
print(
    "of an already agreed-upon concept of ownership - in this demo, for example, TaOwner"
)
print("HollyHomeowner owning a her own electric thermal storage heating system.")
print("")
print("")
time.sleep(SCRIPT_SLEEP_S)
print(
    "Anybody can become a TaValidator, as long as they are prepared to be held publicly accountable"
)
print(
    "for their validations. TaOwners can select the TaValidator they want to use. They will want to choose"
)
print(
    "an organization that they trust in their own house, and whose technical expertise and integrity"
)
print(
    "will be trusted by potential counterparties in energy/money transactions down the road with "
)
print("their TerminalAsset.")
print("")
print("")
time.sleep(SCRIPT_SLEEP_S)
print("To become a validator, Molly requires ")
print(
    "      - a ValidatorCertificate NFT created by the two-sig MultiSigAccount [Gnf.admin.addr, molly.addr]"
)
print("       - the same ValidatorCertificate owned by the molly.addr")

print("")
print("")
time.sleep(SCRIPT_SLEEP_S)
print("At the start, Molly has neither: ")
print(
    f"api_utils.is_validator(molly.acct.addr): {api_utils.is_validator(molly.acct.addr)}"
)

print(
    "Before the gnf will co-sign the token creation, Molly needs to fund the joint account "
)
print("with 100 Algos.")
print("")
print("")
time.sleep(SCRIPT_SLEEP_S)
print(
    "As a Validator, Molly's joint account with gnf will be creating the taDeed certificates."
)
print(
    "So funding with 100 Algos means the joint account has enough funding to create 1000 taDeeds."
)

time.sleep(SCRIPT_SLEEP_S)
print("")
print("")
print(
    "Lawyers would probably consider this a reasonable amount of consideration for a company making the commitment to be a validator."
)


time.sleep(SCRIPT_SLEEP_S)

print("")
print("")

print("Molly generates a request for becoming a new validator by ")
print("     1) funding the joint account with 100 Algos")
print("     2) having the joint account make an assetCreation transaction")
print("     3) signing that transaction, and then")
print("     4) creating a json message of  type `create.validatorcert.algo.010`")
print("")
print("")
time.sleep(SCRIPT_SLEEP_S)
print("The CreateTavalidatorcertAlgo message contains 2 things: ")
print("     1) Molly's address")
print("     2) the half-signed assetCreation transaction")
print("")
print("")

time.sleep(SCRIPT_SLEEP_S)

print("payload = molly.generateCreateTavalidatorcertAlgo()")
print("")
print("")
time.sleep(SCRIPT_SLEEP_S)
print("This payload is an API message of type create.validatorcert.algo.010")
print("")
print("")
cert_idx = api_utils.get_validator_cert_idx(validator_addr=molly.acct.addr)
if cert_idx is not None:
    raise Exception(
        f"There is already a Validator Certificate for Molly! Please ./sandbox reset and start the demo over."
    )
payload = molly.generate_create_tavalidatorcert_algo()
print("")
print("")
print(f"payload: {payload}")
print("")
print("")

time.sleep(SCRIPT_SLEEP_S)

print(
    f"Inspecting actual payload.HalfSignedCertCreationMtx: {payload.HalfSignedCertCreationMtx}"
)

print("")
print("")

time.sleep(SCRIPT_SLEEP_S)
print(
    "Eventually this payload will arrive at the gnf via rabbitMQ or a FastAPI but for the sake of this demo"
)
print(
    "we just call the method cert_idx = gnf.CreateTavalidatorcertAlgoReceived(payload) directly."
)
print("")
print("")

print(
    "The GNodeFactory will inspect the payload and checks that it is a correctly formed transaction"
)
print("for creating a ValidatorCert NFT for Molly with Molly's signature.")
print("")
print("")

time.sleep(SCRIPT_SLEEP_S)
print(
    "Assuming it is, the GNodeFactory then signs and submits the transaction and gets back the newly created cert_idx "
)

cert_idx = gnf.create_tavalidatorcert_algo_received(payload)


print("")
print("")
time.sleep(SCRIPT_SLEEP_S)

print("We can check out the asset in the multiSig address")

print("")
print(f"client.account_info(molly.multi.addr)['created-assets']:")
pp.pprint(client.account_info(molly.validator_multi.addr)["created-assets"])

print("")
print("")
print("The ValidatorCerticate is now created, but Molly's address does not own it.")
print(
    f"client.account_info(molly.acct.addr)['assets']: {client.account_info(molly.acct.addr)['assets']}"
)
print("")
print("")
time.sleep(SCRIPT_SLEEP_S)
print("By definition, Molly becomes a validator when she owns her ValidatorCertificate")
print("")
print("")
time.sleep(SCRIPT_SLEEP_S)
print(
    f"api_utils.is_validator(molly.acct.addr): {api_utils.is_validator(molly.acct.addr)}"
)
print("")
print("")
time.sleep(SCRIPT_SLEEP_S)

print(
    "Molly opts into Cert, and creates & signs a mtx for transferring the cert to her account from the multi account"
)
print("payload = molly.generateTransferTavalidatorcertAlgBase(certIdx=certIdx)")
time.sleep(SCRIPT_SLEEP_S)
print("")
print("")
print(
    f"the payload is TransferTavalidatorcertAlgo message, which has the co-signed cert transfer. Molly sends this to the Gnf"
)

molly_assets = client.account_info(molly.acct.addr)["assets"]
if len(list(filter(lambda x: x["asset-id"] == cert_idx, molly_assets))) > 0:
    raise Exception(
        "Molly already has the asset. Please ./sandbox reset and then run demo"
    )


payload = molly.generate_transfer_tavalidatorcert_algo(cert_idx=cert_idx)
print("")
print("")
print(f"gnf.TransferTavalidatorcertAlgReceived(payload)")
gnf.transfer_tavalidatorcert_algo_received(payload)
print("")
print("")

time.sleep(SCRIPT_SLEEP_S)
print(
    f"api_utils.is_validator(molly.acct.addr): {api_utils.is_validator(molly.acct.addr)}"
)
print("")
print("")
time.sleep(SCRIPT_SLEEP_S)
print("We examine Molly's assets")
print("")
print("")
pp.pprint(client.account_asset_info(molly.acct.addr, asset_id=cert_idx))
print("")
print("")
time.sleep(SCRIPT_SLEEP_S)
time.sleep(SCRIPT_SLEEP_S)
print("##########################################################")
print("# This completes the Validator Certification Flow ")
print("##########################################################")

print("")
print("")
time.sleep(SCRIPT_SLEEP_S)
print("###################################################################")
print("# Starting TerminalAsset Deed Creation Flow -  Flow 2")
print("###################################################################")

print("")
print("")
time.sleep(SCRIPT_SLEEP_S)

print(
    "Holly Homeowner heats her house with a Heat pump Thermal Storage heating system."
)
print(
    "She wants to lower her heating costs by having her heater use energy when there is excess wind on the grid."
)

print("")
time.sleep(SCRIPT_SLEEP_S)
print(
    "To do this, she needs to own a `TaDeed` NFT for her heating system. This will allow her heating system"
)
print(
    "to be represented as a `TerminalAsset` in the GNodeFactory, which in turn will allow the AtomicTransactiveNode "
)
print(
    "for her heating system (the parent node of her `TerminalAsset`) to access low and negative wholesale prices. "
)
print("")
print("")
time.sleep(SCRIPT_SLEEP_S)
print("")
print("")
time.sleep(SCRIPT_SLEEP_S)
print(
    "HollyHomeowner asks MollyMetermaid to validate her TerminalAsset, so that she can get a TaDeed."
)
print("")
print("")
time.sleep(SCRIPT_SLEEP_S)

print("Molly generates a CreateTadeedAlgo request and sends it to the GNodeFactory ")
print("This Tadeed is created by the ValidatorMulti account descrived above, ")
print("and includes the new GNodeAlias for Holly's TerminalAsset as the asset name ")

print("")
print("")
time.sleep(SCRIPT_SLEEP_S)

ta_deed_idx = api_utils.get_tadeed_cert_idx(
    terminal_asset_alias=holly.initial_terminal_asset_alias,
    validator_addr=molly.acct.addr,
)

if ta_deed_idx is not None:
    raise Exception(f"Please ./sandbox reset to rerun demo")


payload = molly.generate_create_tadeed_algo(
    terminal_asset_alias=holly.initial_terminal_asset_alias,
)
print("The GNodeFactory receives a half-signed TaDeed AssetCreationTxn.")
print(
    "After making sure it has also heard from the GNodeRegistry re location information"
)
print("and best-known grid topology information about this asset, tt signs and submits")

atomic_metering_node = gnf.create_tadeed_algo_received(payload)
ta_deed_idx = atomic_metering_node.ownership_deed_nft_id
print("")
time.sleep(SCRIPT_SLEEP_S)

print(
    f"The TaDeed for Holly's heater, {holly.initial_terminal_asset_alias}, now exists (ta_deed_idx {ta_deed_idx}), and we can see it"
)
print(
    f"in the account that created it, and we can see it in the account that created it. "
)

print("")
print("")
pp.pprint(client.account_asset_info(molly.validator_multi.addr, ta_deed_idx))
print("")
print("")
time.sleep(SCRIPT_SLEEP_S)


print(f"(That was client.account_asset_info(molly.validator_multi.addr, {ta_deed_idx})")
print("")
print("")
time.sleep(SCRIPT_SLEEP_S)
print(
    "Once the TaDeed was created, the GNodeFactory also created the parent GNode, for Holly's TerminalAsset which"
)
print(" is an AtomicMeteringNode, with a lifecycle Status 'Pending'")
print("")
print("")
time.sleep(SCRIPT_SLEEP_S)
print(
    f"If Molly does not validate the metering and location of Holly's heater, the TerminalAsset will not be created and"
)
print(f"the AtomicMeteringNode will never have a lifecycle Status of  'Active'")
print("")
print("")
time.sleep(SCRIPT_SLEEP_S)

print(
    "The Gnf will not create a new GNode unless its parent is Active. This is why it only created the parent, "
)
print("which at this point has a status of Pending.")
print("")
print("")
time.sleep(SCRIPT_SLEEP_S)
print("The ta_deed now exists, but it is not owned by Holly: ")
print("")
print("")
print(
    f"client.account_info(ta_multi.addr)['assets']: {client.account_info(ta_multi.addr)['assets']}"
)
print("")
print("")
time.sleep(SCRIPT_SLEEP_S)
print(
    "`ta_multi` above refers to the 2-sig MultisigAccount with addresses [GnfAdmin, HollyPythonTaDaemon, Holly]"
)
print(
    "This is the account that will hold Holly's TaDeed (and will later create TaTradingRights)."
)
print("")
print("")
time.sleep(SCRIPT_SLEEP_S)
print(
    "Holly opts into her TaDeed. This requires funding her ta_multi account with 50 Algos first,"
)
print(
    "and then sending a `sign and submit` message the newly created PythonTaDaemon which is part of "
)
print(
    "her ta_multi account and will administrative tasks for that account without Holly "
)
print("needing to take any action.")
print("")
print("")
time.sleep(SCRIPT_SLEEP_S)
print(
    "To keep Holly's active rights over the ta_multi account healthy, one of the rules governing"
)
print(
    "the behavior of the PythonTaDaemonis that it will sign and submit any valid multi-transaction sent"
)
print(
    "In addition, the remaining scope of its actions are very limited: it will exchange an to it by Holly."
)
print(
    "old, out-of-date TaDeed with a new one, with the GNodeFactory co-signing that exchange."
)
print("")
print("")
time.sleep(SCRIPT_SLEEP_S)
payload = holly.opt_into_original_deed()

daemon = PythonTaDaemon(
    sk=config.HollyTaDaemonSettings().sk.get_secret_value(),
    ta_owner_addr=config.SandboxDemo().holly_homeowner_addr,
    algo_settings=config.Algo(),
)

daemon.signandsubmit_mtx_algo_received(payload)
time.sleep(SCRIPT_SLEEP_S)
print(
    "Finally, Molly Metermaid must schedule a visit and inspect the location, topology, and metering of the pending TerminalAsset."
)
print(
    "A couple of weeks later, Molly does this. She is now prepared to publicly attest to the information in the TaDeed."
)
print("")
print("")
time.sleep(SCRIPT_SLEEP_S)


payload = molly.generate_transfer_tadeed_algo(
    ta_deed_idx=ta_deed_idx,
    ta_owner_addr=holly.acct.addr,
    ta_daemon_addr=daemon.acct.addr,
    micro_lat=45666353,
    micro_lon=-68691705,
)
print("")
print("")
time.sleep(SCRIPT_SLEEP_S)
print(
    "Molly creates and sends a TransferTadeedAlgo message to the GNodeFactory. The GNodeFactory validates that"
)
print("everything is in order, co-signs the deed transfer and submits it to the chain.")
terminal_asset = gnf.transfer_tadeed_algo_received(payload)
print("")
print("")
time.sleep(SCRIPT_SLEEP_S)
print(
    "At the end of the gnf.transfer_tadeed_algo_received(payload) method, after transfering the deed, "
)
print("the GNodeFactory releases two new active GNodes into the GridWorks ecosystem:")
print("")
print("")
time.sleep(SCRIPT_SLEEP_S)
print(
    f"     - A GNode of role `TerminalAsset` and alias {terminal_asset.alias} which represents Holly's heating system"
)
atomic_metering_node: BaseGNode = terminal_asset.parent()
print(
    f"     - A GNode of role `AtomicMeteringNode` and alias {atomic_metering_node.alias} which represents a future transaction agent"
)
print("        for Holly's heating system")

print("")
print(f"TerminalAsset parent: {atomic_metering_node}")
time.sleep(SCRIPT_SLEEP_S)
print(
    "Note that Molly and the GNodeFactory have access to the lat/lon information for Holly's TerminalAsset, but this is "
)
print("not public information.")
print("")
print("")
time.sleep(SCRIPT_SLEEP_S)
print(
    "What IS public is a little bit more information about the topology of the electric grid."
)
print("")
print("")
print("###################################################################")
print("# This completes Flow 2: Initial TaDeed")
print("###################################################################")
print("")
print("")
time.sleep(SCRIPT_SLEEP_S)
time.sleep(SCRIPT_SLEEP_S)
print(
    "In the next milestone, Holly will create a taTradingRights NFT and sign a Service Level Agreement(SLA) contract with a company that "
)
print(
    "will guarantee that her house stays warm, and that she pays a fixed-cost for heating which saves her money compared to"
)
print(
    " what she spends now. In exchange, the SLA company will get her taTradingRights NFT and provide it to cloud-based software agents"
)
print(
    "that can keep her house warm and use future weather and price forecasts to create real-time "
)
print("bids into energy markets for Holly's heating system. ")
print("")
print("")
time.sleep(SCRIPT_SLEEP_S)
