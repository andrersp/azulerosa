# -*- coding: utf-8 -*-

from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from model.products_brand import ModelBrandProduct
from cerberus_validate import CustomValidator


schema = {
    "name": {"type": "string", "required": True, "empty": False, "description": "Nome da Categoria"},
    "description": {"type": "string", "required": True, "empty": True, "description": "Pequena descrição da categoria. Max 120 caracteres", "maxlength": 120}
}


class BrandProductApi(MethodView):

    @jwt_required
    def get(self, brand_id):
        """ Lista de todos as marcas cadastradas.
        Retorna uma lista contendo todos as marcas """

        if brand_id:
            brand = ModelBrandProduct.find_brand(brand_id)

            if brand:
                return jsonify({"data": brand.list_brand()}), 200

            return jsonify({"message": "Brand not found"}), 404

        return jsonify({"data": [data.list_brand() for data in ModelBrandProduct.query.all()]}), 200

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

            brand = ModelBrandProduct(**data)
            brand.save_brand()

            return jsonify({"message": "brand saved", "data": brand.list_brand()}), 201

        except:
            return jsonify({"message": "Internal error"}), 500

    @jwt_required
    def put(self, brand_id):

        data = request.json if request.json else{}

        v = CustomValidator(schema)

        if not v.validate(data):
            return jsonify({"message": v.errors}), 400

        data = v.document

        brand = ModelBrandProduct.find_brand(brand_id)

        if brand:
            try:

                brand.update_brand(**data)
                brand.save_brand()

                return jsonify({"messahe": "Cateory updated", "data": brand.list_brand()}), 200

            except:

                return jsonify({"message": "Internal error"}), 500
        return jsonify({"messahe": "Brand not found"}), 404
