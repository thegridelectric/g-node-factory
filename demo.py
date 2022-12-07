import subprocess
import sys
import time

import requests
from rich.pretty import pprint

import gnf.config as config
import gnf.demo_methods as demo_methods
import gnf.dev_utils.algo_setup as algo_setup
from gnf import load_dev_data


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
print("Funding the GNodeFactory, the Keene MarketMaker and Atn accts")
print("")
print("")

settings = config.GnfSettings()

algo_setup.dev_fund_admin_and_graveyard(settings)
algo_setup.dev_fund_account(
    settings=settings,
    to_addr=settings.public.keene_addr,
    amt_in_micros=10**6,
)

atn_address_list = [
    "4JHRDNY4F6RCVGPALZULZWZNVP3OKT3DATEOLINCGILVPGHUOFY7KCHVIQ",
    "YL3MAWSIST2DWX5GOTZYVX74GNSAVMX52RKSEDT4KIO644JCCRFTFKM5UM",
    "CWOLXCXZKLYLORBQQCI4AUHA5CLOLUXRDZEJZI4S3F6WUNVIAF4MX5EW4U",
    "R3PKD54UOAOW6MTPO7ECZ6YX4COQWN5BJM4OZIHYWFVVGAITM53RGUF6LI",
]

for addr in atn_address_list:
    algo_setup.dev_fund_account(
        settings=settings,
        to_addr=addr,
        amt_in_micros=25 * 10**6,
    )


print("")
print("")
print("Flushing GNodeFactory Database")
print("")
print("")
time.sleep(2)
subprocess.run("./reset-dev-db.sh")

# print("")
# print("")
# print("Starting the GNodeFactory RestAPI")
# print("")
# print("")

# cmd = f"uvicorn  gnf.rest_api:app --reload  --port 8000"
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
    for ta_owner in ta_owners:
        ta_owner.stop()  # Does the same
    raise Exception(
        f"Something went wrong creating TerminalAssets: {rr.HttpStatusCode}, {rr.Note}"
    )


print("")
print("")
print(
    "The AtomicTNodes do not yet own trading rights. Inspect trading right owners at:"
)
for owner in ta_owners:
    print(
        f"Inspect {owner}'s deeds at http://localhost:{owner.settings.ta_daemon_api_port}/trading-rights/"
    )

print("")
print("")


time.sleep(2)
input("HIT RETURN TO CONTINUE")
print("")
print("")
print(
    "In fact the AtomicTNodes do not exist yet. Go to http://d1-1.electricity.works:15672/#/queues"
)
print("")
print("")
time.sleep(1)
print("Username and password are the same:")
print("")
print("smqPublic")
print("")
print("")
time.sleep(1)
print(
    "You will only see the dummy queues, the world d1-Fxxx, and the market maker ...keene.F-xxx"
)
input("To start the atn actors (and time coordinator) in a docker instance, HIT RETURN")

cmd = "docker compose -f docker-actor.yml up -d"
subprocess.run(cmd.split())
time.sleep(2)
print("")
print("")
print("It takes about 5 seconds for them to shop up. Look for them at")
print("http://d1-1.electricity.works:15672/#/queues")
print(
    "Once their queues exist they ready to enter their Service Level Agreements and get their trading rights"
)
input("HIT RETURN TO CONTINUE")
rr = demo_methods.enter_slas(ta_owners)

if rr.HttpStatusCode == 200:
    print("")
    print("")
    time.sleep(2)
    print(
        "Daemons have transferred TradingRights to their AtomicTNodes. Inspect at above pages"
    )
    print("")
    print("")
else:
    cmd = "docker stop gnf-api"
    subprocess.run(cmd.split())
    cmd = "docker compose -f docker-actor.yml down"
    subprocess.run(cmd.split())
    raise Exception("Something went wrong entering Service Level Agreements")


print("")
print("")
print("The demo is now ready to start the simulated trading.")
print("")
time.sleep(2)
print("The AtomicTNodes have access to simulated weather and price forecasts for 2020")
print("")
time.sleep(2)
print("The MarketMaker has access to 2020 prices for Keene Rd")
print("")
time.sleep(2)
print("Once the simulation starts, time moves forward in hourly timesteps")
print("You can see time advancing in the marketmaker terminal window")
print("Or at the marketmaker API: http://localhost:7997/get-time/")
time.sleep(2)
print("The rabbit queues will also start to get busy")
print("http://d1-1.electricity.works:15672/#/queues")
print("")
time.sleep(2)

input("HIT RETURN TO START SIMULATED TIME")

print("")
print("")
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

time.sleep(2)
print("")
print("")
print("In another window, try python pause_time.py (and `python resume_time.py`)")
print("")
print("")
time.sleep(2)

input("HIT RETURN TO STOP SIMULATION AND TEAR DOWN TADAEMON DOCKER INSTANCES")

api_endpoint = f"http://0.0.0.0:8000/pause-time/"
r = requests.post(url=api_endpoint)

# gnf_pr.terminate()
cmd = "docker compose -f docker-actor.yml down"
subprocess.run(cmd.split())

for ta_owner in ta_owners:
    ta_owner.stop()  # Does the same
