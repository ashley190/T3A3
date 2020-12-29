from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, PasswordField
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


class UpdateUserForm(FlaskForm):
    email = StringField('email')
    subscription_status = BooleanField('Subscribe')
    submit = SubmitField("Update Details")


class DeleteButton(FlaskForm):
    submit = SubmitField("Delete Account")
