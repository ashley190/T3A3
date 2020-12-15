from models.Content import Content
from schemas.ContentSchema import content_schema
from main import db
from flask import Blueprint, request, jsonify


content = Blueprint("content", __name__, url_prefix="/content")


@content.route("/", methods=["POST"])
def create_content():
    content_fields = content_schema.load(request.json)
    new_content = Content()
    new_content.title = content_fields["title"]
    new_content.genre = content_fields["genre"]
    new_content.year = content_fields["year"]

    db.session.add(new_content)
    db.session.commit()

    return jsonify(content_schema.dump(new_content))
