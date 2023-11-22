from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from backend.exceptions.user import UserExistError

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql+psycopg2://habrpguser:pgpwd4habr@172.22.0.2:5432/habrdb"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.errorhandler(UserExistError)
def handle_user_exist_error(error):
    response = jsonify({"error": str(error)})
    response.status_code = 409
    return response


from backend.views import users, category, record, helthcheck
from backend.models.user import User
from backend.models.currency import Currency
from backend.models.category import Category
from backend.models.record import Record
