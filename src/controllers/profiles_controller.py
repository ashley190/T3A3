# from database import cursor, connection
from flask import Blueprint     # request, jsonify
profiles = Blueprint('profiles', __name__, url_prefix="/profiles")


@profiles.route("/", methods=["GET"])
def show_profiles():
    return "show all profiles"


@profiles.route("/create", methods=["POST"])
def create_profile():
    return "create profile"


@profiles.route("/<int:id>", methods=["PATCH"])
def update_profile(id):
    return f"update profile {id}"


@profiles.route("/<int:id>", methods=["DELETE"])
def delete_profile(id):
    return f"delete profile {id}"
