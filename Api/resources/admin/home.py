# -*- coding: utf-8 -*-

from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required
from sqlalchemy import func

from model.clients import ModelClient
from model.products import ModelProducts


ns_home = Namespace("Home", description="Home Endpoint")

@ns_home.route("")
class ViewHome(Resource):
    # @jwt_required
    def get(self):

        clients = ModelClient.query.count()
        products = ModelProducts.query.count()
        
        
        # session.query(Table.column, func.count(Table.column)).group_by(Table.column).all()
        # print([data.list_product() for data in ModelProducts.query.group_by(ModelProducts.category)])

        return {"data": {"clients": clients, "products": products}}, 200

        
