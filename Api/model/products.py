# -*- coding: utf-8 -*-

from db import db


class ModelProducts(db.Model):

    __tablename__ = "product"
    id_product = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    category = db.Column(db.Integer)
    brand = db.Column(db.Integer)
    minimum_stock = db.Column(db.Float(precision=2))
    maximum_stock = db.Column(db.Float(precision=2))
    description = db.Column(db.Text)
    obs = db.Column(db.String(120))
    sale_price = db.Column(db.Float(precision=2))

    __mapper_args = {
        "order_by": id
    }

    def __init__(self, id, name, category, brand, minimum_stock, maximum_stock,
                 description, obs, sale_price):
        self.id = id
        self.name = name
        self.category = category
        self.brand = brand
        self.minimum_stock = minimum_stock
        self.maximum_stock = maximum_stock
        self.description = description
        self.obs = obs
        self.sale_price = sale_price

    def list_product(self):
        return {
            "id": self.id_product,
            "name": self.name,
            "category": self.category,
            "brand": self.brand,
            "current_stock": 1,
            "sale_price": self.sale_price
        }

    @classmethod
    def find_product(cls, id_product):

        if not id_product:
            return None

        product = cls.query.filter_by(id_product=id_product).first()

        if product:
            return product
        return None

    def save_product(self):
        db.session.add(self)
        db.session.commit()

    def delete_product(self):
        db.session.delete(self)
        db.session.commit()

    def update_product(self, id, name, category, brand, minimum_stock, maximum_stock,
                       description, obs, sale_price):
        self.name = name
        self.category = category
        self.brand = brand
        self.minimum_stock = minimum_stock
        self.maximum_stock = maximum_stock
        self.description = description
        self.obs = obs
        self.sale_price = sale_price
