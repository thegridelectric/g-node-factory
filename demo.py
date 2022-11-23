import subprocess
import sys
import time

import requests
from rich.pretty import pprint

import gnf.config as config
import gnf.demo_methods as demo_methods
from gnf import load_dev_data
from gnf.dev_utils.algo_setup import dev_fund_admin_and_graveyard


# if len(sys.argv) == 1:
#     sim_size = 2
#     print("If you want to simulate n assets, run python demo.py n")
#     time.sleep(2)
# else:
#     try:
#         sim_size = int(sys.argv[1])
#     except:
#         raise Exception(
#             f"Please enter an integer number of homes to simulate, not {sys.argv[1]}"
#         )

sim_size = 4
full_plant_names = demo_methods.demo_plant_names
plant_names = full_plant_names[0:sim_size]

if sim_size == 0:
    raise Exception("No simulated TerminalAssets. Stopping")
elif sim_size == 1:
    print(f"Running simulation for 1 TerminalAsset (molly.ta)")
else:
    print(f"Running simulation for {sim_size} TerminalAssets")
time.sleep(2)
print("")
print("")
print("Resetting Algorand sandbox")

time.sleep(1)
subprocess.run(["../sandbox/sandbox", "reset"])

print("")
print("")
print("Funding the GNodeFactory")
print("")
print("")


dev_fund_admin_and_graveyard(config.GnfSettings())
print("")
print("")
print("Flushing GNodeFactory Database")
print("")
print("")
time.sleep(2)
subprocess.run("./reset-dev-db.sh")


print("")
print("")
print("Check http://localhost:8000/base-g-nodes/ - shoud be no GNodes.")
print("If page fails, make sure Gnf API is started up")
print("uvicorn  gnf.rest_api:app --reload  --port 8000")
input("HIT RETURN TO CONTINUE")
print("")
print("")
print("Initializing GNodeFactory Database with Seed GNodes")
print("")
print("")
time.sleep(2)
load_dev_data.main()
print("")
print("")
print(
    "There shoud now be 4 GNodes (including MarketMaker d1.isone.ver.keene, but no AtomicTNodes)"
)
input("HIT RETURN TO CONTINUE")
print("")
print("")
# print("Starting the GNodeFactory RestAPI")
# print("")
# print("")
# time.sleep(2)

# cmd = f"docker run -p 8000:8000 --name gnf-api jessmillar/gnf:chaos__b25e5f9__20221122"
# gnf_pr = subprocess.Popen(cmd.split())
# api_endpoint = "http://0.0.0.0:8000/"
# gnf_up: bool = False
# while not gnf_up:
#     try:
#         gnf_up = True
#         requests.get(url=api_endpoint)
#     except:
#         gnf_up = False
print("")
print("")
print("Certifying MollyMetermaid as a TaValidator")
print("")
print("")
time.sleep(2)

rr = demo_methods.certify_molly_metermaid()
pprint(rr)
if rr.HttpStatusCode > 200:
    # gnf_pr.terminate()
    raise Exception("Stopping demo due to errors")

print("")
print("")
print(f"Creating {sim_size} TaOwners")
print("")
print("")
time.sleep(2)
ta_owners = demo_methods.create_ta_owners(plant_names)
print("")
print("")
print(f"Creating {sim_size} TaDaemons")
print("")
print("")
time.sleep(2)
demo_methods.start_ta_owners(ta_owners)

print("")
print("")
print("TaDaemons are now running, each with their own RestAPI.")
print("")
print("")
time.sleep(2)
print("Any TaDeeds they own will show up at the following endpoints:")
print("")
print("")
for owner in ta_owners:
    print(
        f"Inspect {owner}'s deeds at http://localhost:{owner.settings.ta_daemon_api_port}/owned-tadeeds/"
    )

print("")
print("")
time.sleep(2)
print("They do not yet own any TaDeeds.")
print("")
print("")
time.sleep(2)
input("HIT RETURN TO CONTINUE")

print("")
print("")
print(f"Creating {sim_size} TerminalAssets")
print("")
print("")
time.sleep(2)

rr = demo_methods.create_terminal_assets(ta_owners)

if rr.HttpStatusCode == 200:

    print("Success!")
    print("")
    print("")
    time.sleep(2)
    print("TaDaemon Algorand addresses now hold TaDeeds on behalf of their TaOwners")
    print("")
    print("")
    time.sleep(2)
    print("Inspect them at:")

    for owner in ta_owners:
        print(
            f"Inspect {owner}'s deeds at http://localhost:{owner.settings.ta_daemon_api_port}/owned-tadeeds/"
        )

    print("")
    print("")
    time.sleep(2)
else:
    print("Something went wrong")
    print("")
    print("")

input("HIT RETURN TO CONTINUE")

print("")
print("")
print(f"Starting Time")
print("")
print("")

api_endpoint = f"http://0.0.0.0:8000/resume-time/"
r = requests.post(url=api_endpoint)

# api_endpoint = f"http://0.0.0.0:8000/pause-time/"
# r = requests.post(url=api_endpoint)

# cmd = "docker stop gnf-api"
# subprocess.run(cmd.split())
# # This stops the running docker container

# cmd = "docker rm gnf-api"
# subprocess.run(cmd.split())
# # This removes the stopped docker container

input("HIT RETURN TO STOP SIMULATION. TIME WILL STOP AFTER 2 DAYS")

for ta_owner in ta_owners:
    ta_owner.stop()  # Does the same
