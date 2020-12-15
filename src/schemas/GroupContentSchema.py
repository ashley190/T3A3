from main import ma
from models.Group_content import GroupContent
from schemas.ContentSchema import ContentSchema


class GroupContentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = GroupContent

    group_id = ma.Integer(required=True)
    contents = ma.Nested(ContentSchema)
