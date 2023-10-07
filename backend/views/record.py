import datetime
import uuid
from typing import Any, Dict, List

from flask import request

from backend import app

records = {
    "360a4a67a4c849a3a63b855863423b86": {
        "name": "record_0",
        "user_uuid": "360a4a67a4c849a3a63b855863423b87",
        "category_uuid": "360a4a67a4c849a3a63b855863423b81",
        "created_at": str(datetime.datetime.now()),
        "amount": 50,
    },
    "8e580084e1b64b00a338845d38b23b85": {
        "name": "record_1",
        "user_uuid": "8e580084e1b64b00a338845d38b23b83",
        "category_uuid": "8e580084e1b64b00a338845d38b23b82",
        "created_at": str(datetime.datetime.now()),
        "amount": 50,
    },
    "f7bd727277af4fd8a3eca952114ac9b4": {
        "name": "record_2",
        "user_uuid": "f7bd727277af4fd8a3eca952114ac9b7",
        "category_uuid": "f7bd727277af4fd8a3eca952114ac9b3",
        "created_at": str(datetime.datetime.now()),
        "amount": 50,
    },
    "d909383903af4ebfb7865458411eae23": {
        "name": "record_3",
        "user_uuid": "d909383903af4ebfb7865458411eae21",
        "category_uuid": "d909383903af4ebfb7865458411eae24",
        "created_at": str(datetime.datetime.now()),
        "amount": 50,
    },
    "e24c49e9d9b644eca8c75e5c8540b452": {
        "name": "record_4",
        "user_uuid": "e24c49e9d9b644eca8c75e5c8540b453",
        "category_uuid": "e24c49e9d9b644eca8c75e5c8540b455",
        "created_at": str(datetime.datetime.now()),
        "amount": 50,
    },
    "1b9d847e7300460b8c59a9453a546a61": {
        "name": "record_5",
        "user_uuid": "1b9d847e7300460b8c59a9453a546a6a",
        "category_uuid": "1b9d847e7300460b8c59a9453a546a66",
        "created_at": str(datetime.datetime.now()),
        "amount": 50,
    },
}


@app.route("/record/<uuid>/", methods=["GET"])
def get_records(uuid) -> dict[str, Any]:
    return records[uuid]


@app.route("/record/<uuid>/", methods=["DELETE"])
def delete_record(uuid: str) -> dict[str, Any]:
    return records.pop(uuid)


@app.route("/record/", methods=["POST"])
def create_record():
    record_data = request.get_json()
    record_uuid = uuid.uuid4().hex
    record = {record_uuid: record_data, "created_at": str(datetime.datetime.now())}
    records[record_uuid] = record_data
    return record


@app.route("/record_filter/<category_uuid>/<user_uuid>/", methods=["GET"])
def get_records_by_filter(category_uuid=None, user_uuid=None) -> dict[str, str] | list[str]:
    if category_uuid is None and user_uuid is None:
        return {
            "error": "One of the query parameters category_uuid or user_uuid is required"
        }
    response_records = []
    for record in records.values():
        if (
            category_uuid is not None
            and user_uuid is None
            and record["category_uuid"] == category_uuid
        ):
            response_records.append(record)
        elif (
            category_uuid is None
            and user_uuid is not None
            and record["user_uuid"] == user_uuid
        ):
            response_records.append(record)
        elif (
            category_uuid is not None
            and user_uuid is not None
            and record["user_uuid"] == user_uuid
            and record["category_uuid"] == category_uuid
        ):
            response_records.append(record)
    return response_records
