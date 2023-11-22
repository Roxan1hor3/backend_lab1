from pydantic import BaseModel


class BaseOrmModel(BaseModel):
    class Config:
        from_attributes = True
