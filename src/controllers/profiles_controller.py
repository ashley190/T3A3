from models.Profile import Profile
from models.User import User
from main import db
from schemas.ProfileSchema import profile_schema, profiles_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort
profiles = Blueprint('profiles', __name__, url_prefix="/profiles")


@profiles.route("/", methods=["GET"])
@jwt_required
def show_profiles():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    profiles = Profile.query.filter_by(user_id=user.user_id)

    return jsonify(profiles_schema.dump(profiles))


@profiles.route("/create", methods=["POST"])
@jwt_required
def create_profile():
    profile_fields = profile_schema.load(request.json)
    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if not user:
        return abort(401, description="Invalid user")

    new_profile = Profile()
    new_profile.name = profile_fields["name"]
    new_profile.restrictions = profile_fields["restrictions"]

    user.profiles.append(new_profile)
    db.session.commit()

    return jsonify(profile_schema.dump(new_profile))


@profiles.route("/<int:id>", methods=["PATCH"])
@jwt_required
def update_profile(id):
    profile_fields = profile_schema.load(request.json, partial=True)
    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if not user:
        return abort(401, description="Invalid user")

    profile = Profile.query.filter_by(profile_id=id, user_id=user.user_id)

    if profile.count() != 1:
        return abort(401, description="Unauthorised to update this profile")

    profile.update(profile_fields)
    db.session.commit()

    return jsonify(profile_schema.dump(profile[0]))


@profiles.route("/<int:id>", methods=["DELETE"])
@jwt_required
def delete_profile(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="Invalid user")

    profile = Profile.query.filter_by(
        profile_id=id, user_id=user.user_id).first()

    if not profile:
        return abort(404, description="Profile not found")

    db.session.delete(profile)
    db.session.commit()

    return jsonify(profile_schema.dump(profile))
