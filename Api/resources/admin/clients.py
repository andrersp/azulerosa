# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from wraps import required_params

from model.clients import ModelClient, ModelDelivereAdrressClient

from cerberus_validate import CustomValidator2


schema = {
    "enable": {"type": "boolean", "required": True},
    "type_registration": {"type": "integer", "allowed": [1, 2], "required": True, "description": "Tipo de registo. 1 : CPF, 2: CNPJ"},
    "cnpj": {"type": "string", "required": True, "check_with": "registration", "description": "CNPJ/CPF do cliente."},
    "state_registration": {"type": "string", "required": True, "description": "Inscrição Estadual caso CNPJ, RG Caso CPF", "maxlength": 20},
    "municipal_registration": {"type": "string", "required": True, "description": "Inscrição municipal caso CNPJ e 0 caso não exista ou CPF", "maxlength": 12},
    "fancy_name": {"type": "string", "required": True, "description": "Nome Fantasia Caso CNPJ. Vazio Caso CPF"},
    "company_name": {"type": "string", "required": True, "description": "Razão Social ou Nome completo", "empty": False},
    "contact_name": {"type": "string", "required": True, "description": "Nome do contato. Vazio caso CPF", "empty": True},
    "phone": {"type": "string", "required": True, "check_with": "phonecheck",  "description": "Número de telefone ou celular. É obrigatório ao menos 1 deles"},
    "cell_phone": {"type": "string", "required": True, "check_with": "cellcheck", "description": "Número de telefone ou celular. É obrigatório ao menos 1 deles"},
    "email": {"type": "string", "required": True, "description": "Email de contato. Máximo 50 caracteres", "empty": True, "maxlength": 50},
    "zip_code": {"type": "string", "required": True, "maxlength": 8, "minlength": 8, "empty": False, "description": "Cep do endereço principal", "regex": '[0-9]+'},
    "address": {"type": "string", "required": True, "description": "Nome da Rua/Avenida.", "empty": False, "maxlength": 80},
    "number": {"type": "string", "required": True, "description": "Número do endereço", "empty": True, "maxlength": 60},
    "complement": {"type": "string", "required": True, "description": "Complemente", "empty": True, "maxlength": 40},
    "neighborhood": {"type": "string", "required": True, "description": "Nome do Bairro", "empty": False, "maxlength": 80},
    "city": {"type": "string", "required": True, "description": "Cidade", "empty": False, "maxlength": 80},
    "state": {"type": "string", "required": True, "description": "Estado", "empty": False, "maxlength": 2},
    "delivery_address": {"type": "list", "required": True, "empty": False, "schema": {"type": "dict", "schema": {
        "zip_code": {"type": "string", "required": True, "maxlength": 8, "minlength": 8, "empty": False, "description": "Zip Code address", "regex": '[0-9]+'},
        "address": {"type": "string", "required": True, "description": "Company Address", "empty": False, "maxlength": 80},
        "number": {"type": "string", "required": True, "description": "Address number", "empty": True, "maxlength": 60},
        "complement": {"type": "string", "required": True, "description": "Address Complement", "empty": True, "maxlength": 40},
        "neighborhood": {"type": "string", "required": True, "description": "neighborhood name", "empty": False, "maxlength": 80},
        "city": {"type": "string", "required": True, "description": "Company city", "empty": False, "maxlength": 80},
        "state": {"type": "string", "required": True, "description": "Estado", "empty": False, "maxlength": 2},
        "current": {"type": "boolean", "required": True, "description": "Lista de dicionários para endereços de entrega. Pode ser cadastrado posteriormente"}
    }}},
    "obs": {"type": "string", "required": True, "description": "Observação caso houver.", "empty": True},
    "notify": {"type": "boolean", "required": True, "description": "Se cliente aceita ser notificado sob promoções."}

}


