from profile import Profile
from helpers import id_lookup, load_json
from quests import get_objectives

my_profile = Profile(load_json('profiles/674e8d5e000124d3a4adc638.json'))

print(get_objectives('59674cd986f7744ab26e32f2', my_profile.profile_id))