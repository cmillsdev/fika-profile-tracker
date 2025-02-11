# collector.py
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, ProfileSnapshot
from config import PROFILES, POLL_INTERVAL, DB_PATH
from utils.helpers import get_profile
import logging

logging.basicConfig(level=logging.INFO)
engine = create_engine(DB_PATH)
Session = sessionmaker(bind=engine)

def collect_all_profiles():
    """Collect data for all configured profiles"""
    snapshots = []
    
    for pid in PROFILES:
        try:
            profile_data = get_profile(pid)['data'][0]  # PMC profile
            snapshots.append(
                ProfileSnapshot(
                    profile_id=pid,
                    nickname=profile_data['Info']['Nickname'],
                    level=profile_data['Info']['Level'],
                    health=profile_data['Health']['Hydration']['Current'],
                    hydration=profile_data['Health']['Energy']['Current'],
                    energy=profile_data['Health']['BodyParts']['Head']['Health']['Current'],
                    roubles=profile_data['Info']['Roubles']
                )
            )
            logging.info(f"Collected data for {pid}")
        except Exception as e:
            logging.error(f"Failed to collect {pid}: {str(e)}")
            continue

    if snapshots:
        with Session() as session:
            session.bulk_save_objects(snapshots)
            session.commit()
            logging.info(f"Saved {len(snapshots)} profiles to DB")

def run_collector():
    """Main collection loop"""
    Base.metadata.create_all(engine)
    while True:
        start_time = time.time()
        collect_all_profiles()
        elapsed = time.time() - start_time
        sleep_time = max(POLL_INTERVAL - elapsed, 1)
        time.sleep(sleep_time)

if __name__ == "__main__":
    run_collector()