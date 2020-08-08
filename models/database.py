import datetime
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

BaseModel = declarative_base()


class Base(BaseModel):
    __tablename__ = None
    __abstract__ = True

    deleted = Column(Boolean, default=False, nullable=False)
    created_dt = Column(
        DateTime,
        default=datetime.datetime.now,
        nullable=False,
    )
    updated_dt = Column(
        DateTime,
        default=datetime.datetime.now,
        nullable=False,
    )

    def delete(self):
        self.deleted = True
