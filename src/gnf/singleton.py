import time
import os
import subprocess
import sys
import random
import gnf.demo_methods as demo_methods

from gnf import load_dev_data

plant_names = ["holly"]

subprocess.run(["../sandbox/sandbox", "reset"])
subprocess.run("./reset-dev-db.sh")
load_dev_data.main()
demo_methods.certify_molly_metermaid()
holly = demo_methods.create_ta_owners(plant_names)[0]


