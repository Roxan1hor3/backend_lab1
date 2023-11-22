from pydantic import Field

from backend.schemas.base import BaseOrmModel
from backend.schemas.currency import GetCurrencySchema


class CreateUserSchema(BaseOrmModel):
    username: str
    email: str
    password: str
    currency_id: int


class GetUserSchema(BaseOrmModel):
    id: int
    username: str
    email: str
    currency: GetCurrencySchema | None = None
