from collections import defaultdict
from utils.helpers import get_profile, get_percent, id_lookup
# healing/repairing/topping up/hunger&thirst
def get_alerts(pid):
    profile = get_profile(pid)

    task_items = get_task_items_in_stash(profile["Inventory"])
    health = is_player_healthy(profile['Health']['BodyParts'])
    energy = is_player_fed_or_watered(profile['Health']['Energy'])
    hydration = is_player_fed_or_watered(profile['Health']['Hydration'])
    alerts = {'task_items': task_items, 'health': health, 'energy': energy, 'hydration': hydration}
    print(alerts)
    return alerts

def are_mags_reloaded(mags):
    pass

def is_player_healthy(bodyparts):
    for bodypart in bodyparts:
        if get_percent(bodyparts[bodypart]['Health']['Current'], bodyparts[bodypart]['Health']['Maximum']) < 100:
            return False
    return True

def is_gear_repaired(gear):
    pass

def is_player_fed_or_watered(nut):
    if get_percent(nut['Current'], nut['Maximum']) < 85:
        return False
    return True

def is_player_hungry(hunger):
    pass

def get_task_items_in_stash(inventory):
    quest_items = []
    quest_stash_id = inventory["questRaidItems"]
    for item in inventory["items"]:
        if item.get("parentId") == quest_stash_id:
            quest_items.append(id_lookup(item['_tpl']))

    return quest_items
