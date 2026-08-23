from sqlalchemy import select
from pydantic import ValidationError
from flask_login import LoginManager
from flask import Flask, request, jsonify

from database import db
from models.login_request import LoginRequest

app = Flask(__name__)

app.config["SECRET_KEY"] = "my_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

login_manager = LoginManager()

db.init_app(app)
login_manager.init_app(app)

from models.user import User

@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.json

        login_data = LoginRequest.model_validate(data)
    except ValidationError as e:
        return jsonify({
            "error": "Invalid login data",
            "details": e.errors()
        }), 400

    username = login_data.username

    stmt = select(User).where(
        User.username == username
    )

    user = db.session.scalar(stmt)

    if user is None:
         return jsonify({
            "error": "Invalid username or password"
        }), 401

    print(user)


@app.route("/hello-world", methods=["GET"])
def hello_world():
    return "Hello World"


if __name__ == "__main__":
    app.run(debug=True)