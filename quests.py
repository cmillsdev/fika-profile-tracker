from helpers import load_json, id_lookup
from httprequest import get_profile_quests

# active quests in profile, search id in random quests
def get_all_objectives(pid):
    profile_quests = get_profile_quests(pid)
    for quest in profile_quests:
        if quest['sptStatus'] == 2:
            print(quest['QuestName'])
            for condition in quest['conditions']['AvailableForFinish']:
                if condition['conditionType'] == 'CounterCreator':
                    continue
                print(f"{condition['conditionType']}:")
                for target in condition['target']:
                    print(f'{id_lookup(target)}')

def get_objectives(): # single quest lookup
    pass

def parse_objective(qid, pid):
    condition_types = ['CounterCreator', 'HandoverItem', 'FindItem', 'LeaveItemAtLocation', 
        'Quest', 'PlaceBeacon', 'Skill', 'WeaponAssembly', 'TraderLoyalty', 'SellItemToTrader']

def parse_counter_creator_task(task):
    pass

def parse_find_item_task(task): # FindItem or HandoverItem
    target_item = id_lookup(task['target'][0])
    num_required = task['value']
    fir = task['onlyFoundInRaid']

    print(num_required, target_item, fir)

def parse_leave_item_at_location_task(task):
    target_item = id_lookup(task['target'][0])
    num_required = task['value']
    location = task['zoneId']

    print(f'Place {num_required} {target_item} at {location}')

def parse_quest_task(task):
    pass

def parse_place_beacon_task(task):
    target_item = id_lookup(task['target'][0])
    location = task['zoneId']

    print(f'Place a {target_item} at {location}')

def parse_skill_task(task):
    pass

def parse_weapon_assembly_task(task):
    target_item = id_lookup(task['target'][0])
    print('Assemble a custom', target_item)

def parse_trader_loyalty_task(task):
    pass

def parse_sell_item_to_trader_task(task):
    pass

def parse_kill_task(task):
    # comparemethod for distance, target
    pass



