# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

from flask import request
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required

from wraps import required_params

from model.clients import ModelClient, ModelDelivereAdrressClient

client_space = Namespace("Gerenciamento de clientes",
                         description="Endpoints para gerenciamento de clientes")

schema = {
    "id": {"type": "numeric", "required": True, "description": "String vazia ou Int com o ID do Cliente"},
    "enable": {"type": "boolean", "required": True, "description": "Boolean status do cliente"},
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


@client_space.route("")
class clientView(Resource):

    def get(self):
        """ Lista com todos os clientes cadastrados """

        return {"data": [data.list_client() for data in ModelClient.query.all()]}, 200

    # @jwt_required
    @client_space.doc(params=schema)
    @required_params(schema)
    def post(self):
        """ Adicionar ou editar cliente.
        Para criar envie string vazia em id e para editar envie um int com o ID do cliente
        """

        data = request.json

        # Check if delivery_addres has one current selected
        current = len([address.get("current") for address in data.get(
            "delivery_address", "{}") if address.get("current")])
        if len(data.get("delivery_address")) > 1:
            if current != 1:
                return {"message": "Only one address current required"}, 400
        else:
            data["delivery_address"][0]["current"] = True
        # End check current address

        client = ModelClient.find_client(data.get("id"))

        if client:
            return self.put()

        try:
            client = ModelClient(**data)

            for address in data.get("delivery_address"):
                client.delivery_address.append(
                    ModelDelivereAdrressClient(client=client, **address))

            client.save_client()

            return {"message": "Client created", "data": client.json_client()}, 201
        except Exception as err:
            print(err)
            return {"message": "Internal error"}, 500

        return {"data": data}

    @client_space.hide
    @required_params(schema)
    def put(self):

        data = request.json

        client = ModelClient.find_client(data.get("id"))

        if client:

            try:

                client.update_client(**data)

                client.save_client()

                return {"message": "client updated", "data": client.json_client()}, 200

            except:
                return {"message": "Internal Error"}, 500

        return {"message": "client not found"}, 404


@client_space.route("/<int:id_client>")
class clientGet(Resource):

    def get(self, id_client):
        """ Seleciona cliente pelo ID """

        client = ModelClient.find_client(id_client)

        if client:
            return {"data": client.json_client()}, 200

        return {"message": "client not found"}, 404


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


@client_space.route("/<int:id_client>/address/<int:id_address>")
class ClientAddress(Resource):
    def delete(self, id_client, id_address):
        """ Deletar endereço de entrega cadastrado. """
        address = ModelDelivereAdrressClient.query.filter_by(
            id=id_address).filter_by(client=id_client).first()

        if address:
            try:
                address.delete_address()
                return {"message": "address deleted"}, 200
            except:
                return {"message": "Internal error"}, 500

        return {"message": "Address not found"}, 404

    @required_params(schema)
    def put(self, id_client, id_address):
        """ Atualiza endereço de entrega cadastrador"""

        data = request.json

        address = ModelDelivereAdrressClient.query.filter_by(
            id=id_address).filter_by(client=id_client).first()

        if address:

            try:

                address.update_address(**data)
                address.save_address()

                return {"message": "address updated", "data": address.list_address()}, 200
            except Exception as err:
                print(err)
                return {"message": "Internal error"}, 500

        return {"message": "Address not found"}, 404

    def patch(self, id_client, id_address):
        """ Seleciona o endereço de entrega como padrão """

        client = ModelClient.find_client(id_client)

        if not client:
            return {"message": "client not found"}, 404

        address = [address.list_address()
                   for address in client.delivery_address]

        for new in address:
            address = ModelDelivereAdrressClient.find_address(new.get("id"))
            address.current = False
            address.save_address()

        address = ModelDelivereAdrressClient.find_address(id_address)

        if not address:
            return {"message": "address not found"}, 404

        try:
            address.current = True
            address.save_address()

            return {"message": "address updated to current", "data": address.list_address()}, 200
        except Exception as err:
            print(err)
            return {"message": "internal error"}, 500


@client_space.route("/<int:id_client>/address")
class AddressPost(Resource):
    @required_params(schema)
    def post(self, id_client):
        """ Adiciona endereço de entrega """

        data = request.json

        client = ModelClient.find_client(id_client)

        if not client:
            return {"message": "Client not found"}, 400

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
            address = ModelDelivereAdrressClient(**data, client=id_client)
            address.save_address()

            return {"message": "address created", "data": address.list_address()}, 201
        except Exception as err:
            print(err)
            return {"message": "internal error"}, 200
