# -*- coding: utf-8 -*-

from flask_restx import Api
from flask import Blueprint
from sqlalchemy.orm.exc import NoResultFound

# resources

from resources.admin.products import ProductApi


# Namespaces
# from resources.admin.products import product_space  # Products
# from resources.admin.products_category import category_space  # Categories Product
# from resources.admin.products_brand import brand_space  # Categories Product
# from resources.admin.products_unit import unit_space  # Units Product Space

# from resources.admin.provider import provider_space  # Providers

# from resources.admin.clients import client_space  # Clientes

# from resources.admin.purchase import ns_purchase  # Purchases

# from resources.admin.users import ns_user, ns_login, ns_logout  # Users

# from resources.admin.home import ns_home

# authorizations = {
#     'apikey': {
#         'type': 'apiKey',
#         'in': 'header',
#         'name': 'Bearer'
#     }
# }

# Set BluePrint
bp_admin = Blueprint(
    'api', __name__, static_folder='static', url_prefix="/api/v1/admin")

# Products

product_view = ProductApi.as_view("product_view")


bp_admin.add_url_rule(
    "/products/", defaults={"product_id": None}, view_func=product_view, methods=['GET', ])
bp_admin.add_url_rule("/products/", view_func=product_view, methods=['POST', ])
bp_admin.add_url_rule("/products/<int:product_id>",
                      view_func=product_view, methods=['GET', 'PUT', 'DELETE', ])
# # Inicilize Api
# api = Api(blueprint, version="1.0", title="Azul e Rosa Rest APi", contact={"email": "rsp.assistencia@gmail.com"},
#           description="Api for product register [http://swagger.io](http://swagger.io)", authorizations=authorizations)
# @api.errorhandler
# def default_error_handler(e):
#     return {"message": "An unhandled exception occurred"}, 500
# @api.errorhandler(NoResultFound)
# def database_not_found_error(e):
#     return {"message": "A database result was required but none was found"}, 404
# # Name Spaces APi
# # Product
# api.add_namespace(product_space, path="/product")
# # Products Category
# api.add_namespace(category_space, path="/product/category")
# # Products Brand
# api.add_namespace(brand_space, path="/product/brand")
# # Product Unit
# api.add_namespace(unit_space, path="/product/unit")
# # Provider
# api.add_namespace(provider_space, path="/provider")
# # Cliente
# api.add_namespace(client_space, path="/client")
# # purchases
# api.add_namespace(ns_purchase, path="/purchase")
# # Users
# api.add_namespace(ns_user, path="/user")
# # Login
# api.add_namespace(ns_login, path="/login")
# # Logout
# api.add_namespace(ns_logout, path="/logout")
# # Home
# api.add_namespace(ns_home, path="/home")
