from models.User import User
from schemas.UserSchema import user_schema
from main import db, bcrypt
from flask_jwt_extended import create_access_token
from datetime import timedelta
from flask import Blueprint, request, jsonify, abort


users = Blueprint("users", __name__, url_prefix="/users")


@users.route("/register", methods=["POST"])
def users_register():
    user_fields = user_schema.load(request.json)

    user = User.query.filter_by(email=user_fields["email"]).first()

    if user:
        return abort(400, description="Email already registered")

    user = User()
    user.email = user_fields["email"]
    user.password = bcrypt.generate_password_hash(
        user_fields["password"]).decode("utf-8")
    user.subscription_status = user_fields["subscription_status"]

    db.session.add(user)
    db.session.commit()

    return jsonify(user_schema.dump(user))


@users.route("/login", methods=["POST"])
def users_login():
    user_fields = user_schema.load(request.json)

    user = User.query.filter_by(email=user_fields["email"]).first()

    if not user or not bcrypt.check_password_hash(
            user.password, user_fields["password"]):
        return abort(401, description="Incorrect username and password")

    expiry = timedelta(days=1)
    access_token = create_access_token(
        identity=str(user.user_id), expires_delta=expiry)

    return jsonify({"token": access_token})
