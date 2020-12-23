from models.Content import Content
from models.User import User
from schemas.ContentSchema import contents_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, jsonify, abort


content = Blueprint("content", __name__, url_prefix="/content")


@content.route("/", methods=["GET"])
@jwt_required
def get_content():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="Invalid user")

    content = Content.query.all()
    return jsonify(contents_schema.dump(content))
