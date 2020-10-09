# -*- coding: utf-8 -*-

import os

# SQLALCHEMY_DATABASE_URI = "postgresql://andre:rsp@127.0.0.1/dhpp"  # local
# SQLALCHEMY_TRACK_MODIFICATIONS = False


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    # SQLALCHEMY_DATABASE_URI = "postgresql://andre:rsp@127.0.0.1/loja2"  # local
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "passwordkeysecret"
    PROPAGATE_EXCEPTIONS = True
    JWT_BLACKLIST_ENABLED = True
    ERROR_404_HELP = False
