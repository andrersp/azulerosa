# -*- coding: utf-8 -*-

import os
import random
import string

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "Lb)vF~Ge+j$Gjy-)tkRT&:DEz6F*q8Qtm$m]VQ^u+ct69BY'cA*m`o}W-}s0^|B"
    PROPAGATE_EXCEPTIONS = True
    JWT_BLACKLIST_ENABLED = True
    ERROR_404_HELP = False
