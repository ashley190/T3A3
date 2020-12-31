from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, abort)
from flask_login import login_required
from models.Profile import Profile
from models.Group import Group
from models.Group_members import GroupMembers
from models.Content import Content
from schemas.GroupSchema import group_schema
from main import db, login_manager
from forms import (
    CreateGroup, UpdateGroup, DeleteButton,
    JoinGroup, UnjoinGroup, RemoveButton, AddButton)
from flask_login import current_user
from models.User import User

web_groups = Blueprint("web_groups", __name__, url_prefix="/web/groups")


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None


@web_groups.route("/", methods=["GET"])
@login_required
def show_groups():
    if not load_user(current_user.get_id()):
        return abort(401, description="Unauthorised to view this page")

    profile = Profile.query.filter_by(
        profile_id=request.args["profile_id"]).first()
    groups = GroupMembers.query.filter_by(
        profile_id=profile.profile_id).order_by(GroupMembers.group_id)
    other_groups = Group.query.all()

    member_group_ids = [group.groups.group_id for group in groups]
    form = DeleteButton()
    form2 = JoinGroup()
    form3 = UnjoinGroup()
    return render_template(
        "groups.html", groups=groups, other_groups=other_groups,
        member_group_ids=member_group_ids, profile=profile, form=form,
        form2=form2, form3=form3)


@web_groups.route("/<int:id>", methods=["GET"])
@login_required
def view_group(id):
    if not load_user(current_user.get_id()):
        return abort(401, description="Unauthorised to view this page")

    # Check admin status
    profile_id = request.args["profile_id"]
    admin_check = GroupMembers.query.filter_by(
        profile_id=profile_id, group_id=id).first()

    # Retrieve group members
    members = GroupMembers.query.with_entities(
        GroupMembers.group_id, GroupMembers.profile_id,
        Profile.name).filter_by(group_id=id).outerjoin(Profile)
    # SELECT group_members.group_id AS group_members_group_id,
    # profiles.name AS profiles_name
    # FROM group_members
    # LEFT OUTER JOIN profiles
    # ON profiles.profile_id = group_members.profile_id
    # WHERE group_members.group_id = %(group_id_1)s

    # Retrieve group details
    group = Group.query.filter_by(group_id=id).first()

    # load remove button
    form = RemoveButton()

    return render_template(
        "view_group.html", id=id, admin_check=admin_check, members=members,
        group=group, form=form, profile_id=profile_id)


@web_groups.route("/create", methods=["GET", "POST"])
@login_required
def create_group():
    if not load_user(current_user.get_id()):
        return abort(401, description="Unauthorised to view this page")

    profile = Profile.query.filter_by(
        profile_id=request.args["profile_id"]).first()

    form = CreateGroup()
    if form.validate_on_submit():
        new_group = Group(
            name=form.name.data,
            description=form.description.data,
        )
        GroupMembers(
            groups=new_group, profile_id=profile.profile_id, admin=True)

        db.session.add(new_group)
        db.session.commit()
        return redirect(
            url_for("web_groups.show_groups", profile_id=profile.profile_id))
    return render_template("create_group.html", form=form, profile=profile)


@web_groups.route("/<int:id>/update", methods=["GET", "POST"])
@login_required
def update_group(id):
    if not load_user(current_user.get_id()):
        return abort(401, description="Unauthorised to view this page")

    profile_id = request.args["profile_id"]
    member = GroupMembers.query.filter_by(
        profile_id=profile_id, group_id=id).first()
    group = Group.query.filter_by(group_id=id)
    if not member.admin:
        flash("Unauthorised to update group")
        return render_template(url_for(
            "web_groups.show_groups", profile_id=profile_id))
    elif member.admin:
        form = UpdateGroup(obj=group.first())
        if form.validate_on_submit():
            data = {
                "name": form.name.data,
                "description": form.description.data
            }
            fields = group_schema.load(data, partial=True)
            group.update(fields)
            db.session.commit()
            flash(f"Group {group.first().group_id} updated!")
            return redirect(url_for(
                "web_groups.show_groups", profile_id=profile_id))
        return render_template("update_group.html", id=id, form=form)


