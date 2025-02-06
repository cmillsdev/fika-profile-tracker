from utils.helpers import load_json, id_lookup, get_profile_quests, get_profile
from collections import defaultdict

def get_all_objectives(pid, profile):
    profile_quests = get_profile_quests(pid)
    tasks_dict = defaultdict(dict)
    task_name = ''
    last_dict = []
    for quest in profile_quests:
        if quest['sptStatus'] == 2:  # Active quest
            qid = quest["_id"]
            task_name = id_lookup(quest['_id'])
            conditions_dict = []

            for condition in quest['conditions']['AvailableForFinish']:
                cid = condition['id']
                lup = id_lookup(condition['id'])

                condition_status = is_quest_completed(qid, cid, profile)

                if lup not in conditions_dict:
                    if condition_status:
                        conditions_dict.append({"progress": "DONE", "description":f"<s>{lup}</s>"})
                    if not condition_status:
                        current_progress = get_condition_value_complete(cid, profile)
                        target_progress = get_condition_target_value(qid, cid, profile_quests)

                        if current_progress:
                            progress_string = f"{current_progress}/{target_progress}"
                        elif not current_progress and target_progress:
                            if int(target_progress) > 1:
                                progress_string = f"0/{target_progress}"
                            else:
                                progress_string = ""
                        else:
                            progress_string = ""
                        conditions_dict.append({"progress": progress_string,"description":lup})

        if task_name:
            if last_dict != conditions_dict:
                tasks_dict[task_name] = conditions_dict

            last_dict = conditions_dict
            
    return tasks_dict

def is_quest_completed(qid, cid, profile):
    for q in profile:
        if q['qid'] == qid:
            if cid in q['completedConditions']:
                return True
            else:
                return False

def get_condition_target_value(qid, cid, quests):
    try:
        for quest in quests:
            if quest['_id'] == qid:
                for condition in quest['conditions']['AvailableForFinish']:
                    if condition['id'] == cid:
                        return condition['value']
    except:
        return ''

def get_condition_value_complete(cid, profile):
    try:
        return profile['TaskConditionCounters'][cid]['value']
    except:
        return ''