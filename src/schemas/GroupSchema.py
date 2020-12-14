from main import ma
from models.Group import Group
from marshmallow.validate import Length


class GroupSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Group

    name = ma.String(required=True, validate=Length(min=1))
    description = ma.String()
    admin = ma.Boolean(required=False)


group_schema = GroupSchema()
groups_schema = GroupSchema(many=True)
