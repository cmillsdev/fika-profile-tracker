import quests

class Profile():
    def __init__(self, profile_json):
        self.profile_id = profile_json['info']['id']
        self.username = profile_json['info']['username']
        self.pmc_info = profile_json['characters']['pmc']['Info']
        self.pmc_name = self.pmc_info['Nickname']
        self.quests = profile_json['characters']['pmc']['Quests']
        self.skills = profile_json['characters']['pmc']['Skills']
        self.trader_info = profile_json['characters']['pmc']['TradersInfo']
