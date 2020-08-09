import datetime
import math
from fastapi import HTTPException
from sqlalchemy import Table
from sqlalchemy import and_
from sqlalchemy import func
from typing import List
from typing import Optional


class ObjectNotFound(HTTPException):

    def __init__(self, table: Table, item_id: int):
        super().__init__(
            404,
            detail='{}<id:{}> Not found'.format(
                table,
                item_id,
            )
        )


def execute_statement(
    db,
    statement,
    fetchmany: Optional[bool] = False,
    size: Optional[int] = None
):
    with db.connect() as connection:
        result_proxy = connection.execute(statement)
        if fetchmany:
            result = result_proxy.fetchmany(size)
        else:
            result = result_proxy.fetchone()
    return result


def execute_insert_statement(
    db,
    statement,
    values
):
    with db.connect() as connection:
        result_proxy = connection.execute(statement, values)
        result = result_proxy.fetchone()
    return result


def get_count(db, statement):
    count_q = statement.with_only_columns([func.count()]).order_by(None)
    with db.connect() as connection:
        count = connection.execute(count_q).scalar()
    return count


def check_existence(db, table, item_id: int):
    statement = table.select().where(
        and_(
            table.c.id == item_id,
            ~table.c.deleted,
        )
    )
    return get_count(db, statement) != 0


class Crud:
    PAGE_LIMIT = 25
    default_order_field = 'id'
    default_order_direction = 'desc'

    def __init__(self, table):
        self.table = table

    def get_item_by_id(self, db, item_id: int):
        if not check_existence(db, self.table, item_id):
            raise ObjectNotFound(self.table, item_id)
        statement = self.table.select().where(
            and_(
                self.table.c.id == item_id,
                ~self.table.c.deleted,
            )
        )
        item = execute_statement(db, statement)
        return item

    def create(self, db, values: dict):
        statement = self.table.insert().returning(self.table)
        item = execute_insert_statement(db, statement, values)
        return item

    def read(self, db, item_id: int):
        item = self.get_item_by_id(db, item_id)
        return item

    def update(self, db, item_id, values: dict):
        statement = self.table.update().where(
            self.table.c.id == item_id
        ).values(
            dict(
                values,
                updated_dt=datetime.datetime.now()
            )
        ).returning(
            self.table
        )
        item = execute_statement(db, statement)
        return item

    def delete(self, db, item_id: int):
        if not check_existence(db, self.table, item_id):
            raise ObjectNotFound(self.table, item_id)

        statement = self.table.update().where(
            self.table.c.id == item_id
        ).returning(
            self.table
        )
        values = dict(
            deleted=True,
            updated_dt=datetime.datetime.now(),
        )
        execute_insert_statement(db, statement, values)

    def add_filters(self, statement, filters=None):
        _filters = [
            ~self.table.c.deleted,
        ]
        if filters:
            _filters.extend(filters)

        return statement.where(
            and_(*_filters)
        )

    def add_orderings(self, statement, orderings: Optional[List] = None):
        default_order_field = getattr(self.table.c, self.default_order_field)
        default_order_field_with_direction = getattr(
            default_order_field,
            self.default_order_direction,
        )

        if not orderings:
            _orderings = [
                default_order_field_with_direction()
            ]
        elif orderings:
            _orderings = orderings

        return statement.order_by(
            *_orderings
        )

    def _construct_read_page_statement(self, filters, orderings):
        statement = self.table.select()
        statement = self.add_filters(statement, filters)
        statement = self.add_orderings(statement, orderings)
        return statement

    def read_page(
        self,
        db,
        page=1,
        filters=None,
        orderings=None,
        limit=PAGE_LIMIT,
    ):
        if page < 1:
            page = 1

        statement = self._construct_read_page_statement(filters, orderings)
        total = get_count(db, statement)
        last_page = max(1, math.ceil(total/limit))

        if page > last_page:
            raise HTTPException(404, detail='Page not found')

        statement = statement.offset(
            limit * (page-1)
        ).limit(
            limit
        )
        items = execute_statement(
            db,
            statement,
            fetchmany=True,
            size=limit,
        )
        return dict(
            page=page,
            last_page=last_page,
            limit=limit,
            count=len(items),
            total=total,
            items=items,
        )
