# -*- coding: utf-8 -*-

from flask import request
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required

from model.products_category import ModelCategoryProduct

from wraps import required_params

category_space = Namespace(
    'Gerenciamento de categorias do produtos', description="Endpoints para gerenciamento de categorias dos produtos")

schema = {
    "id": {"type": "numeric", "required": True, "empty": True, "description": "String vazia ou Int com o ID da categoria"},
    "name": {"type": "string", "required": True, "empty": False, "description": "Nome da Categoria"},
    "description": {"type": "string", "required": True, "empty": True, "description": "Pequena descrição da categoria. Max 120 caracteres", "maxlength": 120}
}


@category_space.route("")
class CategoryProductView(Resource):

    @jwt_required
    def get(self):
        """ Lista de todos as categorias cadastradas.
        Retorna uma lista contendo todos as categorias"""

        return {"data": [data.list_category() for data in ModelCategoryProduct.query.all()]}, 200

    @category_space.doc(params=schema)
    @required_params(schema)
    @jwt_required
    def post(self):
        """ Adicionar ou editar categoria.
        Para criar envie string vazia em id e para editar envie um int com o ID da categoria"""

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

    @jwt_required
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

    @jwt_required
    def get(self, id_category):
        """ Seleciona categoria pelo ID.
        Retorna a categoria seleciona caso exista."""

        category = ModelCategoryProduct.find_category(id_category)

        if category:
            return {"data": category.list_category()}, 200

        return {"message": "Category not found"}, 404
