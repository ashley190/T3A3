from controllers.profiles_controller import profiles
from controllers.users_controller import users
from controllers.groups_controller import groups
from controllers.contents_controller import content


registerable_controllers = [
    users,
    profiles,
    groups,
    content
]
