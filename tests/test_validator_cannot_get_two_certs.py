from algosdk.v2client.algod import AlgodClient

import gnf.algo_utils as algo_utils
import gnf.config as config
import gnf.dev_utils.algo_setup as algo_setup
from gnf.dev_utils import DevValidator


# from gnf import GNodeFactoryDb


# TODO
# def testValidatorCertCreation():
#     settingsAlgo = config.Algo()
#     gnfSettings = config.GnfSettings()

#     client: AlgodClient = algo_utils.getAlgodClient(settingsAlgo)
#     algo_setup.devFundAdminAndGraveyard(gnfSettings)
#     gnf = GNodeFactoryDb(gnfSettings)

#     admin = gnf.adminAccount

#     molly = DevValidator(config.MollyMetermaidSettings())
#     multi = gnf.getValidatorAccountWithAdmin(molly.acct.addr)

#     payload = molly.generateCreateTavalidatorcertAlgo()

#     certIdx = gnf.CreateTavalidatorcertAlgoReceived(payload)

#     # Check that the joint account created the cert
#     createdAssets = client.account_info(multi.addr)["created-assets"]

#     mollyCerts = list(filter(lambda x: x["params"]["creator"] == multi.addr, createdAssets))

#     assert len(mollyCerts) == 1
#     assert mollyCerts[0]["index"] == certIdx

#     assert mollyCerts[0]["params"]["unit-name"] == "VLDTR"
#     assert mollyCerts[0]["params"]["manager"] == admin.addr

#     # If Molly sends another CreateTavalidatorcertAlgo request,
#     # gnf does not make a second cert

#     algo_setup.devFundAccount(config.Algo(), molly.acct.addr, 100 * 10**6)
#     payload2 = molly.generateCreateTavalidatorcertAlgo()
#     certIdx2 = gnf.CreateTavalidatorcertAlgoReceived(payload2)

#     assert certIdx2 == certIdx
#     mollyAdminCreatedCerts = list(
#         filter(lambda x: x["params"]["creator"] == multi.addr, createdAssets)
#     )
#     assert len(mollyAdminCreatedCerts) == 1