@web_groups.route("<int:id>/delete", methods=["POST"])
@login_required
def delete_group(id):
    if not load_user(current_user.get_id()):
        return abort(401, description="Unauthorised to view this page")

    profile_id = request.args["profile_id"]
    member = GroupMembers.query.filter_by(
        profile_id=profile_id, group_id=id).first()
    group = Group.query.filter_by(group_id=id).first()
    members = GroupMembers.query.filter_by(group_id=id, admin=False).all()
    if not member.admin:
        flash("Unauthorised to delete group")
        return render_template(url_for(
            "web_groups.show_groups", profile_id=profile_id))
    elif member.admin:
        form = DeleteButton()
        if form.submit.data:
            while len(group.content) > 0:
                for content in group.content:
                    group.content.remove(content)
                db.session.commit()

            for profile in members:
                db.session.delete(profile)
            db.session.commit()

            db.session.delete(member)
            db.session.delete(group)
            db.session.commit()
            flash(f"Group {group.group_id} deleted!")
        return redirect(url_for(
            "web_groups.show_groups", profile_id=profile_id))


@web_groups.route("/<int:id>/join", methods=["POST"])
@login_required
def join_group(id):
    if not load_user(current_user.get_id()):
        return abort(401, description="Unauthorised to view this page")

    form = JoinGroup()
    if form.submit.data:
        profile = Profile.query.filter_by(
            profile_id=request.args["profile_id"]).first()
        member = GroupMembers.query.filter_by(
            group_id=id, profile_id=profile.profile_id).first()

        if not member:
            new_member = GroupMembers()
            new_member.group_id = id
            new_member.profile_id = profile.profile_id
            new_member.admin = False
            profile.groups.append(new_member)
            db.session.commit()
            flash(f"Joined group {id}")
            return redirect(url_for(
                "web_groups.show_groups", profile_id=profile.profile_id))
        flash(f"Unable to join group {id}")
        return redirect(url_for(
            "web_groups.show_groups", profile_id=profile.profile_id))


@web_groups.route("/<int:id>/unjoin", methods=["POST"])
@login_required
def unjoin_group(id):
    if not load_user(current_user.get_id()):
        return abort(401, description="Unauthorised to view this page")

    form = UnjoinGroup()
    if form.submit.data:
        profile = Profile.query.filter_by(
            profile_id=request.args["profile_id"]).first()
        member = GroupMembers.query.filter_by(
            group_id=id, profile_id=profile.profile_id).first()

        if not member:
            flash(f"Not a member of group {id}")
            return redirect(url_for(
                "web_groups.show_groups", profile_id=profile.profile_id))

        db.session.delete(member)
        db.session.commit()
        flash(f"Unjoined group {id}")
        return redirect(url_for(
            "web_groups.show_groups", profile_id=profile.profile_id))


@web_groups.route("/<int:id>/<int:member_id>/remove", methods=["POST"])
@login_required
def remove_member(id, member_id):
    if not load_user(current_user.get_id()):
        return abort(401, description="Unauthorised to view this page")

    form = RemoveButton()
    if form.submit.data:
        member = GroupMembers.query.filter_by(
            group_id=id, profile_id=member_id).first()

        if not member:
            flash("Member not found")
            return redirect(url_for(
                "web_groups.view_group", id=id,
                profile_id=request.args["profile_id"]))

        db.session.delete(member)
        db.session.commit()
        flash(f"Member {member.profile_id} removed")
        return redirect(url_for(
            "web_groups.view_group", id=id,
            profile_id=request.args["profile_id"]))


@web_groups.route("/<int:id>/addcontent", methods=["GET", "POST"])
@login_required
def add_content(id):
    if not load_user(current_user.get_id()):
        return abort(401, description="Unauthorised to view this page")

    group = Group.query.filter_by(group_id=id).first()
    content = Content.query.all()
    form = AddButton()
    if form.submit.data:
        group = GroupMembers.query.filter_by(
            profile_id=request.args["profile_id"], group_id=id).first()
        content = Content.query.get(request.args["content_id"])

        group.groups.content.append(content)
        db.session.commit()
        flash(f"Added content {content.title} to group {id}")
        return redirect(url_for(
            "web_groups.view_group", id=id,
            profile_id=request.args["profile_id"]))

    return render_template(
        "content.html", group=group, content=content, form=form,
        id=id, profile_id=request.args["profile_id"])


@web_groups.route("/<int:id>/removecontent", methods=["POST"])
@login_required
def remove_content(id):
    if not load_user(current_user.get_id()):
        return abort(401, description="Unauthorised to view this page")

    form = RemoveButton()
    if form.submit.data:
        group = Group.query.filter_by(group_id=id).first()
        content = Content.query.filter_by(
            content_id=request.args["content_id"]).first()

        for item in group.content:
            if item == content:
                group.content.remove(item)
                db.session.commit()
                flash(f"Removed content {item.title} from group {id}")

    return redirect(url_for(
        "web_groups.view_group", id=id,
        profile_id=request.args["profile_id"]))
