import uuid
from typing import Any

from flask import request, jsonify
from flask_jwt_extended import jwt_required
from pydantic import TypeAdapter
from sqlalchemy.exc import IntegrityError
from backend.models.category import Category

from backend import app, db
from backend.exceptions.category import CategoryExistError
from backend.schemas.category import GetCategorySchema, CreateCategorySchema


@app.route("/category/", methods=["GET"])
@jwt_required()
def get_categories(offset: int = 0, limit: int = 10) -> dict[str, Any]:
    count = db.session.query(Category).count()
    results = TypeAdapter(list[GetCategorySchema]).validate_python(
        db.session.execute(
            db.select(Category).order_by(Category.name).limit(limit).offset(offset)
        ).scalars()
    )
    return {"count": count, "results": [item.model_dump() for item in results]}


@app.route("/category/", methods=["POST"])
@jwt_required()
def create_category():
    category_data = request.get_json()
    category = CreateCategorySchema(**category_data)
    try:
        new_category = Category(name=category.name, description=category.description)
        db.session.add(new_category)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        raise CategoryExistError("Category already exists") from e
    return category.model_dump()


@app.route("/category/<_id>/", methods=["DELETE"])
@jwt_required()
def delete_category(_id: int) -> dict[str, Any]:
    category_to_delete = Category.query.get(_id)

    if category_to_delete:
        db.session.delete(category_to_delete)
        db.session.commit()
        return jsonify({"message": f"Category {_id} deleted successfully"})
    else:
        return jsonify({"message": f"Category {_id} not found"}), 404
