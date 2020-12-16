from main import ma
from models.Profile import Profile
from schemas.UserSchema import UserSchema
from schemas.ContentSchema import contents_schema
from marshmallow.validate import Length, OneOf


class ProfileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Profile

    name = ma.String(required=True, validate=Length(min=1))
    restrictions = ma.String(required=True, validate=OneOf(
        ["G", "PG", "M", "MA15+", "R18+"]))
    user = ma.Nested(UserSchema)
    unrecommend = ma.Nested(contents_schema)


profile_schema = ProfileSchema()
profiles_schema = ProfileSchema(many=True)
