# -*- coding: utf-8

from flask import Flask, jsonify, Blueprint, redirect, url_for
from flask.cli import FlaskGroup
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

from restx import blueprint as api

from db import db


app = Flask(__name__)

app.config.from_object("config.Config")

# Register Bluprint
app.register_blueprint(api, url_prefix="/api/v1")

# BCrypt
bcrypt = Bcrypt(app)

# Data Base
db.init_app(app)

# Migrate
migrate = Migrate(app, db)


# jwt
jwt = JWTManager(app)


# Load profile jwt
@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {'roles': user.get("roles"), "endoints": ['%s' % rule for rule in app.url_map.iter_rules()]}

# Get User Id JWT
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.get("id")

# Message Expire Token
@jwt.expired_token_loader
def my_expire_token_callback(expire_token):
    token_type = expire_token['type']
    return jsonify({
        'status': 401,
        'sub_status': 42,
        'msg': 'Seu acesso expirou. Faça Login novamente!'
    }), 401


@jwt.unauthorized_loader
def error_load_token(fn):
    return jsonify({"message": "Erro na leitura do token"}), 401

# Message Error read Token in header
@jwt.invalid_token_loader
def erro_token(e):
    return jsonify({"message": "Erro na leitura do token"}), 422

# Error token revoked
@jwt.revoked_token_loader
def token_invalidado():
    return jsonify({"message": "Você não esta  logado. Faça login Novamente"}), 401


# Before first request
@app.before_first_request
def create_tables():
    db.create_all()


@app.route("/")
def hello():
    return redirect("/api/v1")

# Redirect for doc in 404
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"message": "URL not Found"}), 404


cli = FlaskGroup(app)

if __name__ == "__main__":
    cli()
