import json

def load_lookup():
    with open('idlookup.json', 'r') as f:
        return json.load(f)

def id_lookup(i):
    lookup = load_lookup()
    return lookup[i]

def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)