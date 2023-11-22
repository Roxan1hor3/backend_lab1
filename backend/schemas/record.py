from datetime import datetime

from backend.schemas.base import BaseOrmModel


class CreateRecordSchema(BaseOrmModel):
    amount: int
    description: str
    date: datetime | None = datetime.utcnow()
    user_id: int
    category_id: int
    currency_id: int


class GetRecordSchema(BaseOrmModel):
    id: int
    amount: int
    description: str
    date: datetime
    user_id: int
    category_id: int
    currency_id: int

    class Config:
        orm_mode = True
