from collections import defaultdict
from utils.helpers import id_lookup, get_hideout_areas


def get_all_hideout(pid, hideout_profile):
    hideout_templates = get_hideout_templates(pid)
    areas = defaultdict(dict)
    for area in hideout_profile["Areas"]:
        area_type = get_area_type(area['type'])
        current_level = area["level"]
        areas[area_type]["current_level"] = current_level
        areas[area_type]["next_required"] = get_next_level_requirements(hideout_templates, area['type'], current_level+1)
    return areas

def get_next_level_requirements(hideout_templates, area_num, next_level):
    requirements = defaultdict(dict)
    for template in hideout_templates:
        if template["type"] == int(area_num):
            if template['stages'].get(str(next_level)):
                for required in template["stages"][str(next_level)]["requirements"]:
                    # requirement types: Area, Item, Skill, TraderLoyalty, 
                    if required['type'] == 'Area':
                        requirements[get_area_type(required['areaType'])] = required['requiredLevel']
                    elif required['type'] == 'Item':
                        requirements[id_lookup(required['templateId'])] = required['count']
                    elif required['type'] == 'Skill':
                        requirements[required['skillName']]= required['skillLevel']
                    elif required['type'] == 'TraderLoyalty':
                        requirements[id_lookup(required['traderId']+" Nickname")] = f"LL{required['loyaltyLevel']}"
                    else:
                        print(required['type'])
    if requirements:
        return requirements
    else:
        return {}

def get_hideout_templates(pid):
    return get_hideout_areas(pid)

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