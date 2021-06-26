from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    psw = db.Column(db.String(500), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    pr = db.relationship('Profiles', backref='users', uselist=False)

    def set_password(self, password):
        self.psw = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.psw, password)

    def repr(self):
        return f"<users {self.id}>"


class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    old = db.Column(db.Integer)
    city = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def repr(self):
        return f"<profiles {self.id}>"


class NewPost(db.Model):
    name = db.Column(db.String(50), nullable=True)
    text = db.Column(db.String(5000), nullable=True)
    id_post = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.String(100), nullable=True)

    def __init__(self, name, text, photo):
        self.name = name
        self.text = text
        self.photo = photo

    def __repr__(self):
        return f"profile {self.name}>"




@login.user_loader
def load_user(id):
    return Users.query.get(int(id))