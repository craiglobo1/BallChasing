import requests
import os
import json
import time

MAX_COUNT = 200  # max count for replays defined in api docs

auth_token = os.getenv("BALLCHASING-API")

def parse_url_params(params : dict):
    return "?" + "&".join([ f"{key}={val}" for key, val in params.items()])

replays_params = {
    "count": MAX_COUNT, 
}

replays = requests.get(f"https://ballchasing.com/api/replays{parse_url_params(replays_params)}", headers={"Authorization": auth_token}).json()
# replays = json.load(open("example_req.json", "r"))

ids = [ replay["id"] for replay in replays["list"]]

start = time.time()

i = 0
while True:
    if i >= len(ids):
        print("hey")
        break
    req = requests.get(f"https://ballchasing.com/api/replays/{ids[i]}/file", headers={"Authorization": auth_token})

    with open(f"replays/{ids[i]}.replay", "wb+") as wf:
        wf.write(req.content)
    
    if req.status_code == 200:
        print(f"id_{i}: {time.time()-start:.4f}")
        start = time.time()
    elif req.status_code == 429:
        print(f"ERROR: Timeout ")
        print(req.json())
    else:
        print(req.json())

    i += 1