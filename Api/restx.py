# -*- coding: utf-8 -*-

from flask_restx import Api
from flask import Blueprint
from sqlalchemy.orm.exc import NoResultFound


# Namespaces
from resources.products import product_space  # Products
from resources.products_category import category_space  # Categories Product

from resources.provider import provider_space  # Providers

from resources.clients import client_space # Clientes

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Bearer'
    }
}

# Set BluePrint
admin = Blueprint(
    'api', __name__, url_prefix="/api/v1/admin", static_folder='static')

front = Blueprint(
    'front', __name__, url_prefix="/api/v1/", static_folder='static')



# Inicilize Api
api = Api(admin, version="1.0", title="Azul e Rosa Rest APi",
          description="Api for product register", authorizations=authorizations)
        
api_front = Api(front, version="1.0", title="Azul e Rosa Rest APi",
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
