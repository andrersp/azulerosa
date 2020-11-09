# -*- coding: utf-8 -*-

from flask import jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from model.clients import ModelClient
from model.products import ModelProducts


class HomeApi(MethodView):
    @jwt_required
    def get(self):

        clients = ModelClient.query.count()
        products = ModelProducts.query.count()

        # session.query(Table.column, func.count(Table.column)).group_by(Table.column).all()
        # print([data.list_product() for data in ModelProducts.query.group_by(ModelProducts.category)])

        return jsonify({"data": {"clients": clients, "products": products}}), 200
