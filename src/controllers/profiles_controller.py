from models.Profile import Profile
# from models.User import User
from main import db
from schemas.ProfileSchema import profile_schema, profiles_schema
from flask_jwt_extended import jwt_required
from flask import Blueprint, request, jsonify
profiles = Blueprint('profiles', __name__, url_prefix="/profiles")


@profiles.route("/", methods=["GET"])
@jwt_required
def show_profiles():
    profiles = Profile.query.all()
    return jsonify(profiles_schema.dump(profiles))


@profiles.route("/create", methods=["POST"])
@jwt_required
def create_profile():
    profile_fields = profile_schema.load(request.json)
    new_profile = Profile()
    new_profile.name = profile_fields["name"]
    new_profile.restrictions = profile_fields["restrictions"]

    db.session.add(new_profile)
    db.session.commit()

    return jsonify(profile_schema.dump(new_profile))


@profiles.route("/<int:id>", methods=["PATCH"])
@jwt_required
def update_profile(id):
    profile = Profile.query.filter_by(profile_id=id)
    profile_fields = profile_schema.load(request.json, partial=True)
    profile.update(profile_fields)
    db.session.commit()

    return jsonify(profile_schema.dump(profile[0]))


@profiles.route("/<int:id>", methods=["DELETE"])
@jwt_required
def delete_profile(id):
    profile = Profile.query.get(id)
    db.session.delete(profile)
    db.session.commit()
    return jsonify(profile_schema.dump(profile))
