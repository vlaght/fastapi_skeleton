from fastapi import FastAPI

from handlers import bind_handlers
from models.database import database
from models.database import engine
from models.database import metadata

metadata.create_all(bind=engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


bind_handlers(app)
