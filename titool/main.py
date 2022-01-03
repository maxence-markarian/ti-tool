from flask import Flask, render_template, url_for, flash, redirect
from titool.config import Config
from titool.forms import RegistrationForm, LoginForm
from titool.db import db
import titool.email_reader

config = Config()

app = Flask(__name__)

app.config["SECRET_KEY"] = config.secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = config.database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = "False"


db.init_app(app)


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
    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("home"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == "admin" and form.password.data == "password":
            flash("You have been logged in!", "success")
            return redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check username and password", "danger")
    return render_template("login.html", title="Login", form=form)


def start():
    titool.email_reader.test_scrape_email(titool.email_reader.read_email(config.mail_username, config.mail_password))
    app.run(debug=True, use_reloader=False)


def sync_db():
    db.drop_all()
    db.create_all()


if __name__ == "__main__":
    start()
