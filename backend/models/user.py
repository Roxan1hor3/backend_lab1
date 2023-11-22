from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, relationship

from backend import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    currency_id = db.Column(db.Integer, db.ForeignKey("currencies.id"))
    currency = db.relationship("Currency", back_populates="users")

    records = relationship("Record", uselist=False)
