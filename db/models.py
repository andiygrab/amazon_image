from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType, URLType

from db.engine import Base


class User(Base):
    ROLE = [
        ("admin", "Admin"),
        ("user", "User")
    ]

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        unique=True,
        nullable=False,
        autoincrement=True
    )
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, ChoiceType(ROLE))

    image = relationship("Image", back_populates="user", foreign_keys="Image.user_id")


class Image(Base):
    __tablename__ = "images"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        unique=True,
        nullable=False,
        autoincrement=True
    )
    user_id = Column(Integer, ForeignKey("users.id"))
    upload_date = Column(BigInteger)
    image_url = Column(URLType)
    upload_url = Column(URLType, default=None)
    is_deleted = Column(Boolean, default=False)
    deleted_date = Column(BigInteger, default=None)
    delete_user_id = Column(Integer, ForeignKey("users.id"), default=None)

    user = relationship(User, back_populates="image", foreign_keys="Image.user_id")


def datetime_to_unix_time(dt: datetime | str) -> int:
    """
    Converts a datetime object or a string in ISO 8601 format to Unix time (Unix timestamp).

    Args:
        dt (Union[datetime, str]): The datetime object or string to convert.

    Returns:
        int: The Unix timestamp representing the input datetime.

    Raises:
        ValueError: If the input string is not in a valid ISO 8601 format.
    """
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt)

    unix_timestamp = int(dt.timestamp())

    return unix_timestamp
