import datetime
from pydantic import BaseModel
from typing import Optional


class ItemCreate(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


class Item(ItemCreate):
    id: int
    created_dt: datetime.datetime
    updated_dt: datetime.datetime

    class Config:
        orm_mode = True


class ItemUpdate(ItemCreate):
    pass


class ItemReadPage(BaseModel):
    id: int
    name: str
    price: float
    is_offer: Optional[bool] = None

    class Config:
        orm_mode = True


class Dispatcher:
    create = ItemCreate
    update = ItemUpdate
    read = Item
    read_page = ItemReadPage
