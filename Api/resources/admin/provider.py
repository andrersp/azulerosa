# -*- coding: utf-8 -*-

from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from wraps import required_params

from model.provider import ModelProvider


schema = {
    "enable": {"type": "boolean", "required": True, "description": "Status of provider"},
    "type_registration": {"type": "integer", "allowed": [1, 2], "required": True, "description": "Type of provider registration. 1 : CPF, 2: CNPJ"},
    "cnpj": {"type": "string", "required": True, "check_with": "registration"},
    "state_registration": {"type": "string", "required": True, "description": "State company registration", "maxlength": 20},
    "municipal_registration": {"type": "string", "required": True, "description": "municipal company registration", "maxlength": 12},
    "fancy_name": {"type": "string", "required": True, "description": "company fancy name"},
    "company_name": {"type": "string", "required": True, "description": "Company name", "empty": False},
    "contact_name": {"type": "string", "required": True, "description": "Company contact name", "empty": True},
    "phone": {"type": "string", "required": True, "check_with": "phonecheck",  "description": "Phone Number of company"},
    "cell_phone": {"type": "string", "required": True, "check_with": "cellcheck", "description": "Cell Number of company"},
    "email": {"type": "string", "required": True, "description": "Contact email", "empty": True, "maxlength": 40},
    "site": {"type": "string", "required": True, "description": "Company site", "empty": True, "maxlength": 50},
    "zip_code": {"type": "string", "required": True, "maxlength": 8, "minlength": 8, "empty": False, "description": "Zip Code address", "regex": '[0-9]+'},
    "address": {"type": "string", "required": True, "description": "Company Address", "empty": False, "maxlength": 80},
    "number": {"type": "string", "required": True, "description": "Address number", "empty": True, "maxlength": 60},
    "complement": {"type": "string", "required": True, "description": "Address Complement", "empty": True, "maxlength": 40},
    "neighborhood": {"type": "string", "required": True, "description": "neighborhood name", "empty": False, "maxlength": 80},
    "city": {"type": "string", "required": True, "description": "Company city", "empty": False, "maxlength": 80},
    "state": {"type": "string", "required": True, "description": "Company State", "empty": False, "maxlength": 2},
    "obs": {"type": "string", "required": True, "description": "Company Observation", "empty": True}
}


# @provider_space.route("")
class ProviderApi(MethodView):

    def get(self, provider_id):
        """ List of all Provider """

        if provider_id:
            provider = ModelProvider.find_provider(provider_id)

            if provider:
                return jsonify({"data": provider.json_provider()}), 200

            return jsonify({"message": "Provider not found"}), 404

        return jsonify({"data": [data.list_provider() for data in ModelProvider.query.all()]}), 200

    # @jwt_required
    @required_params(schema)
    def post(self):
        """  Create or Updated provider """

        data = request.json

        try:
            provider = ModelProvider(**data)
            provider.save_provider()

            return jsonify({"message": "provided created", "data": provider.json_provider()}), 201
        except Exception as err:
            print(err)
            return jsonify({"message": "Internal error"}), 500

    @required_params(schema)
    def put(self, provider_id):

        data = request.json

        provider = ModelProvider.find_provider(provider_id)

        if not provider:
            return jsonify({"message": "Provider not found"}), 404

        if provider:
            try:
                provider.update_provider(**data)
                provider.save_provider()
                return jsonify({"message": "provider updated", "data": provider.json_provider()}), 200
            except:
                return jsonify({"message": "Internal Error"}), 500
