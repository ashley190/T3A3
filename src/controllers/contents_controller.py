from models.Content import Content
from models.User import User
from schemas.ContentSchema import content_schema, contents_schema
from main import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort


content = Blueprint("content", __name__, url_prefix="/content")


@content.route("/", methods=["POST"])
@jwt_required
def create_content():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="Invalid user")

    content_fields = content_schema.load(request.json)
    new_content = Content()
    new_content.title = content_fields["title"]
    new_content.genre = content_fields["genre"]
    new_content.year = content_fields["year"]

    db.session.add(new_content)
    db.session.commit()

    return jsonify(content_schema.dump(new_content))


@content.route("/", methods=["GET"])
@jwt_required
def get_content():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="Invalid user")

    content = Content.query.all()
    return jsonify(contents_schema.dump(content))


@content.route("/<int:id>", methods=["DELETE"])
@jwt_required
def delete_content(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="Invalid user")

    content = Content.query.filter_by(content_id=id).first()

    if not content:
        return abort(404, description="Content not found")

    db.session.delete(content)
    db.session.commit()

    return jsonify(content_schema.dump(content))
