from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    username = db.Column(db.String(18), unique=True, nullable=False)
    password = db.Column(db.LargeBinary, nullable=False)

    def __repr__(self):
        return f"User('{self.id}', '{self.username}')"


class Article(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    author = db.Column(db.String(150), nullable=False)
    url = db.Column(db.String(1000), unique=True, nullable=False)
    insertion_date = db.Column(db.DateTime(timezone=True), nullable=False)

    def __repr__(self):
        return f"Article('{self.id}', '{self.title}', '{self.url}')"


class Favorites(db.Model):
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("user.id"))
    article_id = db.Column(UUID(as_uuid=True), db.ForeignKey("article.id"))
    creation_date = db.Column(db.DateTime(timezone=True), nullable=False)
    __table_args__ = (db.PrimaryKeyConstraint("user_id", "article_id"),)
