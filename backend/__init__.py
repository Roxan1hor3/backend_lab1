import os

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from backend.exceptions.user import UserExistError

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = os.getenv("SQLALCHEMY_DATABASE_URI")
db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

jwt = JWTManager(app)


@app.errorhandler(UserExistError)
def handle_user_exist_error(error):
    response = jsonify({"error": str(error)})
    response.status_code = 409
    return response


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return (
        jsonify({"message": "The token has expired.", "error": "token_expired"}),
        401,
    )


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify(
            {"message": "Signature verification failed.", "error": "invalid_token"}
        ),
        401,
    )


@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "description": "Request does not contain an access token.",
                "error": "authorization_required",
            }
        ),
        401,
    )


from backend.views import users, category, record, helthcheck
from backend.models.user import User
from backend.models.currency import Currency
from backend.models.category import Category
from backend.models.record import Record
