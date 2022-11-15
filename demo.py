import time
import os
import subprocess
import sys
import random
import gnf.demo_methods as demo_methods

from gnf import load_dev_data
from rich.pretty import pprint

if len(sys.argv) == 1:
    sim_size = 5

try:
    sim_size = int(sys.argv[1])
except:
    raise Exception(f"Please enter an integer number of homes to simulate, not {sys.argv[1]}")

full_plant_names = demo_methods.demo_plant_names
full_plant_names.remove("holly")
random.shuffle(full_plant_names)
plant_names = ["holly"] + full_plant_names[0:sim_size - 1]

print(f"Running simulation for {sim_size} TerminalAssets")
time.sleep(2)
print("")
print("")
print("Resetting sandbox and dev database")
print("")
print("")
time.sleep(1)
subprocess.run(["../sandbox/sandbox", "reset"])

subprocess.run("./reset-dev-db.sh")

print("")
print("")
print("Initializing GNodeFactory Database")
print("")
print("")
time.sleep(2)
load_dev_data.main()

print("")
print("")
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
demo_methods.start_ta_owners(ta_owners)
print("")
print("")
print("Sleeping a bit for daemon APIs to start up, then creating TerminalAssets")
time.sleep(5)
print("")
print("")

rr = demo_methods.create_terminal_assets(ta_owners)


print("Success!")


for ta_owner in ta_owners:
    ta_owner.stop()
