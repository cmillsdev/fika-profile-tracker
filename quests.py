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

def get_all_objectives(pid):
    profile_quests = get_profile_quests(pid)
    tasks_dict = []
    task_name = ''
    last_dict = []
    for quest in profile_quests:
        if quest['sptStatus'] == 2:  # Active quest
            task_name = id_lookup(quest['_id'])
            conditions_dict = []

            for condition in quest['conditions']['AvailableForFinish']:
                lup = id_lookup(condition['id'])
                if lup not in conditions_dict:
                    conditions_dict.append(lup)
        if task_name:
            if last_dict != conditions_dict:
                tasks_dict.append({"name": task_name, "conditions": conditions_dict})

            last_dict = conditions_dict
            
    return tasks_dict



def parse_condition(condition):
    condition_type = condition.get("conditionType")
    parser = CONDITION_PARSERS.get(condition_type)
    if parser:
        return parser(condition)
    else:
        print("No match for conditionType:", condition_type)

# Task parsing functions
def parse_exit_status_task(task):
    return "Survive and extract!"

def parse_visit_place_task(task):
    return f"Visit {task['target']}"

def parse_location_task(task):
    loc_string = ''
    for location in task['target']:
        loc_string = loc_string + f'{location}, '
    return loc_string[:-2]

def parse_equipment_task(task):
    equipment_string = ''
    for equip in task['equipmentInclusive']:
        equipment_string = equipment_string + f"{id_lookup(equip[0])}, "

    return equipment_string[:-2]

def parse_counter_creator_task(task):
    """
    Parse a CounterCreator task, handling nested conditions dynamically.
    """
    counter = task.get("counter", {})
    counter_id = counter.get("id", "Unknown Counter ID")
    #print(f"Processing CounterCreator: {counter_id}")

    # Iterate through each sub-condition in the counter
    conditions = counter.get("conditions", [])
    sub_list = []
    for sub_condition in conditions:
        condition_type = sub_condition.get("conditionType", "Unknown")
        #print(f"  Sub-condition: {condition_type}")

        # Dynamically parse sub-conditions using the existing parsers
        sub_list.append(parse_condition(sub_condition))

    # Print any additional metadata about the CounterCreator task
    # if "value" in task:
    #     print(f"# required: {task['value']}")
    return sub_list
    # if "type" in task:
    #    print(f"  Type: {task['type']}")

    #print("Completed parsing CounterCreator.\n")


def parse_find_item_task(task):  # FindItem or HandoverItem
    target_item = id_lookup(task['target'][0])
    num_required = task['value']
    fir = task['onlyFoundInRaid']
    fir_string = "FIR: Yes" if fir else "FIR: No"
    return [num_required, target_item, fir_string]

def parse_leave_item_at_location_task(task):
    target_item = id_lookup(task['target'][0])
    num_required = task['value']
    location = task['zoneId']
    return f'Place {num_required} {target_item} at {location}'

def parse_place_beacon_task(task):
    target_item = id_lookup(task['target'][0])
    location = task['zoneId']
    return f'Place a {target_item} at {location}'

def parse_weapon_assembly_task(task):
    target_item = id_lookup(task['target'][0])
    return 'Assemble a custom', target_item

def parse_quest_task(task):
    return f"Quest task: {id_lookup(task['id'])}"

def parse_kill_task(task):
    body_parts = task.get("bodyPart", None)
    target = "Scavs" if task["target"] == "Savage" else id_lookup(task['target'])
    return f"Kill {target} targeting {body_parts}"
