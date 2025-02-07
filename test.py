from utils.helpers import test_endpoint, get_profile, get_flea_prices
from utils.endpoint import Endpoint
from core.hideout import get_all_hideout

pid = '674e8d5e000124d3a4adc638'

# profile = Profile(get_profile(pid))
# print(profile.bonuses)
# #print(profile.skills.mastering)
#test_endpoint('launcher/profiles', '674e8d5e000124d3a4adc638')

ep = ['client/game/profile/list']

for e in ep:
    test_endpoint(e, pid)

#get_flea_prices()