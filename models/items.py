from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String

from .database import Base


class Item(Base):
    __tablename__ = 'Item'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    price = Column(Float)
    is_offer = Column(Boolean)
