from sqlmodel import SQLModel, Field
from pydantic import BaseModel


class DHT(SQLModel, table = True):
    """Модель данных. Динамическая хеш-таблица.
    Состоит из столбцов: id (int) | meta_file (str) | peers (str)"""
    id: int | None = Field(default=None, primary_key=True)
    meta_file: str | None = Field(default=None, index=True)
    peers : str | None = Field(default=None)

class DistributionModel(BaseModel):
    """Подсобная модель данных для записи новых раздач в таблицу."""
    meta_file: str = Field(index=True)
    peers: str = Field()

class DistributionUpdate(BaseModel):
    """Подсобная модель для обновления записи раздачи в таблице."""
    peers: str = Field()