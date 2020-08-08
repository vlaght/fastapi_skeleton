from fastapi import Depends
from fastapi import HTTPException
from fastapi import Query
from sqlalchemy.orm import Session
from typing import Optional

from core.base import Crud
from models.database import SessionLocal
from schemas.base import get_page_schema


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def bind_crud_handlers(app, name, schema_dispatcher, crud: Crud):
    stream_url = '/{}'.format(name)
    item_url = stream_url + '/{item_id}'
    MAX_PAGE_LIMIT = 100
    ObjId = Query(None, ge=1)

    @app.get(
        stream_url,
        response_model=get_page_schema(schema_dispatcher.read_page),
        tags=[name],
        operation_id='{}_read_page',
    )
    async def read_page(
        db: Session = Depends(get_db),
        page: Optional[int] = Query(1, ge=1),
        limit: Optional[int] = Query(crud.PAGE_LIMIT, ge=1, le=MAX_PAGE_LIMIT),
    ):
        items_page = crud.read_page(db, page=page, limit=limit)
        return items_page

    @app.get(
        item_url,
        response_model=schema_dispatcher.read,
        tags=[name],
        operation_id='{}_read',
    )
    async def read(item_id: int = ObjId, db: Session = Depends(get_db)):
        item = crud.read(db, item_id)
        db.commit()
        return item

    @app.post(
        stream_url,
        response_model=schema_dispatcher.read,
        tags=[name],
        operation_id='{}_create',
    )
    async def create(
        values: schema_dispatcher.create,
        db: Session = Depends(get_db)
    ):
        item = crud.create(db, values.dict())
        db.commit()
        return item

    @app.put(
        item_url,
        response_model=schema_dispatcher.read,
        tags=[name],
        operation_id='{}_update',
    )
    async def update(
        item_id: int = ObjId,
        values: schema_dispatcher.update = None,
        db: Session = Depends(get_db)
    ):
        if values is None:
            raise HTTPException(422, detail='Provide some data')
        item = crud.get_item_by_id(db, item_id)
        updated_item = crud.update(db, item, values.dict())
        return updated_item

    @app.delete(item_url, tags=[name], operation_id='{}_delete',)
    async def delete(item_id: int = ObjId, db: Session = Depends(get_db)):
        item = crud.get_item_by_id(db, item_id)
        crud.delete(db, item)
        db.commit()
        return {}