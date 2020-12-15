from main import ma
from models.Group_members import GroupMembers
from schemas.GroupSchema import GroupSchema


class GroupMemberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = GroupMembers

    profile_id = ma.Integer(required=True)
    admin = ma.Boolean(required=True)
    groups = ma.Nested(GroupSchema)
    # profile = ma.Nested(ProfileSchema)


group_member_schema = GroupMemberSchema()
group_members_schema = GroupMemberSchema(many=True)
