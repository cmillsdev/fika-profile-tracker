import requests
import json
import zlib
import time

from endpoint import Endpoint

# session_id = "674e50640003077d50d67c44" me
# session_id = "677df13900028976aab5cb0f" web profile

def get_all_players():
    return http_request('677df13900028976aab5cb0f', Endpoint.ALL_PROFILES)

def http_request(sid, endpoint, write=False):
    url = "http://192.168.1.238:6969/"

    headers = {
        "Content-Type": "application/json",
        "Cookie": f"PHPSESSID={sid}",
    }

    response = requests.get(url+endpoint, headers=headers)

    if response.status_code == 200:
        try:
            # Decompress zlib-compressed response
            decompressed_data = zlib.decompress(response.content)
            decomp_json = json.loads(decompressed_data)
            if write:
                with open(f"{endpoint.replace('/', '-')}.json", 'w') as f:
                    json.dump(decomp_json, f, indent=4)
            return decomp_json
        except:
                print(f"Error decompressing response")
    else:
        print(f"Error: {response.status_code}, {response.text}")

print(get_all_players())