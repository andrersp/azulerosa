# -*- coding: utf-8 -*-

from datetime import datetime

from flask import request
from flask_restx import Resource, Namespace

from wraps import required_params

from model.purchase import ModelPurchaseItem, ModelPurchase


ns_purchase = Namespace("Purchasing Management",
                        description="Resources for purchase")


def to_date(s): return datetime.strptime(s, "%Y-%m-%d")


schema = {
    "id": {"type": "numeric", "required": True, "description": "numeric string value or int"},
    "provider_id": {"type": "integer", "required": True, "empty": False, "description": "provider id"},
    "value": {"type": "float", "required": True, "empty": False, "description": "net value"},
    "freight": {"type": "float", "required": True, "empty": False, "description": "cost of freight"},
    "discount": {"type": "float", "required": True, "empty": False, "description": "cost of discount"},
    "total_value": {"type": "float", "required": True, "empty": False, "description": "total value"},
    "delivery_time": {"type": "date", "required": True, "empty": False, "description": "Expected Delivery Date", "coerce": to_date},
    "payment_method": {"type": "integer", "required": True, "empty": False, "allowed": [1, 2], "description": "Payment method: 1 - Money, 2 - Card"},
    "parcel": {"type": "integer", "required": True, "min": 1, "description": "number of installments"},
    "status": {"type": "integer", "required": True, "empty": False, "allowed": [1, 2, 3], "description": "Stus: 1 - Orcamento, 2 - Aprovado, 3 Cancelado"},
    "obs": {"type": "string", "required": True, "empty": True, "description": "obs string"},
    "itens": {"type": "list", "required": True, "empty": False, "schema": {
        "type": "dict", "schema": {
            "id": {"type": "numeric", "required": True, "description": "item id, empty string on create purchase or integer on edit"},
            "id_product": {"type": "integer", "required": True, "empty": False, "description": "id product"},
            "unit_price": {"type": "float", "required": True, "empty": False, "description": "unit purchase value"},
            "qtde": {"type": "float", "required": True, "empty": False, "description": "Qtde of products"},
            "total_price": {"type": "float", "required": True, "empty": False, "description": "total purchase value"},
            "obs": {"type": "string", "required": True, "empty": True, "description": "obs string"}
        }
    }}

}


@ns_purchase.route("")
class PurchaseGet(Resource):

    def get(self):
        """ Get list of all purchase """

        return {"data": [data.list_purchases() for data in ModelPurchase.query.all()]}, 200

    @required_params(schema)
    @ns_purchase.doc(params=schema)
    def post(self):
        """ Create or update purchase """

        data = request.json

        purchase = ModelPurchase.find_purchase(data.get("id"))

        if purchase:
            return {"message": "update"}, 200

        try:
            purchase = ModelPurchase(**data)

            for itens in data.get("itens"):
                purchase.itens.append(ModelPurchaseItem(
                    **itens, id_purchase=purchase))
                print(itens)

            purchase.save_purchase()

            return {"message": "purchase saved", "data": purchase.list_purchases()}, 201
        except Exception as err:
            print(err)
            return {"message": "Internal error"}

        return {
            "data": data
        }, 200
