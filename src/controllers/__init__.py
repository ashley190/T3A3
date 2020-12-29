from controllers.profiles_controller import profiles
from controllers.users_controller import users
from controllers.groups_controller import groups
from controllers.contents_controller import content
from controllers.admin_controller import admin
from controllers.web_users_controller import web_users
from controllers.web_profiles_controller import web_profiles


registerable_controllers = [
    users,
    profiles,
    groups,
    content,
    admin,
    web_users,
    web_profiles
]
