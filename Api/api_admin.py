# -*- coding: utf-8 -*-

from flask_restx import Api
from flask import Blueprint
from sqlalchemy.orm.exc import NoResultFound

# resources

from resources.admin.products import ProductApi, ProductSelect  # Products
from resources.admin.products_category import CategoryProductApi  # Category products
from resources.admin.products_brand import BrandProductApi  # Brands Product
from resources.admin.products_unit import UnitProductApi


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
