from main import ma
from models.Group import Group
from schemas.ContentSchema import contents_schema
from marshmallow.validate import Length


class GroupSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Group

    name = ma.String(required=True, validate=Length(min=1))
    description = ma.String()
    content = ma.Nested(contents_schema)


group_schema = GroupSchema()
groups_schema = GroupSchema(many=True)
