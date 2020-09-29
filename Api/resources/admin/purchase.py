# -*- coding: utf-8 -*-

from datetime import datetime

from flask import request
from flask_restx import Resource, Namespace

from wraps import required_params

from model.purchase import ModelPurchaseItem, ModelPurchase
from model.provider import ModelProvider
from model.products import ModelProducts
from model.purchase_options import ModelDeliveryStatus, ModelPaymentStatus


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
    "delivery_status": {"type": "integer", "required": True, "empty": False, "allowed": [1, 2], "description": "Delivery Status integer id: 1 - Pendente, 2 - Em trânsito"},
    "delivery_time": {"type": "date", "required": True, "empty": False, "description": "Expected Delivery Date", "coerce": "form_date"},
    "payment_method": {"type": "integer", "required": True, "empty": False, "allowed": [1, 2], "description": "Payment method: 1 - Money, 2 - Card"},
    "parcel": {"type": "integer", "required": True, "min": 1, "description": "number of installments"},
    "status": {"type": "integer", "required": True, "empty": False, "allowed": [1, 2, 3], "description": "Stus: 1 - Orcamento, 2 - Aprovado, 3 Cancelado"},
    "obs": {"type": "string", "required": True, "empty": True, "description": "obs string"},
    "itens": {"type": "list", "required": True, "empty": False, "schema": {
        "type": "dict", "schema": {
            "id": {"type": "numeric", "required": True, "description": "item id, empty string on create purchase or integer on edit"},
            "product_id": {"type": "integer", "required": True, "empty": False, "description": "id product"},
            "product_name": {"type": "string", "required": False, "empty": True, "description": "Optional name of product"},
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

        provider = ModelProvider.find_provider(data.get("provider_id"))

        if not provider:
            return {"message": "Provider not found"}, 400

        for itens in data.get("itens"):

            item = ModelProducts.find_product(itens.get("product_id"))

            if not item:
                return {"message": "Item Not Found", "item": itens}, 400

        purchase = ModelPurchase.find_purchase(data.get("id"))
        if purchase:
            return {"message": "update"}, 200

        try:
            purchase = ModelPurchase(**data)

            for itens in data.get("itens"):
                purchase.itens.append(ModelPurchaseItem(
                    **itens, id_purchase=purchase, provider_id=provider.provider_id))
                print(itens)

            purchase.save_purchase()

            return {"message": "purchase saved", "data": purchase.list_purchases()}, 201
        except Exception as err:
            print(err)
            return {"message": "Internal error"}, 500

        return {
            "data": data
        }, 200


schema = {
    "id": {"type": "integer", "required": True, "description": "integer id of purchase"},
    "delivery_status": {"type": "integer", "required": True, "allowed": [1, 2, 3, 4], "description": "integer status of delivery"}
}


@ns_purchase.route("/delivery")
class PurchaseDeliveStatus(Resource):

    @required_params(schema)
    @ns_purchase.doc(params=schema)
    def post(self):
        """ Update Delivery Status """

        data = request.json

        purchase = ModelPurchase.find_purchase(data.get("id"))

        if purchase:
            purchase.update_livery_status(data.get("delivery_status"))
            purchase.save_purchase()

            return {"message": "updated"}
