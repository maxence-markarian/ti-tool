from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    username = db.Column(db.String(18), unique=True, nullable=False)
    password = db.Column(db.LargeBinary, nullable=False)

    def __repr__(self):
        return f"User('{self.username}')"

# class Message(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     content = db.Column(db.Text, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#
#     def __repr__(self):
#         return f"Message('{self.date_posted}')"