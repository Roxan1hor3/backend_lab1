from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import declarative_base, relationship

from backend import db


class Currency(db.Model):
    __tablename__ = "currencies"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    records = relationship("Record", uselist=False)
    users = relationship("User", uselist=False, back_populates="currency")
