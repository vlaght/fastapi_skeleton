import datetime
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table

from .database import metadata

Item = Table(
    'Item',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('price', Float, nullable=False),
    Column('is_offer', Boolean, nullable=False, default=False),
    Column(
        'created_dt',
        DateTime,
        nullable=False,
        default=datetime.datetime.now
    ),
    Column(
        'updated_dt',
        DateTime,
        nullable=False,
        default=datetime.datetime.now
    ),
    Column('deleted', Boolean, nullable=False, default=False),
)
