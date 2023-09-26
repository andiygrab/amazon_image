from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    password: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int


class Image(BaseModel):
    id: int
    user_id: int
    upload_date: int
    image_url: str
    upload_url: str | None
    is_deleted: bool
    deleted_date: int | None
    delete_user_id: int | None


class Token(BaseModel):
    access_token: str
    token_type: str