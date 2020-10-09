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

    __mapper_args__ = {
        "order_by": id_user
    }

    def __repr__(self):
        return "<User %r>" % self.username

    def __init__(self, id, username, password, enable):
        self.id = id,
        self.username = username
        self.password = password
        self.enable = enable

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
            print("errr")
            raise

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

        username = cls.query.filter_by(username=username).first()

        if username:
            return username

        return False

    def generate_hash(self):
        self.password = generate_password_hash(self.password).decode("utf8")

    def check_password(self, password):
        return check_password_hash(self.password, password)
