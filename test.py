from utils.helpers import test_endpoint, get_profile, get_flea_prices
from utils.endpoint import Endpoint
from core.hideout import get_all_hideout
from core.overview import get_overview
from pprint import pprint

pid = '674e8d5e000124d3a4adc638'

# profile = Profile(get_profile(pid))
# print(profile.bonuses)
# #print(profile.skills.mastering)
#test_endpoint('launcher/profiles', '674e8d5e000124d3a4adc638')

# ep = [Endpoint.VERSION_EFT, Endpoint.VERSION_FIKA, Endpoint.VERSION_SPT]

# for e in ep:
#     test_endpoint(e, pid)


overview = get_overview(pid)
pprint(overview['last_raid']['last_death'])
#get_flea_prices()