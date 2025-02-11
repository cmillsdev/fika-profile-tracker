from utils.helpers import id_lookup
from core.hideout import get_all_hideout
from core.quests import get_all_objectives
class Skill:
    def __init__(self, skill_data, requires_last_access=True):
        self.name = skill_data["Id"]
        self.progress = skill_data["Progress"]
        self.last_access = skill_data.get("LastAccess", None)  # Some skills don't have LastAccess
        self.is_valid = self.last_access is None or self.last_access > 0  # Valid if LastAccess > 0 or not present

    def __repr__(self):
        return f"Skill(name={self.name}, progress={self.progress}, last_access={self.last_access})"


class Skills:
    """Handles both Common (requires LastAccess) and Mastering (no LastAccess) skills."""
    def __init__(self, common_data, mastering_data):
        self.common = {skill["Id"]: Skill(skill, requires_last_access=True) for skill in common_data if skill["LastAccess"] > 0}
        self.mastering = {skill["Id"]: Skill(skill, requires_last_access=False) for skill in mastering_data}

    def __repr__(self):
        return f"Skills(common={list(self.common.values())}, mastering={list(self.mastering.values())})"

class HealthStat:
    def __init__(self, data):
        self.current = data["Current"]
        self.maximum = data["Maximum"]

    def __repr__(self):
        return f"HealthStat(current={self.current}, maximum={self.maximum})"

class BodyParts:
    def __init__(self, data):
        for part, values in data.items():
            setattr(self, part.lower(), HealthStat(values["Health"]))

    def __repr__(self):
        return f"BodyParts({', '.join(f'{k}={v}' for k, v in self.__dict__.items())})"

class Trader:
    def __init__(self, trader_id, details):
        self.name = id_lookup(f"{trader_id} Nickname")  # Lookup trader name
        self.sales = details["salesSum"]
        self.standing = details["standing"]

    def __repr__(self):
        return f"Trader(name={self.name}, sales={self.sales}, standing={self.standing})"


class Traders:
    def __init__(self, data):
        """Initialize a collection of traders."""
        self.traders = {trader_id: Trader(trader_id, details) for trader_id, details in data.items()}

    def __getitem__(self, trader_id):
        """Allow indexing, e.g., traders['54cb50c76803fa8b248b4571']"""
        return self.traders.get(trader_id)

    def __repr__(self):
        return f"Traders({list(self.traders.values())})"

class Counters:
    def __init__(self, session, overall):
        self.session = self.process_counters(session)
        self.overall = self.process_counters(overall)

    def __repr__(self):
        return f"Counters({', '.join(f'{k}={v}' for k, v in self.__dict__.items())})"

    def process_counters(self, items):
        """Converts session counters into a dictionary with tuple keys where necessary."""
        counters = {}
        for item in items:
            key = tuple(item["Key"]) if len(item["Key"]) > 1 else item["Key"][0]  # Tuple if multi-level key
            counters[key] = item["Value"]
        return counters

class Profile:
    def __init__(self, data):
        self.player_id = data['_id']
        self.nickname = data['Info']['Nickname']
        self.level = data['Info']['Level']
        self.experience = data['Info']['Experience']
        self.reg_date = data['Info']['RegistrationDate']
        self.faction = data['Info']['Side']
        self.scav_karma = data['karmaValue']
        self.ragfair = data['RagfairInfo']
        self.cheevos = self.get_cheevos(data)
        self.lifetime_insured = len(data['InsuredItems'])
        self.examined_count = self.examined_items(data['Encyclopedia'])
        self.health = BodyParts(data["Health"]["BodyParts"])
        self.energy = HealthStat(data["Health"]["Energy"])
        self.hydration = HealthStat(data["Health"]["Hydration"])
        self.skills = Skills(data["Skills"]["Common"], data["Skills"]["Mastering"])
        self.traders = Traders(data['TradersInfo'])
        self.nonbasic_extract_counts = {"car": data["CarExtractCounts"], "coop": data["CoopExtractCounts"]}
        self.counters = Counters(data["Stats"]["Eft"]["SessionCounters"]["Items"], data["Stats"]["Eft"]["OverallCounters"]["Items"])
        self.hideout = get_all_hideout(self.player_id, data['Hideout'])
        self.quests = get_all_objectives(self.player_id, data['Quests'])
        self.bonuses = self.get_profile_bonuses(data["Bonuses"])
        self.repeatable_quests = data["RepeatableQuests"]
        self.inventory = data["Inventory"]
        self.task_counters = data["TaskConditionCounters"]

    def get_profile_bonuses(self, bonuses):
        bonii = []
        for bonus in bonuses:
            bonii.append({'type': bonus['type'], 'value': bonus.get('value', 0)})

        return bonii

    def examined_items(self, encyc):
        return sum(1 for e in encyc if encyc[e])

    def get_cheevos(self, profile):
        cheevos = []
        for cheevo in profile["Achievements"].keys():
            name = id_lookup(f'{cheevo} name')
            desc = id_lookup(f'{cheevo} description')
            cheevos.append({name: desc})
        return cheevos

    