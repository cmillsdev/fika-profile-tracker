from helpers import load_json, id_lookup


def load_profile_random_quests(profile_id):
    return load_json(f'randomquests/{profile_id}/quests.json')

def random_quest_lookup(qid, pid):
    return load_profile_random_quests(pid)[qid]
    
def get_objectives(qid, pid):
    objectives_dict = random_quest_lookup(qid, pid)['conditions']['AvailableForFinish']
    condition_types = ['CounterCreator', 'HandoverItem', 'FindItem', 'LeaveItemAtLocation', 'Quest', 'PlaceBeacon', 'Skill', 'WeaponAssembly', 'TraderLoyalty', 'SellItemToTrader']
    
    for quest in objectives_dict.values():
        for condition in quest['conditions']['AvailableForFinish']:
            if condition['conditionType'] in condition_types:
                cond_type = condition['conditionType']
                if cond_type == 'FindItem':
                    print(f"{condition['value']} {id_lookup(condition['target'][0])}")

