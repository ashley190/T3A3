from main import login_manager
from forms import AdminLoginForm
from sqlalchemy import func
from models.Admin import Admin
from models.User import User
from models.Profile import Profile
from models.Group_members import GroupMembers
from models.Group import Group
from flask_login import login_required, logout_user, login_user, current_user
from flask import (
    Blueprint, render_template, flash, redirect, url_for, request, abort, jsonify)

web_admin = Blueprint("web_admin", __name__, url_prefix="/web/admin")


@login_manager.user_loader
def load_user(admin_id):
    if admin_id is not None:
        return Admin.query.get(admin_id)
    return None


@login_manager.unauthorized_handler
def unauthorised():
    flash("You must be logged in to view this page")
    return redirect(url_for('web_admin.admin_login'))


@web_admin.route("/login", methods=["GET", "POST"])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin and admin.check_password(password=form.password.data):
            login_user(admin)
            next_page = request.args.get('next')
            return redirect(next_page or url_for("web_admin.view_users"))
        flash("Invalid username and password")
        return redirect(url_for("web_admin.admin_login"))
    return render_template("user_login.html", form=form)


@web_admin.route("/logout")
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for("web_admin.admin_login"))


@web_admin.route("/users", methods=["GET"])
@login_required
def view_users():
    if not load_user(current_user.get_id()):
        return abort(401, description="Unauthorised to view users")

    query = User.query.with_entities(
        User.user_id, User.email, func.count(Profile.profile_id).label(
            'profile_count')).outerjoin(Profile).group_by(
                User.user_id).order_by(User.user_id)
    # SELECT users.user_id AS users_user_id, users.email AS users_email,
    # count(profiles.profile_id) AS profile_count
    # FROM users
    # LEFT OUTER JOIN profiles ON users.user_id = profiles.user_id
    # GROUP BY users.user_id
    # ORDER BY users.user_id

    return render_template("admin_users.html", query=query)


@web_admin.route("/groups", methods=["GET"])
@login_required
def view_groups():
    if not load_user(current_user.get_id()):
        return abort(401, description="Unauthorised to view users")

    query = GroupMembers.query.with_entities(GroupMembers.group_id, Group.name, func.count(GroupMembers.profile_id).label("members")).outerjoin(Group).group_by(GroupMembers.group_id, Group.name).order_by(GroupMembers.group_id)
    # SELECT group_members.group_id AS group_members_group_id, groups.name AS groups_name, count(group_members.profile_id) AS members FROM group_members LEFT OUTER JOIN groups ON groups.group_id = group_members.group_id GROUP BY group_members.group_id, groups.name ORDER BY group_members.group_id
    # data = []
    # for item in query:
    #     data.append(item)

    return render_template("admin_groups.html", query=query)