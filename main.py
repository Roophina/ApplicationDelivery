"""Асинхронное веб-приложение, написанное в соответствии с условиями задачи."""
from enum import Enum
from typing import List

import databases
import sqlalchemy
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, constr

from sqlalchemy import String
from sqlalchemy_utils import ChoiceType


DATABASE_URL = "postgresql://postgres:12345@127.0.0.1/Delivery"
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

deliveries = sqlalchemy.Table(
    "deliveries",
    metadata,
    sqlalchemy.Column("id", String(5), primary_key=True),
    sqlalchemy.Column("status", ChoiceType([("to_do", "to_do"), ("in_progress", "n_progress"), ("done", "done")],
                                           impl=String()))
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, pool_size=3, max_overflow=0
)
metadata.create_all(engine)


class StatusEnum(str, Enum):
    """Класс, который используется для определения типа данных в pydantic модели."""

    to_do = 'to_do'
    in_progress = 'in_progress'
    done = 'done'


class Delivery(BaseModel):
    """pydantic модель."""

    id: constr(max_length=5, min_length=2, regex=r"[a-z0-9]+")  # type: ignore  # noqa: F722
    status: StatusEnum


app = FastAPI()


@app.on_event("startup")  # type: ignore
async def startup() -> None:
    """Создание пула соединений на старт приложения."""
    await database.connect()


@app.on_event("shutdown")  # type: ignore
async def shutdown() -> None:
    """Разрыв пула соединения при завершении приложения."""
    await database.disconnect()


@app.get("/deliveries/", response_model=List[Delivery])  # type: ignore
async def read_deliveries() -> list:
    """Выдать список всех текущих доставок."""
    query = deliveries.select()
    return await database.fetch_all(query)


@app.post("/deliveries/", response_model=Delivery)  # type: ignore
async def create_delivery(delivery: Delivery) -> dict:
    """Записать/обновить запись в таблице в бд."""
    query = deliveries.select().where(deliveries.columns.id == delivery.id)
    query_id = await database.fetch_one(query)
    if query_id:
        query = deliveries.update().where(deliveries.columns.id == delivery.id).values(status=delivery.status)
    else:
        query = deliveries.insert().values(id=delivery.id, status=delivery.status)
    await database.execute(query)
    return delivery.dict()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
