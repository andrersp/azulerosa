# -*- coding: utf-8 -*-

from flask import request
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required

from wraps import required_params

from model.products import ModelProducts

product_space = Namespace("Products", description="Resources for Produtos")

schema = {
    "id": {"type": "numeric", "required": True, "description": "numeric value int or str"},
    "name": {"type": "string", "required": True, "empty": False, "description": "name of product"},
    "category": {"type": "integer", "required": True, "description": "integer value of category"},
    "brand": {"type": "integer", "required": True, "description": "integer valur of brand"},
    "minimum_stock": {"type": "float", "required": True, "description": "float value of minimum stock"},
    "maximum_stock": {"type": "float", "required": True, "description": "float value of maximum stock"},
    "long_description": {"type": "string", "required": True, "empty": True, "description": "Long Description of product"},
    "short_description": {"type": "string", "required": True, "empty": False, "description": "Short Description of product, max 200", "maxlength": 200},
    "sale_price": {"type": "float", "required": True, "description": "value of sale price of product"}
}


@product_space.route("")
class ProductsGet(Resource):
    # @jwt_required
    def get(self):
        """ Get all products enabled in Stock """
        return {"data": [product.list_product() for product in ModelProducts.query.all()]}

    @required_params(schema)
    @product_space.doc(params=schema)
    def post(self):
        """ Create or Update product.
        For create a new product send a empty string value or send a int id product value for update """

        data = request.json

        product = ModelProducts.find_product(data.get("id"))

        if product:
            return {"message": "update"}

        try:

            product = ModelProducts(**data)
            product.save_product()

            return {"message": "product created", "data": product.list_product()}, 201
        except Exception as err:
            print(err, "Erro")
            return {"message": "Internal error"}, 500

        return {"messa": "ok"}, 200
