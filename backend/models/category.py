from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from backend import db


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(255))
    records = relationship("Record", uselist=False)
