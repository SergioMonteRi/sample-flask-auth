from uuid import UUID
from sqlalchemy import select
from pydantic import ValidationError
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from database import db
from models.login_request import LoginRequest
from models.create_user_request import CreateUserRequest

app = Flask(__name__)

app.config["SECRET_KEY"] = "my_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

login_manager = LoginManager()

db.init_app(app)
login_manager.init_app(app)

login_manager.login_view = "login"

from models.user import User

@login_manager.user_loader
def load_user(user_id: str):
    stmt = select(User).where(
        User.id == UUID(user_id)
     )

    user = db.session.scalar(stmt)

    print("USER FOUND:", user)
     
    return user

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
    password = login_data.password

    stmt = select(User).where(
        User.username == username
    )

    user = db.session.scalar(stmt)

    if user is None or not check_password_hash(user.password, password):
         return jsonify({
            "error": "Invalid username or password"
        }), 401

    login_user(user)

    return jsonify({
        "message": "Sucessfull login"
    }), 200

@app.route("/logout", methods=["POST"])
@login_required
def logout():
    print(current_user)
    print(current_user.is_authenticated)

    logout_user()

    return jsonify({
        "message": "Sucessfull logout"
    })

@app.route("/create-user", methods=["POST"])
def create_user():
    try:
        data = request.json
        create_user_data = CreateUserRequest.model_validate(data)
    except ValidationError as e:
        return jsonify({
            "error": "Invalid login data",
            "details": e.errors()
        }), 400

    user = User(
        username=create_user_data.username,
        password=generate_password_hash(create_user_data.password)
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
            "message": "User created with sucess"
    }), 201



if __name__ == "__main__":
    app.run(debug=True)