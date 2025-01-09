from httprequest import get_profile
import time

def get_health():
    while True:
        health = get_profile()[0]['Health']
        chest = health["BodyParts"]['Chest']['Health']['Current']
        head = health["BodyParts"]['Head']['Health']['Current']
        left_arm = health["BodyParts"]['LeftArm']['Health']['Current']
        left_leg = health["BodyParts"]['LeftLeg']['Health']['Current']
        right_arm = health["BodyParts"]['RightArm']['Health']['Current']
        right_leg = health["BodyParts"]['RightLeg']['Health']['Current']
        stomach = health["BodyParts"]['Stomach']['Health']['Current']
        energy = health['Energy']['Current']
        hydration = health['Hydration']['Current']
        print(f'''energy: {energy} | hydration: {hydration}\nchest: {chest} | head: {head} | stomach: {stomach}\nleft arm: {left_arm} | right arm: {right_arm}\nleft leg: {left_leg} | right leg: {right_leg}\n=======''')

        time.sleep(5)

get_health()