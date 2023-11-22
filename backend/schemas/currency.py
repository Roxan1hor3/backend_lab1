from backend.schemas.base import BaseOrmModel


class GetCurrencySchema(BaseOrmModel):
    name: str
    id: int


class CreateCurrencySchema(BaseOrmModel):
    name: str
    id: int
