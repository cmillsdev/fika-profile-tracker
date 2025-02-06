from enum import StrEnum

class Endpoint(StrEnum):
    # General stuff
    ALL_PROFILES = "fika/senditem/availablereceivers"
    CLIENT_LOCALE = "client/locale/en"
    # Profile
    ITEMS = "client/items"
    PROFILE = "client/game/profile/list"
    QUESTS = "client/quest/list"
    ACHIEVEMENTS = "client/achievement/list"
    BUILDS = "client/builds/list"
    # Mail
    MAIL_INBOX = "client/mail/dialog/list"
    MAIL_REWARD = "client/mail/dialog/view"
    # Price checks, tarkov.dev for flea
    HANDBOOK = "client/handbook/templates"
    INSURANCE = "client/insurance/items/list/cost"
    # Traders, requires trader_id
    # prapor: 54cb50c76803fa8b248b4571
    # therapist: 54cb57776803fa99248b456e
    # fence: 579dc571d53a0658a154fbec
    # skier: 58330581ace78e27b8b10cee
    # peacekeeper: 5935c25fb3acc3127c3d8cd9
    # mechanic: 5a7c2eca46aef81a7ca2145d
    # ragman: 5ac3b934156ae10c4430e83c
    # jaeger: 5c0647fdd443bc2504c2d371
    # lightkeeper: 638f541a29ffd1183d187f57
    # btr: 656f0f98d80a697f855d34b1
    # ref: 6617beeaa9cfa777ca915b7c
    # scorpion: 6688d464bc40c867f60e7d7e
    # painter: 668aaff35fd574b6dcc4a686
    
    TRADERS = "client/items/prices/"
    TRADER_ASSORT = "client/trading/api/getTraderAssort/"

    TRADER_SETTINGS = "client/trading/api/traderSettings"
    # Hideout
    HIDEOUT_AREAS = "client/hideout/areas"
    HIDEOUT_RECIPES = "client/hideout/production/recipes"

    # Mod stuff
    SERVER_MODS = "launcher/server/loadedServerMods"
    CLIENT_MODS = "launcher/server/serverModsUsedByProfile"

    FIKA_RAIDS = "fika/location/raids"

    VERSION_EFT = 'client/checkVersion'
    VERSION_FIKA = 'fika/client/check/version'
    VERSION_SPT = 'launcher/server/version'

    FIKA_PRESENCE = 'fika/presence/get'
    TIME_WEATHER = 'client/weather'