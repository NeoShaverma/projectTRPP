from sqlalchemy import (
    create_engine, Column, Integer, String, DateTime, JSON
)
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from pathlib import Path

from .config import DB_URL

engine = create_engine(DB_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(Integer, index=True)
    message_id = Column(Integer)
    date = Column(DateTime, default=datetime.utcnow)
    text = Column(String)
    keywords = Column(JSON)

def init_db():
    Base.metadata.create_all(bind=engine)
