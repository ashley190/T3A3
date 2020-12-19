from models.Profile import Profile
from models.Content import Content
from models.User import User
from models.Group_members import GroupMembers
from main import db
from schemas.ProfileSchema import profile_schema, profiles_schema
from schemas.ContentSchema import content_schema, contents_schema
from controllers.groups_controller import retrieve_profile
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort
profiles = Blueprint('profiles', __name__, url_prefix="/profiles")


@profiles.route("/", methods=["GET"])
@jwt_required
def show_profiles():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="Invalid user")

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


@profiles.route("/<int:id>", methods=["GET"])
@jwt_required
def get_profile_by_id(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="Invalid user")

    profile = Profile.query.filter_by(profile_id=id, user_id=user.user_id)

    if profile.count() != 1:
        return abort(404, description="Profile not found")

    return jsonify(profile_schema.dump(profile[0]))


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

    while len(profile.unrecommend) > 0:
        for item in profile.unrecommend:
            profile.unrecommend.remove(item)
        db.session.commit()

    groups = GroupMembers.query.filter_by(profile_id=profile.profile_id)
    for group in groups:
        db.session.delete(group)
        db.session.commit()

    db.session.delete(profile)
    db.session.commit()

    return jsonify(profile_schema.dump(profile))


@profiles.route("/<int:id>/unrecommend", methods=["GET"])
@jwt_required
def unrecommended_content(id):
    profile = retrieve_profile(id)

    return jsonify(contents_schema.dump(profile.unrecommend))


@profiles.route("/<int:id>/unrecommend", methods=["PUT"])
@jwt_required
def unrecommend_content(id):
    profile = retrieve_profile(id)

    content = content_schema.load(request.json, partial=True)
    content_search = Content.query.filter_by(
        content_id=content["content_id"]).first()

    if not content_search:
        return abort(404, description="content not found")

    profile.unrecommend.append(content_search)
    db.session.commit()

    return jsonify(contents_schema.dump(profile.unrecommend))


@profiles.route("/<int:id>/unrecommend", methods=["DELETE"])
@jwt_required
def remove_content(id):
    profile = retrieve_profile(id)
    content = content_schema.load(request.json, partial=True)

    for item in profile.unrecommend:
        if item.content_id == content["content_id"]:
            profile.unrecommend.remove(item)
            db.session.commit()
            return jsonify(contents_schema.dump(profile.unrecommend))

    return abort(404, description="Content not found")
