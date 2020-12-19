from models.Group import Group
from models.Group_members import GroupMembers
from models.Profile import Profile
from models.User import User
from models.Content import Content
from main import db
from schemas.GroupSchema import group_schema
from schemas.GroupMemberSchema import group_members_schema, group_member_schema
from schemas.ProfileSchema import profile_schema
from schemas.ContentSchema import content_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort
groups = Blueprint("groups", __name__, url_prefix="/groups")


def retrieve_profile(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="Invalid user")

    profile = Profile.query.filter_by(
        profile_id=id, user_id=user.user_id).first()

    if not profile:
        return abort(404, description="Profile not found")

    return profile


@groups.route("/", methods=["POST"])
@jwt_required
def create_group():
    profile = retrieve_profile(request.args["profile_id"])

    group_fields = group_schema.load(request.json)
    new_group = Group()
    new_group.name = group_fields["name"]
    new_group.description = group_fields["description"]
    GroupMembers(groups=new_group, profile_id=profile.profile_id, admin=True)

    db.session.add(new_group)
    db.session.commit()

    return jsonify(group_schema.dump(new_group))


@groups.route("/", methods=["GET"])
@jwt_required
def get_groups():
    profile = retrieve_profile(request.args["profile_id"])

    groups = GroupMembers.query.filter_by(profile_id=profile.profile_id).all()

    return jsonify(group_members_schema.dump(groups))


@groups.route("/<int:id>", methods=["GET"])
@jwt_required
def get_group_by_id(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="Invalid user")

    group = Group.query.filter_by(group_id=id).first()

    if not group:
        return abort(404, description="Group not found")

    return jsonify(group_schema.dump(group))


@groups.route("/<int:id>", methods=["PATCH"])
@jwt_required
def update_group(id):
    profile = retrieve_profile(request.args["profile_id"])
    group = GroupMembers.query.filter_by(
        group_id=id, profile_id=profile.profile_id).first()
    group_search = Group.query.filter_by(group_id=id)

    if not group:
        return abort(404, description="Group not found")

    group_fields = group_schema.load(request.json, partial=True)
    if group.admin:
        group_search.update(group_fields)
        db.session.commit()
        return jsonify(group_schema.dump(group_search[0]))
    return abort(401, description="Unauthorised to update")


@groups.route("/<int:id>", methods=["DELETE"])
@jwt_required
def delete_group(id):
    profile = retrieve_profile(request.args["profile_id"])
    group = GroupMembers.query.filter_by(
        group_id=id, profile_id=profile.profile_id).first()
    group_search = Group.query.filter_by(group_id=id).first()

    if not group or not group_search:
        return abort(404, description="Group not found")

    if group.admin:
        while len(group_search.content) > 0:
            for item in group_search.content:
                group_search.content.remove(item)
            db.session.commit()
        db.session.delete(group)
        db.session.delete(group_search)
        db.session.commit()
        return jsonify(group_schema.dump(group_search))

    return abort(401, description="Unauthorised to delete")


@groups.route("/<int:id>/join", methods=["POST"])
@jwt_required
def join_group(id):
    profile = profile_schema.load(request.json, partial=True)
    user_profile = retrieve_profile(profile["profile_id"])

    group = GroupMembers.query.filter_by(
        group_id=id, profile_id=user_profile.profile_id).first()

    if not group:
        new_member = GroupMembers()
        new_member.group_id = id
        new_member.profile_id = user_profile.profile_id
        new_member.admin = False
        user_profile.groups.append(new_member)
        db.session.commit()
        return jsonify(group_member_schema.dump(new_member))
    else:
        return abort(401, description="already a member")


@groups.route("/<int:id>/unjoin", methods=["DELETE"])
@jwt_required
def unjoin_group(id):
    profile = profile_schema.load(request.json, partial=True)
    user_profile = retrieve_profile(profile["profile_id"])

    group = GroupMembers.query.filter_by(
        group_id=id, profile_id=user_profile.profile_id).first()

    if not group:
        return abort(401, description="Not a member of this group")

    db.session.delete(group)
    db.session.commit()

    return "Unjoined group"


@groups.route("/<int:id>/remove_member", methods=["DELETE"])
@jwt_required
def remove_member(id):
    member_profile = profile_schema.load(request.json, partial=True)
    admin_profile = retrieve_profile(request.args["adminprofile_id"])

    retrieve_member = GroupMembers.query.filter_by(
        group_id=id, profile_id=member_profile["profile_id"]).first()

    if not retrieve_member:
        return abort(401, description="Not a member of this group")

    retrieve_admin = GroupMembers.query.filter_by(
        group_id=id, profile_id=admin_profile.profile_id).first()

    if not retrieve_admin:
        return abort(401, description="Does not belong to this group")

    if retrieve_admin.admin is True:
        db.session.delete(retrieve_member)
        db.session.commit()
        return f"member {retrieve_member.profile_id} removed."
    elif retrieve_admin.admin is False:
        return abort(401, description="Not authorized")


@groups.route("/<int:id>/content", methods=["POST"])
@jwt_required
def add_content(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="Invalid user")

    content = content_schema.load(request.json, partial=True)
    content_search = Content.query.filter_by(
        content_id=content["content_id"]).first()

    if not content_search:
        return abort(404, description="content not found")

    group = Group.query.filter_by(group_id=id).first()

    if not group:
        return abort(404, description="group not found")

    # for item in group.content:
    #     if item.content_id == content["content_id"]:
    #         return abort(401, description="Content already exists")

    group.content.append(content_search)
    db.session.commit()

    return jsonify(group_schema.dump(group))


@groups.route("/<int:id>/content", methods=["DELETE"])
@jwt_required
def remove_content(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="Invalid user")

    content = content_schema.load(request.json, partial=True)
    group = Group.query.filter_by(group_id=id).first()

    if not group:
        return abort(404, description="group not found")

    for item in group.content:
        if item.content_id == content["content_id"]:
            group.content.remove(item)
            db.session.commit()
            return jsonify(group_schema.dump(group))

    return abort(404, description="Content not found")
