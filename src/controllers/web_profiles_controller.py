from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from controllers.web_users_controller import load_user
from models.Profile import Profile
from models.Group_members import GroupMembers
from models.Content import Content
from schemas.ProfileSchema import profile_schema
from forms import CreateProfile, UpdateProfile, DeleteButton, UnrecommendButton, RemoveButton
from main import db

web_profiles = Blueprint("web_profiles", __name__, url_prefix="/web/profiles")


@web_profiles.route("/", methods=["GET"])
@login_required
def show_profiles():
    user = load_user(current_user.get_id())
    profiles = Profile.query.filter_by(
        user_id=user.user_id).order_by(Profile.profile_id)

    form = DeleteButton()
    return render_template("profiles.html", profiles=profiles, form=form)


@web_profiles.route("/create", methods=["GET", "POST"])
@login_required
def create_profile():
    user = load_user(current_user.get_id())

    form = CreateProfile()
    if form.validate_on_submit():
        new_profile = Profile(
            name=form.name.data,
            restrictions=form.restriction.data
        )
        user.profiles.append(new_profile)
        db.session.commit()
        flash("Profile added!")
        return redirect(url_for("web_profiles.show_profiles"))

    return render_template("create_profile.html", form=form)


@web_profiles.route("/<int:id>/update", methods=["GET", "POST"])
@login_required
def update_profile(id):
    user = load_user(current_user.get_id())
    profile = Profile.query.filter_by(profile_id=id, user_id=user.user_id)

    if profile.count() != 1:
        flash("Can't find profile")
        return redirect(url_for("web_profiles.show_profiles"))

    form = UpdateProfile(obj=profile.first())
    if form.validate_on_submit():
        data = {
            "name": form.name.data,
            "restrictions": form.restriction.data
        }
        fields = profile_schema.load(data, partial=True)
        profile.update(fields)
        db.session.commit()
        flash("Profile updated!")
        return redirect(url_for("web_profiles.show_profiles"))

    return render_template("update_profile.html", form=form, id=id)


@web_profiles.route("/<int:id>/delete", methods=["POST"])
@login_required
def delete_profile(id):
    form = DeleteButton()
    if form.submit.data:
        user = load_user(current_user.get_id())
        profile = Profile.query.filter_by(
            profile_id=id, user_id=user.user_id).first()

        if not profile:
            flash("No profile found")
            return redirect(url_for("web_profiles.show_profiles"))

        while len(profile.unrecommend) > 0:
            for item in profile.unrecommend:
                profile.unrecommend.remove(item)
            db.session.commit()

        groups = GroupMembers.query.filter_by(profile_id=profile.profile_id)
        for group in groups:
            db.session.delete(group)
            db.session.commit()

        db.session.delete(profile)
        db.session.commit()

        flash("Profile deleted")
        return redirect(url_for("web_profiles.show_profiles"))


@web_profiles.route("/<int:id>", methods=["GET"])
@login_required
def view_profile(id):
    user = load_user(current_user.get_id())

    profile = Profile.query.filter_by(
        profile_id=id, user_id=user.user_id).first()

    if not profile:
        flash("Profile not found")
        return redirect(url_for("web_profiles.view_profile"))

    contents = Content.query.all()

    form1 = UnrecommendButton()
    form2 = RemoveButton()

    return render_template(
        "view_profile.html", contents=contents, profile=profile, form1=form1, form2=form2)


@web_profiles.route("/<int:id>/<int:content_id>/unrecommend", methods=["POST"])
@login_required
def unrecommend_content(id, content_id):
    form = UnrecommendButton()
    if form.submit.data:
        profile = Profile.query.filter_by(profile_id=id).first()

        content = Content.query.filter_by(content_id=content_id).first()

        profile.unrecommend.append(content)
        db.session.commit()

        return redirect(url_for("web_profiles.view_profile", id=profile.profile_id))


@web_profiles.route("/<int:id>/<int:content_id>/restore", methods=["POST"])
@login_required
def restore_content(id, content_id):
    form = RemoveButton()
    if form.submit.data:
        profile = Profile.query.filter_by(profile_id=id).first()
        content = Content.query.filter_by(content_id=content_id).first()

        for item in profile.unrecommend:
            if item.content_id == content.content_id:
                profile.unrecommend.remove(item)
                db.session.commit()
        return redirect(url_for("web_profiles.view_profile", id=profile.profile_id))
