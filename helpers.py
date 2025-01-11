import json
from httprequest import http_request, get_client_locale
from endpoint import Endpoint

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