from flask_jwt_extended import get_jwt_identity
from models.User import User
from flask import abort


def get_user_by_id(first=False):
    user_id = get_jwt_identity()

    if first:
        user = User.query.filter_by(user_id=user_id).first()
    elif not first:
        user = User.query.filter_by(user_id=user_id)

    if not user:
        return abort(401, description="Invalid user")

    return user
