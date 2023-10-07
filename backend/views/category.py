import uuid
from typing import Any

from flask import request

from backend import app

categories = {
    "360a4a67a4c849a3a63b855863423b81": {"name": "category_0"},
    "8e580084e1b64b00a338845d38b23b82": {"name": "category_1"},
    "f7bd727277af4fd8a3eca952114ac9b3": {"name": "category_2"},
    "d909383903af4ebfb7865458411eae24": {"name": "category_3"},
    "e24c49e9d9b644eca8c75e5c8540b455": {"name": "category_4"},
    "1b9d847e7300460b8c59a9453a546a66": {"name": "category_5"},
}


@app.route("/category/", methods=["GET"])
def get_categories() -> dict[str, Any]:
    return categories


@app.route("/category/", methods=["POST"])
def create_category():
    category_data = request.get_json()
    category_uuid = uuid.uuid4().hex
    category = {category_uuid: category_data}
    categories[category_uuid] = category_data
    return category


@app.route("/category/<uuid>/", methods=["DELETE"])
def delete_category(uuid: str) -> dict[str, Any]:
    return categories.pop(uuid)
