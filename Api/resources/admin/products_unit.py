# -*- coding: utf-8  -*-


from flask import request
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required

from model.products_unit import ModelProductUnit

from wraps import required_params


unit_space = Namespace("Gerenciamento de Unidades",
                       description="Endpoints para gerencimanto de unidades de medida")


schema = {
    "id": {"type": "numeric", "required": True, "empty": True, "description": "String vazia ou Int com o ID da categoria"},
    "name": {"type": "string", "required": True, "empty": False, "maxlength": 2, "description": "Nome da Categoria"},
    "description": {"type": "string", "required": True, "empty": True, "maxlength": 120, "description": "Pequena descrição da categoria. Max 120 caracteres", "maxlength": 120}
}


@unit_space.route("")
class UnitProduct(Resource):

    @jwt_required
    def get(self):
        """ LIsta de todas as unidades de medida cadastradas
        Retorna lista de unidades para ser usada no cadastro de produto. """

        units = [unit.json_units() for unit in ModelProductUnit.query.all()]

        return {"data": units}, 200

    @jwt_required
    @unit_space.doc(params=schema)
    @required_params(schema)
    def post(self):
        """ Adicionar ou editar Unidade.
        Para criar envie string vazia em id e para editar envie um int com o ID da unidade """

        data = request.json

        unit = ModelProductUnit.find_unit(data.get("id"))

        if unit:
            return self.put()

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
    @unit_space.hide
    @required_params(schema)
    def put(self):

        data = request.json

        unit = ModelProductUnit.find_unit_name(data.get("name"))

        if unit and unit.id_unit != int(data.get("id")):
            return {"message": "Duplicate name."}, 400

        try:

            unit.update_unit(**data)
            unit.save_unit()
            return {"message": "Unit updated", "data": unit.json_units()}, 200
        except:
            return {"message": "Internal error"}, 500


@unit_space.route("/<int:id_unit>")
class UnitProductGet(Resource):
    @jwt_required
    def get(self, id_unit):

        unit = ModelProductUnit.find_unit(id_unit)

        if unit:
            return {"data": unit.json_units()}, 200

        return {"message": "Unit not found"}, 400
