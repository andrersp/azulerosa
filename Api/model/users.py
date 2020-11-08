# -*- coding: utf-8 -*-

from db import db
from sqlalchemy.exc import SQLAlchemyError

from flask_bcrypt import generate_password_hash, check_password_hash


class ModelsUser(db.Model):
    __tablename__ = 'users'
    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    enable = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "<User %r>" % self.username

    def list_users(self):
        return {
            "id": self.id_user,
            "username": self.username,
            "password": self.password,
            "enable": self.enable
        }

    def save_user(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()

    @classmethod
    def find_user(cls, id_user):
        if not id_user:
            return None

        user = cls.query.get(id_user)

        if user:
            return user

        return None

    @classmethod
    def find_username(cls, username):

        if not username:
            return False

        username = cls.query.filter_by(username=username).all()

        usernames = [data.id_user for data in username]

        if username:
            return usernames

        return False

    @classmethod
    def user_login(cls, username):
        if not username:
            return None

        user = cls.query.filter_by(username=username).first()

        if user:
            return user
        return None

    def update_user(self, username, password, enable):
        self.username = username
        self.password = password
        self.enable = enable

    def generate_hash(self):
        self.password = generate_password_hash(self.password).decode("utf8")

    def check_password(self, password):
        return check_password_hash(self.password, password)


@db.event.listens_for(ModelsUser.__table__, "after_create")
def initial_user(*args, **kwargs):
    user = ModelsUser(1, "admin", "admin", True)
    user.generate_hash()
    db.session.add(user)
    db.session.commit()
