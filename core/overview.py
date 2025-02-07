from utils.helpers import id_lookup, get_profile
from core.stats import get_last_death, get_last_victims, get_accuracy, get_misc_info, get_counter
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
    overview['overall']['accuracy'] = get_accuracy(profile['Stats']['Eft']['OverallCounters']['Items'])
    overview['session']['accuracy'] = get_accuracy(profile['Stats']['Eft']['SessionCounters']['Items'])
    overview['overall']['kills'] = get_counter(profile['Stats']['Eft']['OverallCounters']['Items'], "Kills")
    overview['overall']['deaths'] = get_counter(profile['Stats']['Eft']['OverallCounters']['Items'], "Deaths")
    overview['session']['kills'] = get_counter(profile['Stats']['Eft']['SessionCounters']['Items'], "Kills")
    overview['session']['deaths'] = get_counter(profile['Stats']['Eft']['SessionCounters']['Items'], "Deaths")
    overview['overall']['raids'] = get_counter(profile['Stats']['Eft']['OverallCounters']['Items'], ["Sessions", "PMC"])
    overview['session']['kd'] = get_kd_ratio((get_counter(profile['Stats']['Eft']['SessionCounters']['Items'], "Kills") or 0), (get_counter(profile['Stats']['Eft']['SessionCounters']['Items'], "Deaths") or 0))
    overview['overall']['kd'] = get_kd_ratio((get_counter(profile['Stats']['Eft']['OverallCounters']['Items'], "Kills") or 0), (get_counter(profile['Stats']['Eft']['OverallCounters']['Items'], "Deaths") or 0))
    overview['last_raid'] = get_last_round(profile)

    return overview

def get_last_round(profile):
    stats = defaultdict(dict)
    stats['last_death'] = get_last_death(profile['Stats']['Eft'].get('Aggressor'), profile['Stats']['Eft'].get('DeathCause'))
    stats['victims'] = get_last_victims(profile['Stats']['Eft']['Victims'])
    stats['damage_history'] = profile['Stats']['Eft']['DamageHistory']
    is_lethal = stats['damage_history'].get('LethalDamage')
    if is_lethal:
        stats['damage_history']['LethalDamage'] = id_lookup(stats['LethalDamage'].get('SourceId'))
    if stats.get('damage_history'):
        for bodypart in stats['damage_history']['BodyParts']:
            if stats['damage_history']['BodyParts'][bodypart]:
                for key, damage in enumerate(stats['damage_history']['BodyParts'][bodypart]):
                    stats['damage_history']['BodyParts'][bodypart][key]['SourceId'] = id_lookup(damage['SourceId'])
    return stats

def get_kd_ratio(kills, deaths):
    if not deaths:
        return kills
    return round((kills/deaths),1)

def get_insurance(pid):
    pass

def get_basic_profile_info(profile):
    return get_misc_info(profile)