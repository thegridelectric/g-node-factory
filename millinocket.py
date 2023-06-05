import subprocess
import time

import gridworks.dev_utils.algo_setup as algo_setup
import requests
from rich.pretty import pprint

import gnf.config as config
import gnf.dev_utils.load_data as load_data


settings = config.GnfSettings()
#
# print("Resetting Algorand sandbox")
# subprocess.run(["../sandbox/sandbox", "reset"])
#
# print("")
# print("")
# print("Funding GnfAdminAddr")
# algo_setup.dev_fund_to_min(settings.public.gnf_admin_addr, 10)
#
#
print("")
print("")
print("Flushing GNodeFactory Database")
print("")
print("")
time.sleep(2)
subprocess.run("./reset-dev-db.sh")
#
# print("Starting the GNodeFactory RestAPI")
# print("")
# print("")

cmd = f"uvicorn  gnf.rest_api:app --reload  --port 8000"
gnf_pr = subprocess.Popen(cmd.split())
api_endpoint = "http://0.0.0.0:8000/"
gnf_up: bool = False
while not gnf_up:
    try:
        gnf_up = True
        requests.get(url=api_endpoint)
    except:
        gnf_up = False

print("")
print("")
print("Initializing GNodeFactory Database with Seed GNodes")
print("")
print("")
time.sleep(2)
load_data.millinocket()
print("")
print("")
print(
    "Check http://localhost:8000/base-g-nodes/ - should be 4 GNodes,including MarketMaker d1.isone.ver.keene, but no AtomicTNodes)"
)

print("Return to gridworks-atn repo now.")
print("")
print("")
time.sleep(2)

input(" HIT RETURN TO Stop Gnf API")

gnf_pr.terminate()
