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
    overview['overall_accuracy'] = get_accuracy(profile[0]['Stats']['Eft']['OverallCounters']['Items'])
    overview['session_accuracy'] = get_accuracy(profile[0]['Stats']['Eft']['SessionCounters']['Items'])
    overview['task_items'] = get_task_items_in_stash(profile[0]["Inventory"])
    overview['health'] = get_health_and_hunger(profile[0]["Health"])
    overview['last_raid'] = get_last_round(profile)

    return overview

def get_task_items_in_stash(inventory):
    quest_items = []
    quest_stash_id = inventory["questRaidItems"]
    for item in inventory["items"]:
        if item.get("parentId") == quest_stash_id:
            quest_items.append(id_lookup(item['_tpl']))

    return quest_items

def get_health_and_hunger(health):
    hp_hunger = defaultdict(dict)
    hp_hunger['health'] = health['BodyParts']
    hp_hunger['energy'] = health['Energy']
    hp_hunger['hydration'] = health['Hydration']
    return hp_hunger

def get_last_round(profile):
    stats = defaultdict(dict)
    stats['last_death'] = get_last_death(profile[0]['Stats']['Eft'].get('Aggressor'), profile[0]['Stats']['Eft'].get('DeathCause'))
    stats['victims'] = get_last_victims(profile[0]['Stats']['Eft']['Victims'])
    stats['damage_history'] = profile[0]['Stats']['Eft']['DamageHistory']
    is_lethal = stats['damage_history'].get('LethalDamage')
    if is_lethal:
        stats['damage_history']['LethalDamage']['SourceId'] = id_lookup(stats['LethalDamage']['SourceId'])
    if stats.get('damage_history'):
        for bodypart in stats['damage_history']['BodyParts']:
            if stats['damage_history']['BodyParts'][bodypart]:
                for damage in bodypart:
                    stats['damage_history']['BodyParts'][bodypart][damage]['SourceId'] = id_lookup(stats['damage_history']['BodyParts'][bodypart][damage]['SourceId'])
    return stats

def get_insurance(pid):
    pass

def get_basic_profile_info(profile):
    return get_misc_info(profile)