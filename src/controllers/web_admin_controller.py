from main import db, login_manager
from forms import AdminLoginForm
from sqlalchemy import func
from models.Admin import Admin
from models.User import User
from models.Profile import Profile
from models.Group_members import GroupMembers
from models.Group import Group
from models.joined_tables import unrecommend, group_content
from models.Content import Content
from forms import DeleteButton, CreateContent, RestoreButton, BackupButton
from flask_login import login_required, logout_user, login_user, current_user
from flask import (
    Blueprint, render_template, flash, redirect, url_for, request, abort)
import os
import sys
from datetime import datetime


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
        return abort(401, description="Unauthorised to view this page")

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
        return abort(401, description="Unauthorised to view this page")

    query = GroupMembers.query.with_entities(
        GroupMembers.group_id, Group.name, func.count(
            GroupMembers.profile_id).label(
                "members")).outerjoin(Group).group_by(
                    GroupMembers.group_id, Group.name).order_by(
                        GroupMembers.group_id)
    # SELECT group_members.group_id AS group_members_group_id,
    # groups.name AS groups_name,count(group_members.profile_id) AS members
    # FROM group_members
    # LEFT OUTER JOIN groups ON groups.group_id = group_members.group_id
    # GROUP BY group_members.group_id, groups.name
    # ORDER BY group_members.group_id

    return render_template("admin_groups.html", query=query)


@web_admin.route("/content", methods=["GET"])
@login_required
def view_content():
    if not load_user(current_user.get_id()):
        return abort(401, description="Unauthorised to view this page")

    query1 = Content.query.with_entities(
        Content.content_id, Content.title, func.count(
            Profile.profile_id).label("unrecommended")).select_from(
                Content).outerjoin(unrecommend).outerjoin(Profile).group_by(
                    Content.content_id, Content.title).order_by(
                        Content.content_id)
    # SELECT content.content_id AS content_content_id,
    # content.title AS content_title,
    # count(profiles.profile_id) AS unrecommended
    # FROM content
    # LEFT OUTER JOIN unrecommend
    # ON content.content_id = unrecommend.content_id
    # LEFT OUTER JOIN profiles ON profiles.profile_id = unrecommend.profile_id
    # GROUP BY content.content_id, content.title
    # ORDER BY content.content_id

    query2 = Content.query.with_entities(Content.content_id, func.count(
        Group.group_id).label("group_count")).select_from(
            Content).outerjoin(group_content).outerjoin(Group).group_by(
                Content.content_id).order_by(Content.content_id)
    # SELECT content.content_id AS content_content_id,
    # count(groups.group_id) AS group_count
    # FROM content
    # LEFT OUTER JOIN group_content
    # ON content.content_id = group_content.content_id
    # LEFT OUTER JOIN groups ON groups.group_id = group_content.group_id
    # GROUP BY content.content_id ORDER BY content.content_id

    form = DeleteButton()
    form2 = CreateContent()
    return render_template(
        "admin_content.html", query1=query1, query2=query2,
        form=form, form2=form2)


@web_admin.route("/content/add", methods=["GET", "POST"])
@login_required
def create_content():
    if not load_user(current_user.get_id()):
        return abort(401, description="Unauthorised to view this page")

    form = CreateContent()
    if form.validate_on_submit():
        new_content = Content(
            title=form.title.data,
            genre=form.genre.data,
            year=form.year.data
        )

        db.session.add(new_content)
        db.session.commit()
        flash(f"Added {new_content.title}")
        return redirect(url_for("web_admin.view_content"))

    return render_template("admin_create_content.html", form=form)


@web_admin.route("/content/delete/<int:id>", methods=["POST"])
@login_required
def delete_content(id):
    if not load_user(current_user.get_id()):
        return abort(401, description="Unauthorised to view this page")

    form = DeleteButton()
    if form.submit.data:
        content = Content.query.filter_by(content_id=id).first()
        groups = Group.query.all()

        for group in groups:
            for gcontent in group.content:
                if gcontent.content_id == content.content_id:
                    group.content.remove(gcontent)
                    db.session.commit()

        profiles = Profile.query.all()

        for profile in profiles:
            for unrecommended in profile.unrecommend:
                if unrecommended.content_id == content.content_id:
                    profile.unrecommend.remove(unrecommended)
                    db.session.commit()

        db.session.delete(content)
        db.session.commit()

    flash(f"Content {content.content_id} deleted!")
    return redirect(url_for("web_admin.view_content"))


@web_admin.route("/dbbackups", methods=["GET"])
@login_required
def get_backups():
    if not load_user(current_user.get_id()):
        return abort(401, description="Unauthorised to view this page")

    backups = sorted(os.listdir("backup"), reverse=True)
    form = RestoreButton()
    form2 = BackupButton()
    return render_template(
        "admin_backups.html", backups=backups, form=form, form2=form2)


@web_admin.route("/dbrestore/<name>", methods=["POST"])
@login_required
def restore_backup(name):
    if not load_user(current_user.get_id()):
        return abort(401, description="Unauthorised to view this page")

    form = RestoreButton()
    if form.submit.data:
        backup_path = f"backup/{name}"
        tables = [
            "users", "profiles", "groups", "content",
            "group_content", "group_members", "unrecommend"]

        for table in tables:
            cursor = db.session.connection().connection.cursor()
            cursor.execute(f"TRUNCATE TABLE {table} CASCADE")
            path = f"{backup_path}/{table}.csv"

            with open(path, "r") as file:
                cursor.copy_from(file, table, sep=",")
                db.session.commit()

        flash(f"Database restored to {name}")
        return redirect(url_for("web_admin.get_backups"))


@web_admin.route("/downloaddb", methods=["POST"])
@login_required
def download_database():
    if not load_user(current_user.get_id()):
        return abort(401, description="Unauthorised to view this page")

    form = BackupButton()
    if form.submit.data:
        cursor = db.session.connection().connection.cursor()
        cursor.execute(
            """SELECT table_name
            FROM information_schema.tables
            WHERE table_schema='public'""")
        table_names = cursor.fetchall()
        names = []
        for name in table_names:
            names.append(*name)

        timestamp = datetime.now().strftime("%Y-%m-%d;%H%:%M:%S")
        path = f"backup/{timestamp}"

        for name in names:
            filename = f"{path}/{name}.csv"
            if not os.path.exists(os.path.dirname(filename)):
                try:
                    os.makedirs(os.path.dirname(filename))
                except OSError:
                    raise "Can't create path"

            with open(filename, "w") as sys.stdout:
                cursor.copy_to(sys.stdout, f"{name}", sep=",")

        flash("Database backed up")
        return redirect(url_for("web_admin.get_backups"))
