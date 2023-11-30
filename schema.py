import uuid
import datetime
from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    date_created: datetime.datetime

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: uuid.UUID
    address: str | None = None
    phone_number: str | None = None
    is_active: bool | None = None
    items: list[Item] = []

    class Config:
        from_orm = True
