from models.User import User
from models.Profile import Profile
from main import db, login_manager
from schemas.UserSchema import user_schema
from flask import (
    Blueprint, render_template, flash, redirect, url_for, abort, request)
from forms import RegistrationForm, LoginForm, UpdateUserForm, DeleteButton
from flask_login import current_user, login_required, logout_user, login_user


web_users = Blueprint("web_users", __name__, url_prefix="/web")


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorised():
    flash("You must be logged in to view this page")
    return redirect(url_for('web_users.web_users_login'))


@web_users.route("/register", methods=["GET", "POST"])
def web_users_register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if not existing_user:
            new_user = User(
                email=form.email.data,
                subscription_status=form.subscription_status.data
            )
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for("web_profiles.show_profiles"))
        flash("Email already registered")
        return redirect(url_for("web_users.web_users_login"))
    return render_template("user_register.html", form=form)


@web_users.route("/login", methods=["GET", "POST"])
def web_users_login():
    if current_user.is_authenticated:
        return redirect(url_for("web_profiles.show_profiles"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(password=form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for("web_profiles.show_profiles"))
        flash("Invalid email and password")
        return redirect(url_for("web_users.web_users_login"))
    return render_template("user_login.html", form=form)


@web_users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("web_users.web_users_login"))


@web_users.route("/account", methods=["GET"])
@login_required
def get_user():
    user = load_user(current_user.get_id())

    if not user:
        return abort(401, description="Unauthorised to view this page")

    subscription_status = "Inactive"
    if user.subscription_status:
        subscription_status = "Active"

    form = DeleteButton()
    return render_template(
        "account_details.html",
        user=user,
        subscription=subscription_status, form=form)


@web_users.route("/account/update", methods=["GET", "POST"])
@login_required
def update_user():
    user_id = current_user.get_id()
    user = User.query.filter_by(user_id=user_id)

    form = UpdateUserForm(obj=user.first())
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if form.email.data != user.first().email and existing_user:
            return abort(401, description="Email already registered")
        else:
            data = {
                "email": form.email.data,
                "subscription_status": form.subscription_status.data
            }
            fields = user_schema.load(data, partial=True)
            user.update(fields)
            db.session.commit()
            flash("Account updated!")
            return redirect(url_for("web_users.get_user"))
    return render_template("user_update.html", form=form, user=user)


@web_users.route("/account/delete", methods=["POST"])
@login_required
def delete_user():
    form = DeleteButton()
    if form.submit.data:
        user_id = current_user.get_id()
        user = User.query.get(user_id)

        profiles = Profile.query.filter_by(user_id=user.user_id)
        for profile in profiles:
            while len(profile.unrecommend) > 0:
                for item in profile.unrecommend:
                    profile.unrecommend.remove(item)
                db.session.commit()

        db.session.delete(user)
        db.session.commit()
        logout_user()
        flash("Account deleted")
        return redirect(url_for("web_users.web_users_login"))
    return redirect(url_for("web_users.get_user"))
