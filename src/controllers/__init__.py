from controllers.profiles_controller import profiles
from controllers.users_controller import users
from controllers.groups_controller import groups
from controllers.contents_controller import content
from controllers.admin_controller import admin
from controllers.web_users_controller import web_users
from controllers.web_profiles_controller import web_profiles
from controllers.web_groups_controller import web_groups
from controllers.web_admin_controller import web_admin

registerable_controllers = [
    users,
    profiles,
    groups,
    content,
    admin,
    web_users,
    web_profiles,
    web_groups,
    web_admin
]
