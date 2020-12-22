from models.Admin import Admin
from models.User import User
from models.Profile import Profile
from schemas.AdminSchema import admin_schema, admin_users_schema
from main import bcrypt
from datetime import timedelta
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity      # noqa: E501
from flask import Blueprint, request, jsonify, abort
from sqlalchemy import func

admin = Blueprint("admin", __name__, url_prefix="/admin")


@admin.route("/login", methods=["POST"])
def admin_login():
    admin_fields = admin_schema.load(request.json)

    admin = Admin.query.filter_by(username=admin_fields["username"]).first()

    if not admin or not bcrypt.check_password_hash(
            admin.password, admin_fields["password"]):
        return abort(401, description="Incorrect username and password")

    expiry = timedelta(hours=2)
    access_token = create_access_token(
        identity=str(admin.admin_id), expires_delta=expiry)

    return jsonify({"token": access_token})


@admin.route("/users", methods=["GET"])
@jwt_required
def get_users():
    admin_id = get_jwt_identity()

    admin = Admin.query.get(admin_id)

    if not admin:
        return abort(401, description="Invalid admin user")

    query = User.query.with_entities(
        User.email, func.count(Profile.profile_id).label(
            'profile_count')).outerjoin(Profile).group_by(
                User.email).order_by(User.email)
    # SELECT users.email AS users_email, count(profiles.profile_id)
    # AS profile_count
    # FROM users LEFT OUTER JOIN profiles ON users.user_id = profiles.user_id
    # GROUP BY users.email ORDER BY users.email
    return jsonify(admin_users_schema.dump(query))
