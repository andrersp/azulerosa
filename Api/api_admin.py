# -*- coding: utf-8 -*-

from flask_restx import Api
from flask import Blueprint
from sqlalchemy.orm.exc import NoResultFound


# Namespaces
from resources.admin.products import product_space  # Products
from resources.admin.products_category import category_space  # Categories Product

from resources.admin.provider import provider_space  # Providers

from resources.admin.clients import client_space # Clientes

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Bearer'
    }
}

# Set BluePrint
blueprint = Blueprint(
    'api', __name__, static_folder='static')




# Inicilize Api
api = Api(blueprint, version="1.0", title="Azul e Rosa Rest APi",
          description="Api for product register", authorizations=authorizations)
        

@api.errorhandler
def default_error_handler(e):
    return {"message": "An unhandled exception occurred"}, 500


@api.errorhandler(NoResultFound)
def database_not_found_error(e):
    return {"message": "A database result was required but none was found"}, 404


# Name Spaces APi
api.add_namespace(product_space, path="/product")  # Product
# Products Category
api.add_namespace(category_space, path="/product/category")

# Provider
api.add_namespace(provider_space, path="/provider")

# Cliente
api.add_namespace(client_space, path="/client")