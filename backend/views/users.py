import uuid
from typing import Any

from flask import request

from backend import app

users = {
    "360a4a67a4c849a3a63b855863423b87": {"name": "user_0"},
    "8e580084e1b64b00a338845d38b23b83": {"name": "user_1"},
    "f7bd727277af4fd8a3eca952114ac9b7": {"name": "user_2"},
    "d909383903af4ebfb7865458411eae21": {"name": "user_3"},
    "e24c49e9d9b644eca8c75e5c8540b453": {"name": "user_4"},
    "1b9d847e7300460b8c59a9453a546a6a": {"name": "user_5"},
}


@app.route("/users/", methods=["GET"])
def get_users() -> dict[str, Any]:
    return users


@app.route("/user/<uuid>/", methods=["GET"])
def get_user(uuid: str) -> dict[str, Any]:
    return users[uuid]


@app.route("/user/<uuid>/", methods=["DELETE"])
def delete_user(uuid: str) -> dict[str, Any]:
    return users.pop(uuid)


@app.route("/user/", methods=["POST"])
def create_user():
    user_data = request.get_json()
    user_uuid = uuid.uuid4().hex
    user = {user_uuid: user_data}
    users[user_uuid] = user_data
    return user
