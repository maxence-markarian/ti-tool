from typing import List

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, HiddenField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo

from titool.db import User


class RegistrationForm(FlaskForm):
    username = StringField("Username",
                           validators=[DataRequired(), Length(min=3, max=18)])
    password = PasswordField("Password",
                             validators=[DataRequired()])
    confirm_password = PasswordField("Confirm password",
                                     validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign up")


class LoginForm(FlaskForm):
    username = StringField("Username",
                           validators=[DataRequired(), Length(min=3, max=18)])
    password = PasswordField("Password",
                             validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")


class AddToMyFavorites(FlaskForm):
    article = HiddenField("Article")
    submit = SubmitField("Add")


class ShareArticle(FlaskForm):
    article = HiddenField("Article")
    user_target = SelectField("Target", coerce=str)
    submit = SubmitField("Share")

    def set_user_target(self, list_users: List[User]):
        choices = []
        for user in list_users:
            choices.append((user.id, user.username))
        self.user_target.choices = choices


class DeleteFromMyFavorites(FlaskForm):
    article = HiddenField("Article")
    submit = SubmitField("Delete")


class DeleteFromMyShared(FlaskForm):
    article = HiddenField("Article")
    submit = SubmitField("Delete")
