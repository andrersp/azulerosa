# -*- coding: utf-8

from flask import Flask, jsonify, Blueprint, redirect
from flask.cli import FlaskGroup
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

from db import db

# Namespaces
from resources.products import product_space  # Products
from resources.products_category import category_space  # Categories Product


app = Flask(__name__)

app.config.from_object("config.Config")

# Set BluePrint
blueprint = Blueprint(
    'api', __name__, url_prefix="/api/v1", static_folder='static')


authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Bearer'
    }
}

# Inicilize Api
api = Api(blueprint, version="1.0", title="Azul e Rosa Rest APi",
          description="Api for product register", doc="/doc", authorizations=authorizations)


# Name Spaces APi
api.add_namespace(product_space, path="/product")  # Product
api.add_namespace(category_space, path="/category")  # Products Category

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


# BCrypt
bcrypt = Bcrypt(app)

# Data Base
db.init_app(app)

# Migrate
migrate = Migrate(app, db)

# Register Bluprint
app.register_blueprint(blueprint)


# Before first request
@app.before_first_request
def create_tables():
    print("Criando tabelas")


@app.route("/")
def hello():
    return redirect("/api/v1/doc")

# Redirect for doc in 404
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"message": "URL not Found"}), 404


cli = FlaskGroup(app)

if __name__ == "__main__":
    cli()
