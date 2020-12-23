from models.Admin import Admin
from models.User import User
from models.Group import Group
from models.Profile import Profile
from models.Content import Content
from models.joined_tables import unrecommend, group_content
from models.Group_members import GroupMembers
from schemas.AdminSchema import (
    admin_schema, admin_users_schema, admin_groups_schema,
    admin_contents_schema, admin_groupcontents_schema)
from schemas.ContentSchema import content_schema
# from schemas.GroupSchema import groups_schema
# from schemas.ProfileSchema import profiles_schema
from main import bcrypt, db
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


@admin.route("/groups", methods=["GET"])
@jwt_required
def get_groups():
    admin_id = get_jwt_identity()

    admin = Admin.query.get(admin_id)

    if not admin:
        return abort(401, description="Invalid admin user")

    query = GroupMembers.query.with_entities(
        GroupMembers.group_id, func.count(GroupMembers.profile_id).label(
            "members")).group_by(
                GroupMembers.group_id).order_by(GroupMembers.group_id)
    # SELECT group_members.group_id AS group_members_group_id,
    # count(group_members.profile_id)
    # AS members
    # FROM group_members
    # GROUP BY group_members.group_id ORDER BY group_members.group_id
    return jsonify(admin_groups_schema.dump(query))


@admin.route("/content", methods=["GET"])
@jwt_required
def get_content():
    admin_id = get_jwt_identity()

    admin = Admin.query.get(admin_id)

    if not admin:
        return abort(401, description="Invalid admin user")

    query = Content.query.with_entities(
        Content.content_id, func.count(Profile.profile_id).label(
            'unrecommended')).select_from(Content).join(
                unrecommend).join(Profile).group_by(
                    Content.content_id).order_by(Content.content_id)
    # SELECT content.content_id AS content_content_id,
    # count(profiles.profile_id) AS unrecommended
    # FROM content
    # JOIN unrecommend ON content.content_id = unrecommend.content_id
    # JOIN profiles ON profiles.profile_id = unrecommend.profile_id
    # GROUP BY content.content_id ORDER BY content.content_id

    return jsonify(admin_contents_schema.dump(query))


@admin.route("/groupcontent", methods=["GET"])
@jwt_required
def get_group_content():
    admin_id = get_jwt_identity()

    admin = Admin.query.get(admin_id)

    if not admin:
        return abort(401, description="Invalid admin user")

    query = Content.query.with_entities(
        Content.content_id, func.count(Group.group_id).label(
            'group_count')).select_from(Content).join(
                group_content).join(Group).group_by(
                    Content.content_id).order_by(Content.content_id)
    # SELECT content.content_id AS content_content_id,
    # count(groups.group_id) AS "group_count"
    # FROM content
    # JOIN group_content ON content.content_id = group_content.content_id
    # JOIN groups ON groups.group_id = group_content.group_id
    # GROUP BY content.content_id ORDER BY content.content_id
    return jsonify(admin_groupcontents_schema.dump(query))


@admin.route("/content", methods=["POST"])
@jwt_required
def create_content():
    admin_id = get_jwt_identity()

    admin = Admin.query.get(admin_id)

    if not admin:
        return abort(401, description="Invalid admin user")

    content_fields = content_schema.load(request.json)
    new_content = Content()
    new_content.title = content_fields["title"]
    new_content.genre = content_fields["genre"]
    new_content.year = content_fields["year"]

    db.session.add(new_content)
    db.session.commit()

    return jsonify(content_schema.dump(new_content))

# @admin.route("/content", methods=["DELETE"])
# @jwt_required
# def delete_content():
#     admin_id = get_jwt_identity()

#     admin = Admin.query.get(admin_id)

#     if not admin:
#         return abort(401, description="Invalid admin user")

#     id = request.args["content_id"]

#     content = Content.query.filter_by(
# content_id=request.args["content_id"]).first()

#     return jsonify(content_schema.dump(content))
