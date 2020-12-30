from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from models.Profile import Profile
from models.Group import Group
from models.Group_members import GroupMembers
from main import db
from forms import CreateGroup

web_groups = Blueprint("web_groups", __name__, url_prefix="/web/groups")


@web_groups.route("/", methods=["GET"])
@login_required
def show_groups():
    profile = Profile.query.filter_by(
        profile_id=request.args["profile_id"]).first()
    groups = GroupMembers.query.filter_by(profile_id=profile.profile_id).all()
    other_groups = Group.query.all()

    member_group_ids = [group.groups.group_id for group in groups]
    return render_template(
        "groups.html", groups=groups, other_groups=other_groups,
        member_group_ids=member_group_ids, profile=profile)


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
