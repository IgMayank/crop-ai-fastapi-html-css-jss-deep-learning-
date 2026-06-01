from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

# DATABASE_URL = "sqlite:///./crop_monitor.db"

# engine = create_engine(
#     DATABASE_URL,
#     connect_args={"check_same_thread":False}
# )

import os

DATABASE_URL = os.getenv("DATABASE_URL",
    "sqlite:///./crop_monitor.db")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://",
        "poatgresql://",
        1
    )
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread" : False}
    )
else:
    engine = create_engine(DATABASE_URL)

SessionLocker = sessionmaker(
    autocommit = False,
    autoflush=False,
    bind = engine
)
Base = declarative_base()