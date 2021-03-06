import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class ItemCreate(BaseModel):
    name: str = Field(None, description='Name of item')
    price: float = Field(None, description='Item`s price')
    is_offer: bool = Field(False, description='Offer flag')


class Item(BaseModel):
    id: int
    name: str
    price: float
    is_offer: bool
    created_dt: datetime.datetime
    updated_dt: datetime.datetime


class ItemUpdate(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool]


class ItemReadPage(BaseModel):
    id: int
    name: str
    price: float
    is_offer: bool


class Dispatcher:
    create = ItemCreate
    update = ItemUpdate
    read = Item
    read_page = ItemReadPage
