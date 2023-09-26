from datetime import datetime

from fastapi import UploadFile
from sqlalchemy.orm import Session

from utils.schemas import UserCreate
from amazon import upload_file_to_bucket
from core.hashing import Hasher
from db import models
from db.models import datetime_to_unix_time, User


def get_image(db: Session, image_id: int) -> models.Image | None:
    return db.query(models.Image).filter(models.Image.id == image_id).first()


def get_images(db: Session, skip: int = 0, limit: int = 100) -> list[models.Image]:
    return db.query(models.Image).filter(
        models.Image.is_deleted == False
    ).offset(skip).limit(limit).all()


def create_image(db: Session, file: UploadFile, user: User):
    s3_key = upload_file_to_bucket(file)
    upload_date = datetime_to_unix_time(datetime.now())

    db_image = models.Image(
        user_id=user.id,
        upload_date=upload_date,
        image_url=s3_key,
    )
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


def delete_image(db: Session, image_id: int, user: User) -> None:
    image_to_delete = db.query(models.Image).filter(
        models.Image.id == image_id
    ).one_or_none()
    if image_to_delete:
        image_to_delete.is_deleted = True
        image_to_delete.deleted_date = datetime_to_unix_time(datetime.now())
        image_to_delete.delete_user_id = user.id
        db.commit()


def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_new_user(user: UserCreate, db: Session):
    user = User(
        username=user.username,
        password=Hasher.get_password_hash(user.password),
        role="User",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
