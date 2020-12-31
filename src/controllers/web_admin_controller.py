from flask import Blueprint, render_template, flash, redirect, url_for, request
from main import login_manager
from models.Admin import Admin
from forms import AdminLoginForm
from flask_login import login_required, logout_user, login_user

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


@web_admin.route("/", methods=["GET"])
@login_required
def view_users():
    return render_template("admin_users.html")
