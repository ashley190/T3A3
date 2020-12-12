from main import ma
from models.Profile import Profile


class ProfileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Profile


profile_schema = ProfileSchema()
profiles_schema = ProfileSchema(many=True)
