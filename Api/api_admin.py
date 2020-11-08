# -*- coding: utf-8 -*-

from flask_restx import Api
from flask import Blueprint
from sqlalchemy.orm.exc import NoResultFound

# resources
from resources.admin.home import HomeApi  # Home
from resources.admin.products import ProductApi, ProductSelect  # Products
from resources.admin.products_category import CategoryProductApi  # Category products
from resources.admin.products_brand import BrandProductApi  # Brands Product
from resources.admin.products_unit import UnitProductApi  # unit Products
from resources.admin.provider import ProviderApi  # Provider
from resources.admin.users import UsersApi, LoginApi, LogoutApi  # user and login


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

# Home
home_view = HomeApi.as_view("home_view")
bp_admin.add_url_rule("/", view_func=home_view, methods=['GET', ])


# Category Products
category_product_view = CategoryProductApi.as_view("category_product_view")
bp_admin.add_url_rule("/products/categories/", defaults={"category_id": None},
                      view_func=category_product_view,
                      methods=['GET', ])
bp_admin.add_url_rule("/products/categories/",
                      view_func=category_product_view, methods=['POST', ])
bp_admin.add_url_rule("/products/categories/<int:category_id>",
                      view_func=category_product_view,
                      methods=['GET', 'PUT', 'DELETE'])

# Brands Product
brand_product_view = BrandProductApi.as_view("brand_product_view")
bp_admin.add_url_rule(
    "/products/brands/", defaults={"brand_id": None},
    view_func=brand_product_view, methods=['GET', ])
bp_admin.add_url_rule("/products/brands/",
                      view_func=brand_product_view, methods=['POST'])
bp_admin.add_url_rule("/products/brands/<int:brand_id>",
                      view_func=brand_product_view,
                      methods=['GET', 'PUT', 'DELETE'])


# Unit Product
unit_product_view = UnitProductApi.as_view("unit_product_view")
bp_admin.add_url_rule("/products/units/",
                      defaults={"unit_id": None},
                      view_func=unit_product_view, methods=['GET', ])
bp_admin.add_url_rule("/products/units/",
                      view_func=unit_product_view, methods=['POST', ])
bp_admin.add_url_rule("/products/units/<int:unit_id>",
                      view_func=unit_product_view, methods=['GET', 'PUT'])

# Providers
provider_view = ProviderApi.as_view("provider_view")

bp_admin.add_url_rule("/providers/", defaults={"provider_id": None},
                      view_func=provider_view, methods=['GET', ])
bp_admin.add_url_rule(
    "/providers/", view_func=provider_view, methods=['POST', ])
bp_admin.add_url_rule("/providers/<int:provider_id>", view_func=provider_view,
                      methods=['GET', 'PUT', ])

# Products endpoints
product_view = ProductApi.as_view("product_view")
product_selects_view = ProductSelect.as_view("product_selects")

bp_admin.add_url_rule(
    "/products/", defaults={"product_id": None}, view_func=product_view, methods=['GET', ])
bp_admin.add_url_rule("/products/", view_func=product_view, methods=['POST', ])
bp_admin.add_url_rule("/products/<int:product_id>",
                      view_func=product_view, methods=['GET', 'PUT', 'DELETE', ])
bp_admin.add_url_rule("/products/image/<int:image_id>",
                      view_func=product_view, methods=['DELETE', ])
bp_admin.add_url_rule("/products/selects/",
                      view_func=product_selects_view, methods=['GET'])


# user
user_view = UsersApi.as_view("user_view")
bp_admin.add_url_rule("/users/", defaults={"user_id": None},
                      view_func=user_view, methods=['GET', ])
bp_admin.add_url_rule("/users/", view_func=user_view, methods=['POST', ])
bp_admin.add_url_rule("/users/<int:user_id>", view_func=user_view,
                      methods=['GET', 'PUT'])

# Login
login_view = LoginApi.as_view("login_api")
bp_admin.add_url_rule("/login/", view_func=login_view, methods=['POST', ])

# Logout
logout_view = LogoutApi.as_view("logout_view")
bp_admin.add_url_rule("/logout/", view_func=logout_view, methods=['POST', ])
