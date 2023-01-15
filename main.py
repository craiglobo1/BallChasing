import requests
import os
import json
import time

MAX_COUNT = 200  # max count for replays defined in api docs

auth_token = os.getenv("BALLCHASING-API")

def parse_url_params(params : dict):
    return "?" + "&".join([ f"{key}={val}" for key, val in params.items()])

done_ids = set([ file[:-7] for file in os.listdir("replays")])

replays_params = {
    "count": MAX_COUNT, 
}

replays = requests.get(f"https://ballchasing.com/api/replays{parse_url_params(replays_params)}", headers={"Authorization": auth_token}).json()
ids = [ replay["id"] for replay in replays["list"]]

# removes ids that have been done
ids = list(set(ids)-done_ids)
print(f"[NEW] Replenishing {len(ids)}")

start = time.time()

i = 0
total_count= 0

while True:
    while i >= len(ids):
        new_replays = requests.get(f"https://ballchasing.com/api/replays{parse_url_params(replays_params)}", headers={"Authorization": auth_token}).json()
        new_ids = [ replay["id"] for replay in replays["list"]]
        # removes ids that have been done
        ids = list((set(new_ids)-set(ids))-done_ids)
        print(f"[NEW] Replenishing {len(ids)}")
        i = 0

    req = requests.get(f"https://ballchasing.com/api/replays/{ids[i]}/file", headers={"Authorization": auth_token})

    if req.status_code == 200:
        with open(f"replays/{ids[i]}.replay", "wb+") as wf:
            wf.write(req.content)
        total_count += 1
        print(f"id_{total_count}: {time.time()-start:.4f}")
        start = time.time()
    # when times out due to rate limiting may add something later
    elif req.status_code == 429:
        print(f"ERROR: {req.json()['error']}")
    else:
        print(f"ERROR: {req.json()['error']}")

    i += 1