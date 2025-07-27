from sqlmodel import SQLModel, Session, create_engine
from fastapi import Depends, FastAPI
from typing import Annotated
from contextlib import asynccontextmanager

sqlite_file_name = 'dht.db'
sqlite_url = f'sqlite:///{sqlite_file_name}'
connect_args = {'check_same_thread': False} # разрешаем работу с базой данных из разных потоков
engine = create_engine(sqlite_url, connect_args=connect_args)

async def create_db_and_tables():
    """Создаёт все таблицы базы dht.db, которых ещё нет в dht.db"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Возвращает объект взаимодействия с базой данных.
    Который используется через Depends для создания и 
    закрытия подключений при каждом запросе."""
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield