# -*- coding: utf-8 -*-

from flask import request
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required

from wraps import required_params

from model.products import ModelProducts

product_space = Namespace("Products", description="Resources for Produtos")

schema = {
    "id": {"type": "numeric", "required": True, "description": "numeric value int or str"},
    "name": {"type": "string", "required": True, "description": "name of product"}
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

        return {"messa": "ok"}, 200
