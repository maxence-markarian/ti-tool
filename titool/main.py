from flask import Flask, render_template, url_for, flash, redirect
from titool.config import Config
from titool.forms import RegistrationForm, LoginForm
import titool.email_reader


app = Flask(__name__)


app.config["SECRET_KEY"] = "BU~!jmZS.:xH^z!1"


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
    config = Config()
    titool.email_reader.test_scrape_email(titool.email_reader.read_email(config.mail_username, config.mail_password))
    app.run(debug=True, use_reloader=False)


if __name__ == "__main__":
    start()
