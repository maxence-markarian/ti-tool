from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField("Username",
                           validators=[DataRequired(), Length(min=3, max=18)])
    password = PasswordField("Password",
                             validators=[DataRequired()])
    confirm_password = PasswordField("Confirm password",
                                     validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    username = StringField("Username",
                           validators=[DataRequired(), Length(min=3, max=18)])
    password = PasswordField("Password",
                             validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")
