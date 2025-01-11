from helpers import load_json, id_lookup
from httprequest import get_profile_quests

# Map condition types to functions
CONDITION_PARSERS = {
    "Kills": lambda task: parse_kill_task(task),
    "VisitPlace": lambda task: parse_visit_place_task(task),
    "FindItem": lambda task: parse_find_item_task(task),
    "HandoverItem": lambda task: parse_find_item_task(task),
    "PlaceBeacon": lambda task: parse_place_beacon_task(task),
    "LeaveItemAtLocation": lambda task: parse_leave_item_at_location_task(task),
    "WeaponAssembly": lambda task: parse_weapon_assembly_task(task),
    "CounterCreator": lambda task: parse_counter_creator_task(task),
    "Location": lambda task: parse_location_task(task),
    "Equipment": lambda task: parse_equipment_task(task),
    "Quest": lambda task: parse_quest_task(task),
    "ExitStatus": lambda task: parse_exit_status_task(task)
}

def remove_rainbow_formatting(fir):
    return fir.replace("<color=#ff0000>f</color><color=#ff6d00>o</color><color=#ffdb00>u</color><color=#b6ff00>n</color><color=#49ff00>d</color><color=#00ff24> </color><color=#00ff92>i</color><color=#00ffff>n</color><color=#0092ff> </color><color=#0024ff>r</color><color=#4900ff>a</color><color=#b600ff>i</color><color=#ff00db>d</color><color=#ff006d> </color>", "FOUND IN RAID ")
# Entry point for processing profile quests
def get_all_objectives(pid):
    profile_quests = get_profile_quests(pid)
    for quest in profile_quests:
        if quest['sptStatus'] == 2:  # Active quest
            print(id_lookup(quest['_id']))
            for condition in quest['conditions']['AvailableForFinish']:
                print(remove_rainbow_formatting(id_lookup(condition['id']))) # get task description for locale
                parse_condition(condition)
            print("\n")

def parse_condition(condition):
    condition_type = condition.get("conditionType")
    parser = CONDITION_PARSERS.get(condition_type)
    if parser:
        parser(condition)
    else:
        print("No match for conditionType:", condition_type)

# Task parsing functions
def parse_exit_status_task(task):
    print("Survive and extract!")

def parse_visit_place_task(task):
    print(f"Visit {task['target']}")

def parse_location_task(task):
    loc_string = ''
    for location in task['target']:
        loc_string = loc_string + f'{location}, '
    print(loc_string[:-2])

def parse_equipment_task(task):
    equipment_string = ''
    for equip in task['equipmentInclusive']:
        equipment_string = equipment_string + f"{id_lookup(equip[0])}, "

    print(equipment_string[:-2])

def parse_counter_creator_task(task):
    """
    Parse a CounterCreator task, handling nested conditions dynamically.
    """
    counter = task.get("counter", {})
    counter_id = counter.get("id", "Unknown Counter ID")
    #print(f"Processing CounterCreator: {counter_id}")

    # Iterate through each sub-condition in the counter
    conditions = counter.get("conditions", [])
    for sub_condition in conditions:
        condition_type = sub_condition.get("conditionType", "Unknown")
        #print(f"  Sub-condition: {condition_type}")

        # Dynamically parse sub-conditions using the existing parsers
        parse_condition(sub_condition)

    # Print any additional metadata about the CounterCreator task
    if "value" in task:
        print(f"# required: {task['value']}")
    # if "type" in task:
    #    print(f"  Type: {task['type']}")

    #print("Completed parsing CounterCreator.\n")


def parse_find_item_task(task):  # FindItem or HandoverItem
    target_item = id_lookup(task['target'][0])
    num_required = task['value']
    fir = task['onlyFoundInRaid']
    fir_string = "FIR: Yes" if fir else "FIR: No"
    print(num_required, target_item, fir_string)

def parse_leave_item_at_location_task(task):
    target_item = id_lookup(task['target'][0])
    num_required = task['value']
    location = task['zoneId']
    print(f'Place {num_required} {target_item} at {location}')

def parse_place_beacon_task(task):
    target_item = id_lookup(task['target'][0])
    location = task['zoneId']
    print(f'Place a {target_item} at {location}')

def parse_weapon_assembly_task(task):
    target_item = id_lookup(task['target'][0])
    print('Assemble a custom', target_item)

def parse_quest_task(task):
    print(f"Quest task: {id_lookup(task['id'])}")

def parse_kill_task(task):
    body_parts = task.get("bodyPart", None)
    target = "Scavs" if task["target"] == "Savage" else id_lookup(task['target'])
    print(f"Kill {target} targeting {body_parts}")
