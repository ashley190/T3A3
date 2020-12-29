from models.User import User
from main import db, login_manager
from flask import Blueprint, render_template, flash, redirect, url_for
from forms import RegistrationForm, LoginForm
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
            return "Registration successful. Redirect to home page"
        flash("Email already registered")

    return render_template("user_register.html", form=form)


@web_users.route("/login", methods=["GET", "POST"])
def web_users_login():
    if current_user.is_authenticated:
        return "Redirect to main page"

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(password=form.password.data):
            login_user(user)
            # next_page = request.args.get('next')
            # return redirect(next_page or "Main page")
            return "Login successful"
        flash("Invalid username and password")
        return redirect(url_for("web_users.web_users_login"))
    return render_template("user_login.html", form=form)


@web_users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("web_users.web_users_login"))
