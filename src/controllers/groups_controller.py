from models.Group import Group
from models.Group_members import GroupMembers
from models.Profile import Profile
from models.User import User
from main import db
from schemas.GroupSchema import group_schema
from schemas.GroupMemberSchema import group_members_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort
groups = Blueprint("groups", __name__, url_prefix="/groups")


def retrieve_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="Invalid user")

    id = request.args["profile_id"]

    profile = Profile.query.filter_by(
        profile_id=id, user_id=user.user_id).first()

    if not profile:
        return abort(404, description="Profile not found")

    return profile


@groups.route("/create", methods=["POST"])
@jwt_required
def create_group():
    profile = retrieve_profile()

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
    profile = retrieve_profile()

    groups = GroupMembers.query.filter_by(profile_id=profile.profile_id).all()

    return jsonify(group_members_schema.dump(groups))
