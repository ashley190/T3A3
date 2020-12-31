from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models.Profile import Profile
from models.Group import Group
from models.Group_members import GroupMembers
from schemas.GroupSchema import group_schema
from main import db
from forms import (
    CreateGroup, UpdateGroup, DeleteButton, JoinGroup, UnjoinGroup)

web_groups = Blueprint("web_groups", __name__, url_prefix="/web/groups")


@web_groups.route("/", methods=["GET"])
@login_required
def show_groups():
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


@web_groups.route("/create", methods=["GET", "POST"])
@login_required
def create_group():
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
