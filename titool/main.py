from uuid import uuid4, UUID

import bcrypt
import flask_login
from flask import Flask, render_template, url_for, flash, redirect
from flask_login import login_user, LoginManager, logout_user
from sqlalchemy import select

from titool.config import Config
from titool.forms import RegistrationForm, LoginForm
from titool.db import db, User
import titool.email_reader
from titool.visitor import Visitor

config = Config()

app = Flask(__name__)

app.config["SECRET_KEY"] = config.secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = config.database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = "False"

login_manager = LoginManager()
login_manager.init_app(app)

db.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    if user_id is None:
        return None
    query = select(User).where(User.id == UUID(user_id))
    db_user: User = db.session.execute(query).scalars().one_or_none()
    return Visitor(db_user.id, db_user.username)


posts = [
    {
        "author": "dummy1",
        "title": "title1"
    },
    {
        "author": "dummy2",
        "title": "title2"
    }
]


@app.route("/")
@app.route("/home")
def home():
    # print(flask_login.current_user)
    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        password_bytes = form.password.data.encode("UTF-8")
        password_hash = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        user_id = uuid4()
        user = User(id=user_id, username=form.username.data, password=password_hash)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("home"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        query = select(User).where(User.username == form.username.data)
        db_user: User = db.session.execute(query).scalars().one_or_none()
        if db_user is None:
            flash("Login unsuccessful. Unknown username", "danger")
            return render_template("login.html", title="Login", form=form)
        password_bytes = form.password.data.encode("UTF-8")
        if not bcrypt.checkpw(password_bytes, db_user.password):
            flash("Login unsuccesful. Wrong password", "danger")
            return render_template("login.html", title="Login", form=form)
        visitor = Visitor(db_user.id, db_user.username)
        login_user(visitor, remember=form.remember.data)
        flash("You have been logged in!", "success")
        return redirect(url_for("home"))
    return render_template("login.html", title="Login", form=form)


@app.route("/logout", methods=["POST"])
def logout():
    logout_user()
    flash("You have been logged out!", "success")
    return redirect(url_for("home"))


def start():
    titool.email_reader.test_scrape_email(titool.email_reader.read_email(config.mail_username, config.mail_password))
    app.run(debug=True, use_reloader=False)


def sync_db():
    db.init_app(app)
    app.app_context().push()
    db.drop_all()
    db.create_all()


if __name__ == "__main__":
    start()
