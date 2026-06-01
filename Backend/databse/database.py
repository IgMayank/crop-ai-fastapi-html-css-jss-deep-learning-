from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = "sqlite:///./crop_monitor.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread":False}
)

SessionLocker = sessionmaker(
    autocommit = False,
    autoflush=False,
    bind = engine
)
Base = declarative_base()