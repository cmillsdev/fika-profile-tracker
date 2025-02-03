from utils.helpers import id_lookup, get_profile
from core.stats import get_last_death, get_last_victims, get_accuracy, get_misc_info
from collections import defaultdict
import json

# -- todo
# task items to turn in
# do you need to heal
# last round info -- victims, death info, damagehistory
# hydration/energy
# insurance counter?
# generator
# flea offers
# raid review url

def get_overview(pid):
    profile = get_profile(pid)
    overview = defaultdict(dict)
    overview['basic'] = get_misc_info(profile)
    overview['overall_accuracy'] = get_accuracy(profile['Stats']['Eft']['OverallCounters']['Items'])
    overview['session_accuracy'] = get_accuracy(profile['Stats']['Eft']['SessionCounters']['Items'])
    overview['last_raid'] = get_last_round(profile)

    return overview

def get_last_round(profile):
    stats = defaultdict(dict)
    stats['last_death'] = get_last_death(profile['Stats']['Eft'].get('Aggressor'), profile['Stats']['Eft'].get('DeathCause'))
    stats['victims'] = get_last_victims(profile['Stats']['Eft']['Victims'])
    stats['damage_history'] = profile['Stats']['Eft']['DamageHistory']
    is_lethal = stats['damage_history'].get('LethalDamage')
    if is_lethal:
        stats['damage_history']['LethalDamage']['SourceId'] = id_lookup(stats['LethalDamage']['SourceId'])
    if stats.get('damage_history'):
        for bodypart in stats['damage_history']['BodyParts']:
            if stats['damage_history']['BodyParts'][bodypart]:
                for key, damage in enumerate(stats['damage_history']['BodyParts'][bodypart]):
                    stats['damage_history']['BodyParts'][bodypart][key]['SourceId'] = id_lookup(damage['SourceId'])
    return stats

def get_insurance(pid):
    pass

def get_basic_profile_info(profile):
    return get_misc_info(profile)