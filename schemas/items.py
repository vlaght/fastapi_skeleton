import datetime
from pydantic import BaseModel
from pydantic import Field
from typing import Optional


class ItemCreate(BaseModel):
    name: str
    price: float
    is_offer: bool = Field(False)


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
    is_offer: Optional[bool] = False


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
