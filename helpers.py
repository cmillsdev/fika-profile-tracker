import json
from httprequest import http_request, get_client_locale
from endpoint import Endpoint

def id_lookup(i):
    lookup = get_client_locale()['data']
    return lookup[i+' Name']

def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)