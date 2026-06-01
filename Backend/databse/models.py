from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import DateTime

from datetime import datetime

from databse.database  import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(
        Integer,
        primary_key = True,
        index = True
    )
    user_id = Column(
        Integer,
        nullable=False
    )

    image_name = Column(
        String,
        nullable =False
    )

    crop = Column(
        String,
        nullable = False
    )
    disease = Column(
        String,
        nullable=False
    )

    confidence = Column(
        Float,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class user(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    username = Column(
        String,
        unique=True
    )
    email = Column(
        String,
        unique=True
    )
    password = Column(
        String
    )