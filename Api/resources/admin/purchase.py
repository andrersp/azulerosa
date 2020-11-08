# -*- coding: utf-8 -*-

from datetime import datetime

from flask import request, jsonify
from flask.views import MethodView
from flask_restx import Resource, Namespace

from wraps import required_params

from model.purchase import ModelPurchaseItem, ModelPurchase
from model.provider import ModelProvider
from model.products import ModelProducts
from model.purchase_options import (ModelDeliveryStatus,
                                    ModelPaymentStatus,
                                    ModelPaymentForm,
                                    ModelPaymentMethod)


ns_purchase = Namespace("Purchasing Management",
                        description="Endpoind para gerenciamento de compras")


def to_date(s): return datetime.strptime(s, "%Y-%m-%d")


schema = {
    "provider_id": {"type": "integer", "required": True, "empty": False, "description": "ID Fornecedor"},
    "value": {"type": "float", "required": True, "empty": False, "description": "Valor total dos produtos"},
    "freight": {"type": "float", "required": True, "empty": False, "description": "Valor do Frete. 0 Se não hoyver"},
    "discount": {"type": "float", "required": True, "empty": False, "description": "Valor do desconto. 0 Se não houver"},
    "total_value": {"type": "float", "required": True, "empty": False, "description": "Valor Total incluindo Frete e/ou Desconto"},
    "delivery_status": {"type": "integer", "required": True, "empty": False, "allowed": [1, 2], "description": "ID estatus entrega: 1 - Pendente, 2 - Em trânsito, "},
    "delivery_time": {"type": "string", "required": True, "empty": False, "description": "Data prevista para entrega"},
    "payment_form": {"type": "integer", "required": True, "empty": False, "allowed": [1, 2, 3], "description": "ID Forma de pagamento. 1 - À Vista, 2 - Depósito Bancário, 3 - A Prazo"},
    "payment_method": {"type": "integer", "required": True, "empty": False, "allowed": [1, 2], "description": "ID Meio de Pagamento: 1 - Dinheiro, 2 - Cartão, 3 - Tranferência Bancaria"},
    "parcel": {"type": "integer", "required": True, "min": 1, "check_with": "payment_method", "description": "Número de parcelas. 1 para pagemento a vista"},
    "obs": {"type": "string", "required": True, "empty": True, "description": "String para observação se houver"},
    "itens": {"type": "list", "required": True, "empty": False, "schema": {
        "type": "dict", "schema": {
            "product_id": {"type": "integer", "required": True, "empty": False, "description": "ID do Produto"},
            "product_name": {"type": "string", "required": False, "empty": True, "description": "Nome do Produto. Opcional. Usado para mensagem caso produto não exista"},
            "unit_price": {"type": "float", "required": True, "empty": False, "description": "Valor de compra unitário"},
            "qtde": {"type": "float", "required": True, "empty": False, "description": "Quantidade"},
            "total_price": {"type": "float", "required": True, "empty": False, "description": "Valor Total dos itens"},
            "obs": {"type": "string", "required": True, "empty": True, "description": "String para observação se houver"}
        }
    }, "description": "List with dictionaries of itens"}

}


schema_delivery = {
    "delivery_status": {"type": "integer", "required": True, "allowed": [1, 2, 3], "description": "Int ID status entrega. Permitidos: 1, 2 ou 3"}
}


@ns_purchase.route("")
class PurchaseApi(MethodView):

    def get(self, purchase_id):
        """ Get list of all purchase """

        if purchase_id:
            purchase = ModelPurchase.find_purchase(purchase_id)
            if purchase:
                return jsonify({"data": purchase.json_purchase()}), 200

            return jsonify({"message": "Purchase not found"})

        return jsonify({"data": [data.list_purchases() for data in ModelPurchase.query.all()]}), 200

    @required_params(schema)
    @ns_purchase.doc(params=schema)
    def post(self):
        """ Create or update purchase """

        data = request.json

        provider = ModelProvider.find_provider(data.get("provider_id"))

        if not provider:
            return jsonify({"message": "Provider not found"}), 400

        total = []
        for itens in data.get("itens"):

            item = ModelProducts.find_product(itens.get("product_id"))

            if not item:
                return jsonify({"message": "Item Not Found", "item": itens}), 400

            if not itens.get("unit_price") * itens.get("qtde") == itens.get("total_price"):
                return jsonify({"message": "Total value of item: {} does not check".format(item.name)}), 400

            total.append(itens.get("total_price"))

        if sum(total) != data.get("value"):
            return jsonify({"message": "Value does not check"}), 400

        total_check = sum(total) + data.get("freight") - data.get("discount")

        if total_check != data.get("total_value"):
            return jsonify({"message": "total value does not check "}), 400

        try:
            purchase = ModelPurchase(**data)

            for itens in data.get("itens"):
                purchase.itens.append(ModelPurchaseItem(
                    **itens, id_purchase=purchase, provider_id=provider.provider_id))

            purchase.save_purchase()

            return jsonify({"message": "purchase saved", "data": purchase.json_purchase()}), 201
        except Exception as err:
            print(err)
            return jsonify({"message": "Internal error"}), 500

    # Update Purchase

    def put(self, purchase_id):

        data = request.json

        purchase = ModelPurchase.find_purchase(purchase_id)

        if not purchase:
            return jsonify({"message": "Purchase  not found"}), 404

        if purchase.delivery_status == 1:
            return jsonify({"message": "Delivered purchase cannot be changed"}), 400

        provider = ModelProvider.find_provider(data.get("provider_id"))

        if not provider:
            return jsonify({"message": "Provider not found"}), 400

        total = []
        for itens in data.get("itens"):

            item = ModelProducts.find_product(itens.get("product_id"))

            if not item:
                return jsonify({"message": "Item Not Found", "item": itens}), 400

            if not itens.get("unit_price") * itens.get("qtde") == itens.get("total_price"):
                return jsonify({"message": "Total value of item: {} does not check".format(item.name)}), 400

            total.append(itens.get("total_price"))

        if sum(total) != data.get("value"):
            return jsonify({"message": "Value does not check"}), 400

        total_check = sum(total) + data.get("freight") - data.get("discount")

        if total_check != data.get("total_value"):
            return jsonify({"message": "total value does not check "}), 400

        try:
            purchase.update_purchase(**data)

            for itens in data.get("itens"):
                purchase.itens.append(ModelPurchaseItem(
                    **itens, id_purchase=purchase, provider_id=provider.provider_id))

            purchase.save_purchase()

            return jsonify({"message": "Purchase updated", "data": purchase.json_purchase()}), 200
        except Exception as err:
            print(err)
            return jsonify({"message": "Internal error"}), 500

    @required_params(schema_delivery)
    def patch(self, purchase_id):
        """ Atualizar status da entrega.
        1: Pendente
        2: Em Trânsito
        3: Entregue (Dar entrada do produto no estoque)
        """

        data = request.json

        purchase = ModelPurchase.find_purchase(purchase_id)

        if purchase:

            delivery_status = purchase.delivery_status

            if delivery_status == 3:
                return jsonify({"message": "Delivered purchase cannot be changed"}), 400

            if data.get("delivery_status") == delivery_status:
                return jsonify({"message": "No changes to make"}), 400

            try:
                purchase.update_delivery_status(data.get("delivery_status"))
                purchase.save_purchase()
                return jsonify({"message": "Updated delivery status", "status": purchase.delivery_status_name.name}), 200
            except Exception as err:
                print(err)
                return jsonify({"message": "internal error"}), 400

        return {"message": "purchase not found"}, 404
