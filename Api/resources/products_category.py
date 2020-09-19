# -*- coding: utf-8 -*-

from flask import request
from flask_restx import Resource, Namespace

from model.products_category import ModelCategoryProduct

from wraps import required_params

category_space = Namespace(
    'Products Category', description="Resources for product category")

schema = {
    "id": {"type": "numeric", "required": True, "empty": True, "description": "numeric string value or int"},
    "name": {"type": "string", "required": True, "empty": False, "description": "Name of category"},
    "description": {"type": "string", "required": True, "empty": True, "description": "Short Description of category"}
}


@category_space.route("")
class CategoryProductView(Resource):

    def get(self):
        """ Get All Products Category """

        return {"data": [data.list_category() for data in ModelCategoryProduct.query.all()]}, 200

    @category_space.doc(params=schema)
    @required_params(schema)
    def post(self):
        """ Create of update a product category """

        data = request.json

        category = ModelCategoryProduct.find_category(data.get("id"))

        if category:
            return self.put()

        try:

            category = ModelCategoryProduct(**data)
            category.save_category()

            return {"message": "category saved", "data": category.list_category()}, 201

        except:
            return {"message": "Internal error"}, 500

    @category_space.hide
    @required_params(schema)
    def put(self):

        data = request.json

        category = ModelCategoryProduct.find_category(data.get("id"))

        if category:
            try:

                category.update_category(**data)
                category.save_category()

                return {"messahe": "cateory updated", "data": category.list_category()}, 200

            except:

                return {"message": "Internal error"}


@category_space.route("/<int:id_category>")
class CategoryGet(Resource):

    def get(self, id_category):
        """ Get Category By Id """

        category = ModelCategoryProduct.find_category(id_category)

        if category:
            return {"data": category.list_category()}, 200

        return {"message": "Category not found"}, 404

