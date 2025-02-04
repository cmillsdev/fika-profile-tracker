import json
from collections import defaultdict
from utils.helpers import load_json, id_lookup, get_hideout_areas, get_profile


def get_all_hideout(pid):
    hideout_profile = get_hideout_profile(pid)
    hideout_templates = get_hideout_templates(pid)
    
    areas = defaultdict(dict)
    for area in hideout_profile["Areas"]:
        area_type = get_area_type(area['type'])
        current_level = area["level"]
        areas[area_type]["current_level"] = current_level

        areas[area_type]["required"] = get_next_level_requirements(pid, hideout_templates, area['type'], current_level+1)

    return areas

def get_next_level_requirements(pid, hideout_templates, area_num, next_level):
    requirements = []
    for template in hideout_templates:
        if template["type"] == int(area_num):
            if template['stages'].get(str(next_level)):
                for required in template["stages"][str(next_level)]["requirements"]:
                    # requirement types: Area, Item, Skill, TraderLoyalty, 
                    if required['type'] == 'Area':
                        requirements.append(f"L{required['requiredLevel']} {get_area_type(required['areaType'])}")
                    elif required['type'] == 'Item':
                        requirements.append(f"{required['count']} {id_lookup(required['templateId'])}")
                    elif required['type'] == 'Skill':
                        requirements.append(f"L{required['skillLevel']} {required['skillName']}")
                    elif required['type'] == 'TraderLoyalty':
                        requirements.append(f'''LL{required['loyaltyLevel']} {id_lookup(required['traderId']+" Nickname")}''')
                    else:
                        print(required['type'])

    return requirements

def get_hideout_templates(pid):
    return get_hideout_areas(pid)

def get_hideout_profile(pid):
    return get_profile(pid)["Hideout"]

def get_area_type(area_num):
    area_types = [
        "VENTS",
        "SECURITY",
        "LAVATORY",
        "STASH",
        "GENERATOR",
        "HEATING",
        "WATER COLLECTOR",
        "MEDSTATION",
        "NUTRITION UNIT",
        "REST SPACE",
        "WORKBENCH",
        "INTELLIGENCE CENTER",
        "SHOOTING RANGE",
        "LIBRARY",
        "SCAV CASE",
        "ILLUMINATION",
        "HALL OF FAME",
        "AIR FILTERING UNIT",
        "SOLAR POWER",
        "BOOZE GENERATOR",
        "BITCOIN FARM",
        "CHRISTMAS TREE",
        "BROKEN WALL",
        "GYM",
        "WEAPON WALL",
        "SECONDARY WEAPON WALL",
        "GEAR RACK",
        "CULTIST CIRCLE"
    ]

    return area_types[area_num]