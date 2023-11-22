import uuid
from typing import Any, Tuple

from flask import request, jsonify, Response
from pydantic import TypeAdapter
from sqlalchemy.exc import IntegrityError

from backend import app, db
from backend.exceptions.user import UserExistError
from backend.models.user import User
from backend.models.currency import Currency
from backend.schemas.user import CreateUserSchema, GetUserSchema


@app.route("/users/", methods=["GET"])
def get_users(offset: int = 0, limit: int = 10) -> dict[str, Any]:
    count = db.session.query(User).count()
    results = TypeAdapter(list[GetUserSchema]).validate_python(
        db.session.execute(
            db.select(User, Currency)
            .join(Currency, User.currency_id == Currency.id, isouter=True)
            .order_by(User.username)
            .limit(limit)
            .offset(offset)
        ).scalars()
    )
    return {"count": count, "results": [item.model_dump() for item in results]}


@app.route("/user/<_id>/", methods=["GET"])
def get_user(_id: int) -> dict[str, Any]:
    user = db.get_or_404(User, _id)
    return GetUserSchema(
        id=user.id, username=user.username, email=user.email
    ).model_dump()


@app.route("/user/<_id>/", methods=["DELETE"])
def delete_user(_id: int) -> Response | tuple[Response, int]:
    user_to_delete = User.query.get(_id)

    if user_to_delete:
        db.session.delete(user_to_delete)
        db.session.commit()
        return jsonify({"message": f"User {_id} deleted successfully"})
    else:
        return jsonify({"message": f"User {_id} not found"}), 404


@app.route("/user/", methods=["POST"])
def create_user():
    user_data = request.get_json()
    user = CreateUserSchema(**user_data)
    try:
        new_user = User(
            password=user.password,
            username=user.username,
            email=user.email,
            currency_id=user.currency_id,
        )
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        raise UserExistError("User already exists") from e
    return user.model_dump()
