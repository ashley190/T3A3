from main import ma
from models.Admin import Admin
from marshmallow.validate import Length


class AdminSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Admin
        load_only = ["password"]

        email = ma. String(required=True, validate=Length(min=4))
        password = ma.String(required=True, validate=Length(min=6))


admin_schema = AdminSchema()
admins_schema = AdminSchema(many=True)


class AdminUserSchema(ma.Schema):
    email = ma.Email()
    profile_count = ma.Integer()


admin_user_schema = AdminUserSchema()
admin_users_schema = AdminUserSchema(many=True)


class AdminGroupSchema(ma.Schema):
    group_id = ma.Integer()
    members = ma.Integer()


admin_group_schema = AdminGroupSchema()
admin_groups_schema = AdminGroupSchema(many=True)


class AdminContentSchema(ma.Schema):
    content_id = ma.Integer()
    unrecommended = ma.Integer()


admin_content_schema = AdminContentSchema()
admin_contents_schema = AdminContentSchema(many=True)


class AdminGroupContentSchema(ma.Schema):
    content_id = ma.Integer()
    group_count = ma.Integer()


admin_groupcontent_schema = AdminGroupContentSchema()
admin_groupcontents_schema = AdminGroupContentSchema(many=True)
