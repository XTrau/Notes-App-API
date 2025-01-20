from fastapi import Query
from pydantic import BaseModel


class SPagination(BaseModel):
    page: int = Query(0, ge=0)
    count: int = Query(10, gt=0)


async def get_pagination(
        page: int = Query(0, ge=0),
        count: int = Query(10, gt=0)
) -> SPagination:
    return SPagination(page=page, count=count)
