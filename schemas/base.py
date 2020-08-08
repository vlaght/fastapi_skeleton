from pydantic import BaseModel
from typing import List


def get_page_schema(type_):

    class Page(BaseModel):
        count: int
        limit: int
        total: int
        page: int
        last_page: int
        items: List[type_]

    return Page
