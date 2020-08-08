from fastapi import FastAPI

from handlers import bind_handlers
from models.database import Base
from models.database import engine

Base.metadata.create_all(bind=engine)
app = FastAPI()
bind_handlers(app)
