from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

from backend import db


class Record(db.Model):
    __tablename__ = "record"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    description = db.Column(db.String(255))
    date = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    _user = db.relationship("User", back_populates="records")

    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    _category = db.relationship("Category", back_populates="records")

    currency_id = db.Column(db.Integer, db.ForeignKey("currencies.id"))
    _currency = db.relationship("Currency")
