from utils.endpoint import Endpoint
from utils.helpers import http_request

def get_version(pid):
    eft = http_request(pid, Endpoint.VERSION_EFT)['data']['latestVersion']
    spt = http_request(pid, Endpoint.VERSION_SPT)
    fika = http_request(pid, Endpoint.VERSION_FIKA)['version']

    return {'eft':eft, 'spt':spt, 'fika':fika}