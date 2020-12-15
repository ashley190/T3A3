from main import ma
from models.Content import Content
from marshmallow.validate import Length


class ContentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Content

    title = ma.String(required=True, validate=Length(min=1))
    genre = ma.String()
    year = ma.Integer()


content_schema = ContentSchema()
contents_schema = ContentSchema(many=True)
