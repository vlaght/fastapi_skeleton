from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import false
from sqlalchemy import func

from .database import metadata

Item = Table(
    'Item',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('price', Float, nullable=False),
    Column('is_offer', Boolean, nullable=False, default=false()),
    Column(
        'created_dt',
        DateTime,
        nullable=False,
        default=func.now(),
    ),
    Column(
        'updated_dt',
        DateTime,
        nullable=False,
        default=func.now(),
    ),
    Column('deleted', Boolean, nullable=False, default=false()),
)
