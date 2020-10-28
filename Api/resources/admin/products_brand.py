# -*- coding: utf-8 -*-

from flask import request
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required

from model.products_brand import ModelBrandProduct

from wraps import required_params

brand_space = Namespace(
    'Gerenciamento de Marcas dos produtos', description="Endpoints para gerenciamento de marcas dos produtos")

schema = {
    "id": {"type": "numeric", "required": True, "empty": True, "description": "String vazia ou Int com o ID da categoria"},
    "name": {"type": "string", "required": True, "empty": False, "description": "Nome da Categoria"},
    "description": {"type": "string", "required": True, "empty": True, "description": "Pequena descrição da categoria. Max 120 caracteres", "maxlength": 120}
}


@brand_space.route("")
class brandProductView(Resource):

    def get(self):
        """ Lista de todos as marcas cadastradas.
        Retorna uma lista contendo todos as marcas"""

        return {"data": [data.list_brand() for data in ModelBrandProduct.query.all()]}, 200

    @brand_space.doc(params=schema)
    @required_params(schema)
    # @jwt_required
    def post(self):
        """ Adicionar ou editar categoria.
        Para criar envie string vazia em id e para editar envie um int com o ID da categoria"""

        data = request.json

        brand = ModelBrandProduct.find_brand(data.get("id"))

        if brand:
            return self.put()

        try:

            brand = ModelBrandProduct(**data)
            brand.save_brand()

            return {"message": "brand saved", "data": brand.list_brand()}, 201

        except:
            return {"message": "Internal error"}, 500

    # @jwt_required
    @brand_space.hide
    @required_params(schema)
    def put(self):

        data = request.json

        brand = ModelBrandProduct.find_brand(data.get("id"))

        if brand:
            try:

                brand.update_brand(**data)
                brand.save_brand()

                return {"messahe": "cateory updated", "data": brand.list_brand()}, 200

            except:

                return {"message": "Internal error"}


@brand_space.route("/<int:id_brand>")
class brandGet(Resource):

    def get(self, id_brand):
        """ Seleciona categoria pelo ID.
        Retorna a categoria seleciona caso exista."""

        brand = ModelBrandProduct.find_brand(id_brand)

        if brand:
            return {"data": brand.list_brand()}, 200

        return {"message": "brand not found"}, 404
