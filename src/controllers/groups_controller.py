from models.Group import Group
from models.Profile import Profile
from models.User import User
from main import db
from schemas.GroupSchema import group_schema
# from schemas.ProfileSchema import profile_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort
groups = Blueprint("groups", __name__, url_prefix="/groups")


@groups.route("/create", methods=["POST"])
@jwt_required
def create_group():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="Invalid user")

    id = request.args["profile_id"]

    profile = Profile.query.filter_by(
        profile_id=id, user_id=user.user_id).first()

    # if profile.count() != 1:
    #     return abort(404, description="Profile not found")

    group_fields = group_schema.load(request.json)
    new_group = Group()
    new_group.name = group_fields["name"]
    new_group.description = group_fields["description"]
    new_group.admin = group_fields["admin"]

    profile.groups.append(new_group)
    db.session.commit()

    return jsonify(group_schema.dump(new_group))
