import json
import requests
import zlib
import time
import os
from utils.endpoint import Endpoint

CACHE_FILE = "client_locale_cache.json"
CACHE_TTL = 300  # Cache Time-to-Live in seconds (5 minutes)

def id_lookup(i):
    lookup = get_client_locale()['data']
    keys = [f"{i} Name", f"{i} name", i]
    
    for key in keys:
        if key in lookup:
            return lookup[key]
    return i

def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def http_request(sid, endpoint, write=False):
    url = "http://wafflefm:6969/"

    headers = {
        "Content-Type": "application/json",
        "Cookie": f"PHPSESSID={sid}",
    }

    response = requests.get(url + endpoint, headers=headers)

    if response.status_code == 200:
        try:
            # Decompress zlib-compressed response
            decompressed_data = zlib.decompress(response.content)
            decomp_json = json.loads(decompressed_data)
            if write:
                with open(f"{endpoint.replace('/', '-')}.json", 'w') as f:
                    json.dump(decomp_json, f, indent=4)
            return decomp_json
        except Exception as e:
            print(f"Error decompressing response: {e}")
    else:
        print(f"Error: {response.status_code}, {response.text}")
    return None

def is_cache_valid():
    if not os.path.exists(CACHE_FILE):
        return False
    cache_age = time.time() - os.path.getmtime(CACHE_FILE)
    return cache_age < CACHE_TTL

def get_client_locale():
    if is_cache_valid():
        # Read from cache
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    else:
        # Fetch new data and update cache
        data = http_request('', Endpoint.CLIENT_LOCALE)
        if data:
            with open(CACHE_FILE, 'w') as f:
                json.dump(data, f, indent=4)
        return data

def get_profile(pid):
    return http_request(pid, Endpoint.PROFILE)['data']

def get_all_players():
        return http_request('677df13900028976aab5cb0f', Endpoint.ALL_PROFILES)

def get_profile_quests(profile_id):
    return http_request(profile_id, Endpoint.QUESTS)['data']

def get_hideout_areas(profile_id):
    return http_request(profile_id, Endpoint.HIDEOUT_AREAS)['data']

def test_endpoint(endpoint, pid):
    with open(f'{endpoint.replace('/', '-')}.json', 'w') as f:
        r = http_request(pid, endpoint)
        json.dump(r, f, indent=4)

def dump_page_json(pid):
    from core.quests import get_all_objectives
    from core.hideout import get_all_hideout
    from core.stats import get_all_stats
    from core.overview import get_overview

    # "674e50640003077d50d67c44" iain
    # "674e8d5e000124d3a4adc638" me
    # "677df13900028976aab5cb0f" web profile

    objs = get_all_objectives(pid)
    print('Got objectives.')
    hideout = get_all_hideout(pid)
    print('Got hideout')
    stats = get_all_stats(pid)
    print('Got stats')
    overview = get_overview(pid)
    print('Got overview')

    dump = {"overview": overview, "stats": stats, "objectives": objs, "hideout": hideout}
    print('dumped')

    with open(f"pages-{pid}.json", 'w') as f:
        json.dump(dump, f, indent=4)