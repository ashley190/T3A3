from models.Admin import Admin
from schemas.AdminSchema import admin_schema
from main import bcrypt
from datetime import timedelta
from flask_jwt_extended import create_access_token  # jwt_required
from flask import Blueprint, request, jsonify, abort

admin = Blueprint("admin", __name__, url_prefix="/admin")


@admin.route("/login", methods=["POST"])
def admin_login():
    admin_fields = admin_schema.load(request.json)

    admin = Admin.query.filter_by(email=admin_fields["username"]).first()

    if not admin or not bcrypt.check_password_hash(
            admin.password, admin_fields["password"]):
        return abort(401, description="Incorrect username and password")

    expiry = timedelta(hours=2)
    access_token = create_access_token(
        identity=str(admin.admin_id), expires_delta=expiry)

    return jsonify({"token": access_token})
