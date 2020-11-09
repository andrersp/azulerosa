# -*- coding: utf-8  -*-


from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from model.products_unit import ModelProductUnit
from cerberus_validate import CustomValidator


schema = {
    "name": {"type": "string", "required": True, "empty": False, "maxlength": 2, "description": "Nome da Categoria"},
    "description": {"type": "string", "required": True, "empty": True, "maxlength": 120, "description": "Pequena descrição da categoria. Max 120 caracteres", "maxlength": 120}
}


class UnitProductApi(MethodView):

    @jwt_required
    def get(self, unit_id):
        """ LIsta de todas as unidades de medida cadastradas
        Retorna lista de unidades para ser usada no cadastro de produto. """

        if unit_id:
            unit = ModelProductUnit.find_unit(unit_id)

            if unit:
                return jsonify({"data": unit.json_units()}), 200

            return jsonify({"message": "Unit not found"}), 404

        units = [unit.json_units() for unit in ModelProductUnit.query.all()]

        return jsonify({"data": units}), 200

    @jwt_required
    def post(self):
        """ Adicionar ou editar Unidade.
        Para criar envie string vazia em id e para editar envie um int com o ID da unidade """

        data = request.json if request.json else{}

        v = CustomValidator(schema)

        if not v.validate(data):
            return jsonify({"message": v.errors}), 400

        data = v.document

        unit_name = ModelProductUnit.find_unit_name(data.get("name"))

        if unit_name:
            return {"message": "Duplicate name."}, 400

        try:

            unit = ModelProductUnit(**data)
            unit.save_unit()

            return {"message": "Unit saved", "data": unit.json_units()}, 201

        except:
            return {"message": "Internal error"}, 500

    @jwt_required
    def put(self, unit_id):

        data = request.json if request.json else{}

        v = CustomValidator(schema)

        if not v.validate(data):
            return jsonify({"message": v.errors}), 400

        data = v.document

        unit = ModelProductUnit.find_unit(unit_id)

        if not unit:
            return jsonify({"message": "Unit not found"}), 404

        unit_name = ModelProductUnit.find_unit_name(data.get("name"))

        if unit_name:
            if len(unit_name) > 1 or unit_name[0] != unit_id:
                return {"message": "Duplicate name."}, 400

        try:

            unit.update_unit(**data)
            unit.save_unit()
            return {"message": "Unit updated", "data": unit.json_units()}, 200
        except:
            return {"message": "Internal error"}, 500
