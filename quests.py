from helpers import load_json, id_lookup
from httprequest import http_request
from endpoint import Endpoint

def load_profile_quests(profile_id):
    return http_request(profile_id, Endpoint.QUESTS)['data']

def load_profile_random_quests(profile_id):
    return load_json(f'randomquests/{profile_id}/quests.json')

def random_quest_lookup(qid, pid):
    return load_profile_random_quests(pid)[qid]
    
def get_objectives(qid, pid):
    objectives_dict = random_quest_lookup(qid, pid)['conditions']['AvailableForFinish']
    condition_types = ['CounterCreator', 'HandoverItem', 'FindItem', 'LeaveItemAtLocation', 'Quest', 'PlaceBeacon', 'Skill', 'WeaponAssembly', 'TraderLoyalty', 'SellItemToTrader']
    print(objectives_dict) 
    for quest in objectives_dict[0].values():
        print(quest)
        for condition in quest:
            print(condition)
            if condition['conditionType'] in condition_types:
                cond_type = condition['conditionType']
                if cond_type == 'FindItem':
                    print(f"{condition['value']} {id_lookup(condition['target'][0])}")

# active quests in profile, search id in random quests
def get_all_objectives(pid):
    profile_quests = load_profile_quests(pid)
    quest_randomizer = load_profile_random_quests(pid)
    for quest in profile_quests:
        if quest['sptStatus'] == 2:
            print(quest['QuestName'])
            for condition in quest['conditions']['AvailableForFinish']:
                if condition['conditionType'] == 'CounterCreator':
                    continue
                print(f"{condition['conditionType']}:")
                for target in condition['target']:
                    print(f'{id_lookup(target)}')


