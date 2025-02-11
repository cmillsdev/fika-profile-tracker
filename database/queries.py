# queries.py
from sqlalchemy import desc
from database import ProfileSnapshot, Session


def get_all_live_stats():
    """Get latest stats for all profiles"""
    with Session() as session:
        subquery = (
            session.query(
                ProfileSnapshot.profile_id,
                func.max(ProfileSnapshot.timestamp).label("max_time"),
            )
            .group_by(ProfileSnapshot.profile_id)
            .subquery()
        )

        results = (
            session.query(ProfileSnapshot)
            .join(
                subquery,
                (ProfileSnapshot.profile_id == subquery.c.profile_id)
                & (ProfileSnapshot.timestamp == subquery.c.max_time),
            )
            .all()
        )

    return {result.profile_id: result for result in results}


def get_profile_history(profile_id, hours=24):
    """Get historical data for one profile"""
    cutoff = func.datetime("now", f"-{hours} hours")
    with Session() as session:
        return (
            session.query(ProfileSnapshot)
            .filter(ProfileSnapshot.profile_id == profile_id)
            .filter(ProfileSnapshot.timestamp >= cutoff)
            .order_by(ProfileSnapshot.timestamp.asc())
            .all()
        )
