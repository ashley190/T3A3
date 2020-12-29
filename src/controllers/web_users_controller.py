from flask import Blueprint


web_users = Blueprint("web_users", __name__, url_prefix="/web")


@web_users.route("/register", methods=["GET", "POST"])
def web_users_register():
    pass


@web_users.route("/login", methods=["GET", "POST"])
def web_users_login():
    pass
