# -*- coding: utf-8 -*-

from datetime import datetime


from db import db


class ModelPurchase(db.Model):
    __tablename__ = 'purchase'

    id_purchase = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.provider_id'))
    value = db.Column(db.Float(precision=2), default=0.00)
    freight = db.Column(db.Float(precision=2), default=0.00)
    discount = db.Column(db.Float(precision=2), default=0.00)
    total_value = db.Column(db.Float(precision=2))
    delivery_time = db.Column(db.DateTime)
    tracking_cod = db.Column(db.String(20))
    payment_method = db.Column(db.Integer)
    parcel = db.Column(db.Integer, default=1)
    delivery_status = db.Column(db.Integer)
    payment_status = db.Column(db.Integer)
    status = db.Column(db.Integer)
    obs = db.Column(db.String(80))
    date = db.Column(db.DateTime, default=datetime.now())
    itens = db.relationship('ModelPurchaseItem',
                            backref='purchase', lazy='joined')

    provider_name = db.relationship(
        "ModelProvider", backref='provider_name', lazy='joined')

    __mapper_args__ = {
        "order_by": id_purchase
    }

    def __init__(self, id, provider_id, value, freight, discount, total_value,
                 delivery_time, payment_method, parcel,
                 status, obs, itens):
        self.id = id
        self.provider_id = provider_id
        self.value = value
        self.freight = freight
        self.discount = discount
        self.total_value = total_value
        self.delivery_time = delivery_time
        self.payment_method = payment_method
        self.parcel = parcel
        self.obs = obs
        self.status = status
        # self.itens = itens

    def list_purchases(self):
        return {
            "id": self.id_purchase,
            "provider": self.provider_name.fancy_name,
            "value": "%.2f" % (self.value),
            "delivery_time": "{}-{}-{}".format(self.delivery_time.day,
                                               self.delivery_time.month,
                                               self.delivery_time.year),
            "tracking_cod": self.tracking_cod,
            "delivery_status": self.delivery_status,
            "payment_status": self.payment_status,
            "status": self.status,
            "itens": [item.list_itens() for item in self.itens]
        }

    def save_purchase(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_purchase(cls, id_purchase):

        if not id_purchase:
            return None
        purchase = cls.query.filter_by(id_purchase=id_purchase).first()

        if purchase:
            return purchase

        return None

    def update_purchase(self, id, provider_id, value, freight, discount, total_value,
                        delivery_time, payment_method, parcel,
                        status, obs, itens):
        self.provider_id = provider_id
        self.value = value
        self.freight = freight
        self.discount = discount
        self.total_value = total_value
        self.delivery_time = delivery_time
        self.payment_method = payment_method
        self.parcel = parcel
        self.obs = obs
        self.itens = itens


class ModelPurchaseItem(db.Model):
    __tablename__ = "purchase_item"
    id_item = db.Column(db.Integer, primary_key=True)
    id_purchase = db.Column(db.Integer, db.ForeignKey('purchase.id_purchase'))
    id_product = db.Column(db.Integer, db.ForeignKey(
        'product.id_product'), nullable=False)
    provider_id = db.Column(db.Integer)
    unit_price = db.Column(db.Float(precision=2), default=0.00)
    qtde = db.Column(db.Float(precision=2))
    total_price = db.Column(db.Float(precision=2), default=0.00)
    delivery_date = db.Column(db.DateTime)
    obs = db.Column(db.String(120))

    product_name = db.relationship(
        "ModelProducts", backref=db.backref('product_name', lazy=False))

    def __init__(self, id, id_purchase, product_id, unit_price,
                 qtde, total_price, obs, **kwargs):
        self.id = id
        self.id_purchase = id_purchase
        self.id_product = product_id
        self.unit_price = unit_price
        self.qtde = qtde
        self.total_price = total_price
        self.obs = obs

    def list_itens(self):
        return {
            "id": self.id_item,
            "product": self.product_name.name,
            "unit_price": self.unit_price,
            "qtde": self.qtde,
            "total_price": self.total_price,
            "obs": self.total_price
        }