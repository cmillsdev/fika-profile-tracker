import json
from httprequest import http_request
from endpoint import Endpoint

def load_lookup():
    return http_request('', Endpoint.CLIENT_LOCALE)

def id_lookup(i):
    lookup = load_lookup()['data']
    return lookup[i+' Name']

def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)