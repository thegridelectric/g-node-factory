# HACK for resetting time coordinator to its initial time
# Won't work unless all GNodes listening to time are restarted (atn, marketmaker)
import requests


api_endpoint = "http://localhost:8000/debug-tc-reinitialize-time/"

r = requests.post(url=api_endpoint)
