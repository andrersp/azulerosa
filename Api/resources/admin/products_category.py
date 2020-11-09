# -*- coding: utf-8 -*-

from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from model.products_category import ModelCategoryProduct
from cerberus_validate import CustomValidator


schema = {
    "name": {"type": "string", "required": True, "empty": False, "description": "Nome da Categoria"},
    "description": {"type": "string", "required": True, "empty": True, "description": "Pequena descrição da categoria. Max 120 caracteres", "maxlength": 120}
}


class CategoryProductApi(MethodView):

    @jwt_required
    def get(self, category_id):
        """ Lista de todos as categorias cadastradas.
        Retorna uma lista contendo todos as categorias"""

        if category_id:
            category = ModelCategoryProduct.find_category(category_id)

            if category:
                return jsonify({"data": category.list_category()}), 200

            return jsonify({"message": "Category not found"}), 404

        return {"data": [data.list_category() for data in ModelCategoryProduct.query.all()]}, 200

    @jwt_required
    def post(self):
        """ Adicionar ou editar categoria.
        Para criar envie string vazia em id e para editar envie um int com o ID da categoria"""

        data = request.json if request.json else{}

        v = CustomValidator(schema)

        if not v.validate(data):
            return jsonify({"message": v.errors}), 400

        data = v.document

        try:
            category = ModelCategoryProduct(**data)
            category.save_category()

            return jsonify({"message": "category saved", "data": category.list_category()}), 201

        except:
            return jsonify({"message": "Internal error"}), 500

    @jwt_required
    def put(self, category_id):

        data = request.json if request.json else{}

        v = CustomValidator(schema)

        if not v.validate(data):
            return jsonify({"message": v.errors}), 400

        data = v.document
        category = ModelCategoryProduct.find_category(category_id)

        if category:
            try:
                category.update_category(**data)
                category.save_category()
                return jsonify({"messahe": "cateory updated", "data": category.list_category()}), 200
            except:
                return jsonify({"message": "Internal error"}), 500

        return jsonify({"message": "Category not found"}), 404
