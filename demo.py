import os
import subprocess
import sys
import time

from rich.pretty import pprint

import gnf.demo_methods as demo_methods
from gnf import load_dev_data


if len(sys.argv) == 1:
    sim_size = 2
    print("If you want to simulate n assets, run python demo.py n")
    time.sleep(2)
else:
    try:
        sim_size = int(sys.argv[1])
    except:
        raise Exception(
            f"Please enter an integer number of homes to simulate, not {sys.argv[1]}"
        )

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
print("Flushing GNodeFactory Database")
print("")
print("")
time.sleep(2)
subprocess.run("./reset-dev-db.sh")

print("")
print("")
print("Initializing GNodeFactory Database with Seed GNodes")
print("")
print("")
time.sleep(2)
load_dev_data.main()

print("Certifying MollyMetermaid as a TaValidator")
print("")
print("")
time.sleep(2)

demo_methods.certify_molly_metermaid()

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
input("Type any key to continue the demo")

print("")
print("")
print(f"Creating {sim_size} TerminalAssets")
print("")
print("")
time.sleep(2)

rr = demo_methods.create_terminal_assets(ta_owners)


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
input("Type any key to terminate daemon docker instances")

for ta_owner in ta_owners:
    ta_owner.stop()
