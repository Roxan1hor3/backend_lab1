from sqlite3 import IntegrityError
from typing import Any

from flask import request
from pydantic import TypeAdapter

from backend import app, db
from backend.exceptions.currency import CurrencyExistError
from backend.models.currency import Currency
from backend.schemas.currency import GetCurrencySchema, CreateCurrencySchema


@app.route("/currencies/", methods=["GET"])
def get_currencies(offset: int = 0, limit: int = 10) -> dict[str, Any]:
    count = db.session.query(Currency).count()
    results = TypeAdapter(list[GetCurrencySchema]).validate_python(
        db.session.execute(
            db.select(Currency).order_by(Currency.name).limit(limit).offset(offset)
        ).scalars()
    )
    return {"count": count, "results": [item.model_dump() for item in results]}


@app.route("/currency/", methods=["POST"])
def create_user():
    currency_data = request.get_json()
    currency = CreateCurrencySchema(**currency_data)
    try:
        new_user = Currency(name=currency.name)
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        raise CurrencyExistError("Currency already exists") from e
    return currency.model_dump()
