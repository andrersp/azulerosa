# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

from flask import request
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required

from wraps import required_params

from model.clients import ModelClient, ModelDelivereAdrressClient

client_space = Namespace("Clilentes", description="Resource for clients")

schema = {
    "id": {"type": "numeric", "required": True, "description": "numeric string value or int"},
    "enable": {"type": "boolean", "required": True, "description": "Status of client"},
    "type_registration": {"type": "integer", "allowed": [1, 2], "required": True, "description": "Type of client registration. 1 : CPF, 2: CNPJ"},
    "cnpj": {"type": "string", "required": True, "check_with": "registration"},
    "state_registration": {"type": "string", "required": True, "description": "State company registration", "maxlength": 20},
    "municipal_registration": {"type": "string", "required": True, "description": "municipal company registration", "maxlength": 12},
    "fancy_name": {"type": "string", "required": True, "description": "company fancy name"},
    "company_name": {"type": "string", "required": True, "description": "Company name", "empty": False},
    "contact_name": {"type": "string", "required": True, "description": "Company contact name", "empty": True},
    "phone": {"type": "string", "required": True, "check_with": "phonecheck",  "description": "Phone Number of company"},
    "cell_phone": {"type": "string", "required": True, "check_with": "cellcheck", "description": "Cell Number of company"},
    "email": {"type": "string", "required": True, "description": "Contact email", "empty": True, "maxlength": 40},
    "zip_code": {"type": "string", "required": True, "maxlength": 8, "minlength": 8, "empty": False, "description": "Zip Code address", "regex": '[0-9]+'},
    "address": {"type": "string", "required": True, "description": "Company Address", "empty": False, "maxlength": 80},
    "number": {"type": "string", "required": True, "description": "Address number", "empty": True, "maxlength": 60},
    "complement": {"type": "string", "required": True, "description": "Address Complement", "empty": True, "maxlength": 40},
    "neighborhood": {"type": "string", "required": True, "description": "neighborhood name", "empty": False, "maxlength": 80},
    "city": {"type": "string", "required": True, "description": "Company city", "empty": False, "maxlength": 80},
    "state": {"type": "string", "required": True, "description": "Company State", "empty": False, "maxlength": 2},
    "delivery_address": {"type": "list", "required": True, "empty": True, "schema": {"type": "dict", "schema": {
        "zip_code": {"type": "string", "required": True, "maxlength": 8, "minlength": 8, "empty": False, "description": "Zip Code address", "regex": '[0-9]+'},
        "address": {"type": "string", "required": True, "description": "Company Address", "empty": False, "maxlength": 80},
    "number": {"type": "string", "required": True, "description": "Address number", "empty": True, "maxlength": 60},
    "complement": {"type": "string", "required": True, "description": "Address Complement", "empty": True, "maxlength": 40},
    "neighborhood": {"type": "string", "required": True, "description": "neighborhood name", "empty": False, "maxlength": 80},
    "city": {"type": "string", "required": True, "description": "Company city", "empty": False, "maxlength": 80},
    "state": {"type": "string", "required": True, "description": "Company State", "empty": False, "maxlength": 2},
    "current": {"type": "boolean", "required": True}
    }} },
    "obs": {"type": "string", "required": True, "description": "Company Observation", "empty": True},
    "notify": {"type": "boolean", "required": True, "description": "If customer wants to receive promotions"}

}


@client_space.route("")
class clientView(Resource):

    def get(self):
        """ List of all client """

        return {"data": [data.list_client() for data in ModelClient.query.all()]}, 200

    # @jwt_required
    @client_space.doc(params=schema)
    @required_params(schema)
    def post(self):

        """  Create or Updated client 
        For crente a new cliente send key "id" with a empty string
        """       

        data = request.json

        client = ModelClient.find_client(data.get("id"))

        if client:
            return {"message": 'update'}, 200
            # return self.put()

        try:
            client = ModelClient(**data)

            for address in data.get("delivery_address"):
                print(address)
                client.delivery_address.append(ModelDelivereAdrressClient(client=client, **address))

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
        """ Get client By id """

        client = ModelClient.find_client(id_client)

        if client:
            return {"data": client.json_client()}, 200
        
        return {"message": "client not found"}, 404       
