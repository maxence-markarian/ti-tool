import datetime
from typing import List
from uuid import uuid4, UUID

import bcrypt
from flask import Flask, render_template, url_for, flash, redirect
from flask_login import login_user, LoginManager, logout_user, login_required, current_user
from sqlalchemy import select

from titool.config import Config
from titool.email_reader import EmailItem, read_email, scrape_email
from titool.forms import RegistrationForm, LoginForm, AddToMyFavorites, ShareArticle
from titool.db import db, User, Article, Favorites, Shared
from titool.visitor import Visitor
from sqlalchemy.dialects.postgresql import insert

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
    if db_user is None:
        return None
    return Visitor(db_user.id, db_user.username)


@app.route("/")
@app.route("/home")
def home():
    favorites_form = AddToMyFavorites()
    shared_form = ShareArticle()
    articles = get_articles()
    users = get_all_users()
    shared_form.set_user_target(users)
    return render_template("home.html", articles=articles, users=users,
                           favorites_form=favorites_form, shared_form=shared_form)


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


@app.route("/profile")
def profile():
    articles_by_user = get_articles_by_user(current_user.user_id)
    shared_articles = get_shared_articles(current_user.user_id)
    # print(shared_articles)
    return render_template("profile.html", favorites=articles_by_user,
                           shared_articles=shared_articles, title="Profile")


@app.route("/addtomyfavorites", methods=["POST"])
@login_required
def add_to_my_favorites():
    form = AddToMyFavorites()
    if form.validate_on_submit():
        insert_into_favorites(current_user.user_id, UUID(form.article.data))
        flash("The article has been added!", "success")
    return redirect(url_for("home"))


@app.route("/sharearticle", methods=["POST"])
@login_required
def share_article():
    form = ShareArticle()
    form.set_user_target(get_all_users())
    if form.validate_on_submit() and form.user_target.data != "":
        insert_into_shared(current_user.user_id, UUID(form.user_target.data), UUID(form.article.data))
        flash("The article has been sent!", "success")
    return redirect(url_for("home"))


def insert_into_shared(user_id: UUID, user_id_target: UUID, article_id: UUID):
    insertion = insert(Shared).values(user_id_sender=user_id, user_id_target=user_id_target,
                                      article_id=article_id,
                                      creation_date=datetime.datetime.utcnow()).on_conflict_do_nothing()
    db.session.execute(insertion)
    db.session.commit()


def insert_into_favorites(user_id: UUID, article_id: UUID):
    insertion = insert(Favorites).values(user_id=user_id, article_id=article_id,
                creation_date=datetime.datetime.utcnow()).on_conflict_do_nothing()
    db.session.execute(insertion)
    db.session.commit()


def get_articles() -> List[Article]:
    articles = Article.query.all()
    return list(articles)


def get_articles_by_user(user_id: UUID) -> List[Article]:
    join_articles = db.session.query(Article).join(Favorites).filter(Article.id == Favorites.article_id)
    articles_by_user = join_articles.filter_by(user_id=user_id).all()
    return list(articles_by_user)


def get_shared_articles(user_id: UUID) -> List[Article]:
    join_articles = db.session.query(Article).join(Shared).filter(Article.id == Shared.article_id)
    shared_articles = join_articles.filter_by(user_id_target=user_id).all()
    return list(shared_articles)


def get_all_users() -> List[User]:
    users = User.query.all()
    return list(users)


def update_articles():
    emails = read_email(config.mail_username, config.mail_password)
    articles: List[EmailItem] = []
    for body in emails:
        email_items = scrape_email(body)
        for item in email_items:
            articles.append(item)
    insert_articles(articles)


def insert_articles(articles: List[EmailItem]):
    for article in articles:
        article_id = uuid4()
        # article = Article(id=article_id, title=article.title, url=article.url,
        #                  author=article.author, insertion_date=datetime.datetime.utcnow())
        insertion = insert(Article).values(id=article_id, title=article.title, url=article.url,
                    author=article.author, insertion_date=datetime.datetime.utcnow()).on_conflict_do_nothing()
        db.session.execute(insertion)
        db.session.commit()


def start():
    with app.app_context():
        update_articles()
    app.run(debug=True, use_reloader=False)


def sync_db():
    with app.app_context():
        db.drop_all()
        db.create_all()


if __name__ == "__main__":
    start()
