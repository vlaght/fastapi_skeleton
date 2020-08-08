import datetime
import math
from fastapi import HTTPException
from sqlalchemy.orm import Session


class Crud:
    PAGE_LIMIT = 25
    default_order_field = 'id'
    default_order_direction = 'desc'

    def __init__(self, model):
        self.model = model

    def get_item_by_id(self, db: Session, item_id: int):
        item = db.query(self.model).get(item_id)
        if item.deleted:
            raise HTTPException(
                404,
                detail='{}<id:{}> Not found'.format(
                    self.model.__tablename__,
                    item_id,
                )
            )
        return item

    def create(self, db: Session, values: dict):
        obj = self.model(**values)
        db.add(obj)
        return obj

    def read(self, db: Session, item_id: int):
        obj = self.get_item_by_id(db, item_id)
        return obj

    def update(self, db: Session, obj, values: dict):
        for prop, value in values.items():
            setattr(obj, prop, value)
        obj.updated_dt = datetime.datetime.now()
        return obj

    def delete(self, db: Session, obj):
        obj.updated_dt = datetime.datetime.now()
        obj.delete()
        db.flush()

    def read_page(
        self,
        db: Session,
        page=1,
        filters=None,
        orderings=None,
        limit=PAGE_LIMIT,
    ):
        if page < 1:
            page = 1
        query = db.query(self.model)
        if orderings:
            query = query.order_by(*orderings)
        default_order_field = getattr(self.model, self.default_order_field)
        default_order_filter = getattr(
            default_order_field,
            self.default_order_direction,
        )
        query = query.order_by(
            default_order_filter()
        )
        if filters:
            query = query.filter(
                *filters
            )

        query = query.filter(
            self.model.deleted == False  # noqa: E712
        )
        total = query.count()
        last_page = math.ceil(total/limit)
        if page > last_page:
            raise HTTPException(404, detail='Page not found')
        query = query.offset(
            limit * (page-1)
        ).limit(
            limit
        )
        items = query.all()
        return dict(
            page=page,
            last_page=last_page,
            limit=limit,
            count=len(items),
            total=total,
            items=items,
        )
