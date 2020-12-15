from main import ma
from models.Unrecommend import Unrecommend
from schemas.ContentSchema import ContentSchema


class UnrecommendSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Unrecommend

    profile_id = ma.Integer(required=True)
    contents = ma.Nested(ContentSchema)
