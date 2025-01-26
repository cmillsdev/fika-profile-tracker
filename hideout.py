import json
from helpers import load_json, id_lookup
from httprequest import get_hideout_areas, get_profile


def get_all_hideout(pid):
    hideout_profile = get_profile(pid)[0]["Hideout"]
    hideout_areas = get_hideout_areas(pid)
    
    areas = {}
    for area in hideout_profile["Areas"][0]:
        area_type = get_area_type(area['type'])
        areas[area_type]["level"] = area["level"]
        requirements = []
        for template in hideout_areas:
            if template['type'] == area['type']:
                
        


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
        "PLACE OF FAME",
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