class ClientApi(MethodView):
    @jwt_required
    def get(self, client_id):
        """ Lista com todos os clientes cadastrados """

        if client_id:
            client = ModelClient.find_client(client_id)

            if client:
                return jsonify({"data": client.json_client()}), 200

            return jsonify({"message": "Client not found!"}), 404

        return jsonify({"data": [data.list_client() for data in ModelClient.query.all()]}), 200

    # @jwt_required

    def post(self):
        """ Adicionar ou editar cliente.
        Para criar envie string vazia em id e para editar envie um int com o ID do cliente
        """

        data = request.json if request.json else {}

        v = CustomValidator2(schema)

        if not v.validate(data):
            return jsonify({"message": v.errors}), 400

        # data = v.document

        return jsonify(data)

        # # Check if delivery_addres has one current selected
        # current = len([address.get("current") for address in data.get(
        #     "delivery_address", "{}") if address.get("current")])
        # if len(data.get("delivery_address")) > 1:
        #     if current != 1:
        #         return jsonify({"message": "Only one address current required"}), 400
        # else:
        #     data["delivery_address"][0]["current"] = True
        # # End check current address

        # try:
        #     client = ModelClient(**data)

        #     for address in data.get("delivery_address"):
        #         client.delivery_address.append(
        #             ModelDelivereAdrressClient(client=client, **address))

        #     client.save_client()

        #     return jsonify({"message": "Client created", "data": client.json_client()}), 201
        # except:

        #     return jsonify({"message": "Internal error"}), 500

    @jwt_required
    @required_params(schema)
    def put(self, client_id):

        data = request.json

        client = ModelClient.find_client(client_id)

        if not client:
            return jsonify({"message": "Client not found"}), 404

        if client:

            try:
                client.update_client(**data)
                client.save_client()
                return jsonify({"message": "client updated", "data": client.json_client()}), 200

            except:
                return jsonify({"message": "Internal Error"}), 500


schema = {
    "zip_code": {"type": "string", "required": True, "maxlength": 8, "minlength": 8, "empty": False, "description": "Zip Code address", "regex": '[0-9]+'},
    "address": {"type": "string", "required": True, "description": "Company Address", "empty": False, "maxlength": 80},
    "number": {"type": "string", "required": True, "description": "Address number", "empty": True, "maxlength": 60},
    "complement": {"type": "string", "required": True, "description": "Address Complement", "empty": True, "maxlength": 40},
    "neighborhood": {"type": "string", "required": True, "description": "neighborhood name", "empty": False, "maxlength": 80},
    "city": {"type": "string", "required": True, "description": "Company city", "empty": False, "maxlength": 80},
    "state": {"type": "string", "required": True, "description": "Company State", "empty": False, "maxlength": 2},
    "current": {"type": "boolean", "required": True}

}


class ClientAddressApi(MethodView):
    @jwt_required
    def delete(self, client_id, address_id):
        """ Deletar endereço de entrega cadastrado. """

        address = ModelDelivereAdrressClient.query.filter_by(
            id=address_id).filter_by(client=client_id).first()

        if address:
            try:
                address.delete_address()
                return jsonify({"message": "address deleted"}), 200
            except:
                return jsonify({"message": "Internal error"}), 500

        return jsonify({"message": "Address not found"}), 404

    @jwt_required
    @required_params(schema)
    def put(self, client_id, address_id):
        """ Atualiza endereço de entrega cadastrador"""

        data = request.json

        address = ModelDelivereAdrressClient.query.filter_by(
            id=address_id).filter_by(client=client_id).first()

        if address:

            try:
                address.update_address(**data)
                address.save_address()

                return jsonify({"message": "address updated", "data": address.list_address()}), 200
            except:

                return jsonify({"message": "Internal error"}), 500

        return jsonify({"message": "Address not found"}), 404

    @jwt_required
    def patch(self, client_id, address_id):
        """ Seleciona o endereço de entrega como padrão """

        client = ModelClient.find_client(client_id)

        if not client:
            return jsonify({"message": "client not found"}), 404

        address = ModelDelivereAdrressClient.query.filter_by(
            id=address_id).filter_by(client=client_id).first()

        if not address:
            return jsonify({"message": "address not found"}), 404

        address = [address.list_address()
                   for address in client.delivery_address]

        for new in address:
            address = ModelDelivereAdrressClient.find_address(new.get("id"))
            address.current = False
            address.save_address()

        try:
            address.current = True
            address.save_address()

            return jsonify({"message": "address updated to current", "data": address.list_address()}), 200
        except:

            return jsonify({"message": "internal error"}), 500

    @jwt_required
    def post(self, client_id):
        """ Adiciona endereço de entrega """

        data = request.json

        client = ModelClient.find_client(client_id)

        if not client:
            return jsonify({"message": "Client not found"}), 400

        address = [address.list_address()
                   for address in client.delivery_address]

        if not address:
            data["current"] = True
        else:
            if data.get("current"):
                for new in address:
                    address = ModelDelivereAdrressClient.find_address(
                        new.get("id"))
                    address.current = False
                    address.save_address()

        try:
            address = ModelDelivereAdrressClient(**data, client=client_id)
            address.save_address()

            return jsonify({"message": "address created", "data": address.list_address()}), 201
        except:
            return jsonify({"message": "internal error"}), 200
