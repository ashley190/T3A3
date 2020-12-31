from flask_wtf import FlaskForm
from wtforms import (
    StringField, BooleanField, SubmitField,
    PasswordField, SelectField, IntegerField)
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField(
        'password', validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField(
        'confirm password', validators=[DataRequired(), EqualTo(
            'password', message='Passwords must match')])
    subscription_status = BooleanField('Subscribe')
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class AdminLoginForm(FlaskForm):
    username = StringField(
        'username', validators=[DataRequired(), Length(min=1)])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class UpdateUserForm(FlaskForm):
    email = StringField('email')
    subscription_status = BooleanField('Subscribe')
    submit = SubmitField("Update Details")


class DeleteButton(FlaskForm):
    submit = SubmitField("Delete")


class CreateProfile(FlaskForm):
    name = StringField("name", validators=[DataRequired(), Length(min=1)])
    restriction = SelectField(
        "Restrictions",
        choices=[
            ("G", "G"), ("PG", "PG"), ("M", "M"),
            ("MA15+", "MA15+"), ("R18+", "R18+")],
        validators=[DataRequired()])
    submit = SubmitField("Create Profile")


class UpdateProfile(CreateProfile):
    submit = SubmitField("Update Profile")


class UnrecommendButton(FlaskForm):
    submit = SubmitField("Unrecommend")


class RemoveButton(FlaskForm):
    submit = SubmitField("Remove")


class CreateGroup(FlaskForm):
    name = StringField("name", validators=[DataRequired(), Length(min=1)])
    description = StringField("description")
    submit = SubmitField("Create Group")


class UpdateGroup(CreateGroup):
    submit = SubmitField("Update Group")


class JoinGroup(FlaskForm):
    submit = SubmitField("Join")


class UnjoinGroup(FlaskForm):
    submit = SubmitField("Unjoin")


class AddButton(FlaskForm):
    submit = SubmitField("Add to group")


class CreateContent(FlaskForm):
    title = StringField("title", validators=[DataRequired(), Length(min=1)])
    genre = StringField("genre", validators=[DataRequired()])
    year = IntegerField("year")
    submit = SubmitField("Add content")
