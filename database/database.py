# database.py
from sqlalchemy import Column, Integer, String, Float, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class ProfileSnapshot(Base):
    __tablename__ = "profiles"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    profile_id = Column(String, index=True)  # Original profile ID from Tarkov
    nickname = Column(String)
    level = Column(Integer)
    health = Column(Float)
    hydration = Column(Float)
    energy = Column(Float)
    roubles = Column(Integer)
    timestamp = Column(DateTime, default=func.utcnow())

    # Composite index for faster profile+time queries
    __table_args__ = (
        Index('idx_profile_time', 'profile_id', 'timestamp'),
    )