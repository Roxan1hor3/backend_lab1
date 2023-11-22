from typing import Any

from flask import request, jsonify, Response
from pydantic import TypeAdapter
from sqlalchemy.exc import IntegrityError

from backend.exceptions.record import RecordExistError
from backend.models.record import Record
from backend import app, db
from backend.schemas.record import GetRecordSchema, CreateRecordSchema


@app.route("/record/<_id>/", methods=["GET"])
def get_records(_id) -> dict[str, Any]:
    record = db.get_or_404(Record, _id)
    return GetRecordSchema(
        id=record.id,
        amount=record.amount,
        description=record.description,
        date=record.date,
        user_id=record.user_id,
        category_id=record.category_id,
        currency_id=record.currency_id,
    ).model_dump()


@app.route("/record/<_id>/", methods=["DELETE"])
def delete_record(_id: int) -> Response | tuple[Response, int]:
    record_to_delete = Record.query.get(_id)

    if record_to_delete:
        db.session.delete(record_to_delete)
        db.session.commit()
        return jsonify({"message": f"Record {_id} deleted successfully"})
    else:
        return jsonify({"message": f"Record {_id} not found"}), 404


@app.route("/record/", methods=["POST"])
def create_record():
    record_data = request.get_json()
    record = CreateRecordSchema(**record_data)
    try:
        new_user = Record(
            amount=record.amount,
            description=record.description,
            date=record.date,
            user_id=record.user_id,
            category_id=record.category_id,
            currency_id=record.currency_id,
        )
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        raise RecordExistError("Record already exists") from e
    return record.model_dump()


@app.route("/record_filter/<category_id>/<user_id>/", methods=["GET"])
def get_records_by_filter(
    category_id=None, user_id=None, offset: int = 0, limit: int = 10
) -> dict[str, str] | list[str]:
    if category_id is None and user_id is None:
        return {
            "error": "One of the query parameters category_id or user_id is required"
        }
    count = db.session.query(Record).count()
    query = (
        db.select(Record)
        .filter(Record.category_id == category_id)
        .order_by(Record.date)
        .limit(limit)
        .offset(offset)
    )
    if category_id:
        query.filter(Record.category_id == category_id)
    if user_id:
        query.filter(Record.user_id == user_id)
    results = TypeAdapter(list[GetRecordSchema]).validate_python(
        db.session.execute(query).scalars()
    )
    return {"count": count, "results": [item.model_dump() for item in results]}
