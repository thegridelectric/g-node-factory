import requests


api_endpoint = f"http://0.0.0.0:8000/pause-time/"
r = requests.post(url=api_endpoint)
