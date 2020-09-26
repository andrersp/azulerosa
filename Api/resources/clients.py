# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

from flask import request
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required

from wraps import required_params

from model.clients import ModelClient, ModelDelivereAdrressClient

client_space = Namespace("Clients Manager", description="Resource for clients")

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
        For crente a new cliente send key "id" with a empty string.
        
        """       

        data = request.json

        # Check if delivery_addres has one current selected
        current = len([address.get("current") for address in data.get("delivery_address", "{}") if address.get("current")])
        
        if current != 1:
            return {"message": "Only one address current required"}, 400
        # End check current address


        client = ModelClient.find_client(data.get("id"))
                
        if client:
            return self.put()

        try:
            client = ModelClient(**data)
            
            for address in data.get("delivery_address"):                
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
@client_space.route("/<int:id_client>/<int:id_address>")
class ClientAddress(Resource):
    def delete(self, id_client, id_address):
        """ Delete Client Delivery Address """ 
        address = ModelDelivereAdrressClient.query.filter_by(id=id_address).filter_by(client=id_client).first()

        if address:
            try:
                address.delete_address()
                return {"message": "address deleted"}, 200
            except:
                return {"message": "Internal error"}, 500
        
        return {"message": "Address not found"}, 404

    @required_params(schema)    
    def put(self, id_client, id_address):

        """ Update delivery address """

        data = request.json

        address = ModelDelivereAdrressClient.query.filter_by(id=id_address).filter_by(client=id_client).first()

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
        """ Make this address current """

        client = ModelClient.find_client(id_client)

        if not client:
            return {"message": "client not found"}, 404

        address = [address.list_address() for address in client.delivery_address]

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
        """ Add delivery address """

        data = request.json
        
        client = ModelClient.find_client(id_client)

        if not client:
            return {"message": "Client not found"}, 400
        
        address = [address.list_address() for address in client.delivery_address]

        if not address:
            data["current"] = True
        else:
            if data.get("current"):
                for new in address:
                    address = ModelDelivereAdrressClient.find_address(new.get("id"))                    
                    address.current = False
                    address.save_address()

        try:
            address = ModelDelivereAdrressClient(**data, client=id_client)
            address.save_address()

            return {"message": "address created", "data": address.list_address()}, 201
        except Exception as err:
            print(err)
            return {"message": "internal error"}, 200






    
