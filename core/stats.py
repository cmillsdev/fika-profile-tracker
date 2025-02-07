from utils.helpers import id_lookup, get_profile, get_profile_quests, get_percent
from collections import defaultdict
from core.hideout import get_all_hideout
import json
# inventory count - figure out how to break it down by category
# get damage history

def get_all_stats(pid, profile):
    stats = defaultdict(dict)
    stats['cheevos'] = get_cheevos(profile)
    stats['inv_len'] = get_inventory_count(profile)
    stats['encyc_len'] = get_encyclopedia(profile)
    stats['misc'] = get_misc_info(profile)
    
    stats['overall_counters'] = get_counters(profile['Stats']['Eft']['OverallCounters']['Items'])
    stats['session_counters'] = get_counters(profile['Stats']['Eft']['SessionCounters']['Items'])
    stats['skills_common'] = get_skills_common(profile['Skills']['Common'])
    stats['skills_mastering'] = get_skills_mastering(profile['Skills']['Mastering'])
    stats['bonuses'] = get_profile_bonuses(profile['Bonuses'])
    stats['mini_quest_info'] = get_mini_quest_info(profile['Quests'])
    stats['last_death'] = get_last_death(profile['Stats']['Eft'].get('Aggressor'), profile['Stats']['Eft'].get('DeathCause'))
    stats['victims'] = get_last_victims(profile['Stats']['Eft']['Victims'])
    stats['traders'] = get_trader_info(profile['TradersInfo'])
    stats['hideout'] = get_all_hideout(pid)
    stats['overall_accuracy'] = get_accuracy(profile['Stats']['Eft']['OverallCounters']['Items'])
    stats['session_accuracy'] = get_accuracy(profile['Stats']['Eft']['SessionCounters']['Items'])
    return stats

def get_profile_bonuses(bonuses):
    bonii = []
    for bonus in bonuses:
        bonii.append({'type': bonus['type'], 'value': bonus.get('value', 0)})

    return bonii

def get_trader_info(trader_info):
    traders = defaultdict(dict)
    # calculate trader loyaltyf
    for trader in trader_info.keys():
        nickname = id_lookup(f"{trader} Nickname")
        traders[nickname] = {'standing': trader_info[trader]['standing'], 'sales_sum': trader_info[trader]['salesSum']}

    return traders

def get_last_death(killer=None, cause=None):
    try:
        if killer:
            killer = {'name': killer['Name'], 'side': killer['Side'], 'BodyPart': killer['ColliderType'], 'weapon': id_lookup(killer['WeaponName'])}
        if cause:
            cause = {'damage_type': cause['DamageType'], 'weapon': id_lookup(f"{cause['WeaponId']} ShortName")}
        return {'killer': killer, 'cause': cause}
    except:
        return []

def get_last_victims(last_victims):
    victims = []
    for victim in last_victims:
        victims.append({'time':victim['Time'], 'name': victim['Name'], 'side': victim['Side'], 'level': victim['Level'], 'body_part': victim['BodyPart'], 'weapon': id_lookup(victim['Weapon']), 'distance': victim['Distance']})
    return victims

def get_mini_quest_info(profile_quests):
    #total_quests = len(get_profile_quests(pid)) - only total for profile
    # get total somehow
    active = 0
    finished = 0
    for quest in profile_quests:
        if quest['status'] == 4:
            finished += 1
        if quest['status'] == 2:
            active += 1

    return {'active': active, 'finished': finished}

def get_accuracy(counters):
    reached = 0
    used = 0
    for counter in counters:
        if "AmmoUsed" in counter['Key']:
            used = counter['Value']
        if "AmmoReached" in counter['Key']:
            reached = counter['Value']
    return f"{get_percent(reached, used):.2f}%"

def get_counter(counters, key):
    for k in counters:
        if key in k['Key']:
            value = k['Value']
            return value
    return None

def get_counters(counters):
    overall = defaultdict(dict)
    looted_items = []
    for counter in counters:
        counter_string = ''
        if 'LootItem' in counter['Key']:
            for key in counter['Key']:
                if key != 'LootItem':
                    counter_string += f"{id_lookup(key)}"
            looted_items.append(f"{counter['Value']}x {counter_string}")
        else:
            for key in counter['Key']:
                counter_string += f"/{id_lookup(key)}"
            overall[counter_string] = counter['Value']
    if looted_items:
        overall['looted_items'] = looted_items
    return overall

def get_misc_info(profile):
    stats = defaultdict(dict)
    stats['exp_gained'] = profile['Info']['Experience']
    stats['level'] = profile['Info']['Level']
    stats['reg_date'] = profile['Info']['RegistrationDate']
    stats['faction'] = profile['Info']['Side']
    stats['nickname'] = profile['Info']['Nickname']
    stats['total_insured_items'] = len(profile['InsuredItems'])
    stats['ragfair_rating'] = f"{profile['RagfairInfo']['rating']:.2f}"
    stats['survivor_class'] = profile['Stats']['Eft']['SurvivorClass']
    stats['ingame_time'] = profile['Stats']['Eft']['TotalInGameTime']
    stats['scav_karma'] = profile['karmaValue']
    stats['car_extract_count'] = profile['CarExtractCounts']
    return stats

def get_cheevos(profile):
    cheevos = defaultdict(dict)
    for cheevo in profile["Achievements"].keys():
        name = id_lookup(f'{cheevo} name')
        desc = id_lookup(f'{cheevo} description')
        cheevos[name] = desc
    return cheevos

def get_inventory_count(profile):
    return len(profile['Inventory']['items'])

def get_encyclopedia(profile):
    encyclopedia = profile["Encyclopedia"]
    total = len(encyclopedia)
    examined = 0
    for e in encyclopedia:
        if not encyclopedia[e]:
            examined += 1
    return f"{examined}/{total}"

# stats = get_all_stats('674e50640003077d50d67c44')
# with open('stats.json', 'w') as f:
#     json.dump(stats, f, indent=4)
# # 674e50640003077d50d67c44 -iain
# # 674e8d5e000124d3a4adc638 -me