# -*- coding: utf-8 -*-

from db import db


class ModelStock(db.Model):

    __tablename__ = 'stock'
    stock_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id_product'))
    qtde = db.Column(db.Float(precision=2), default=0.00)
    purchase_price = db.Column(db.Float(precision=2), default=0.00)

    def get_stoc(self):
        return {
            "qtde": self.qtde,
            "purchase_price": self.purchase_price
        }


class ModelStockEntry(db.Model):

    __tablename__ = 'stock_entry'
    entry_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id_product'))
    qtde = db.Column(db.Float(precision=2), default=0.00)
    purchase_price = db.Column(db.Float(precision=0.00))
