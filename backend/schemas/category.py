from backend.schemas.base import BaseOrmModel


class CreateCategorySchema(BaseOrmModel):
    name: str
    description: str


class GetCategorySchema(BaseOrmModel):
    id: int
    name: str
    description: str
