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
    long_description = db.Column(db.Text)
    short_description = db.Column(db.String(200))
    sale_price = db.Column(db.Float(precision=2))
    available = db.Column(db.Boolean)
    height = db.Column(db.Float(precision=2))
    widht = db.Column(db.Float(precision=2))
    length = db.Column(db.Float(precision=2))
    weight = db.Column(db.Float(precision=2))
    maximum_discount = db.Column(db.Float(precision=2))
    images = db.relationship("ModelImagesProducts", lazy="select",
                             backref=db.backref("product", lazy="joined"))

    __mapper_args__ = {
        "order_by": id_product
    }

    def __init__(self, id, name, category, brand, minimum_stock, maximum_stock,
                 long_description, short_description, sale_price, weight,
                 available, height, widht, length, maximum_discount, **kwargs):
        self.id = id
        self.name = name
        self.category = category
        self.brand = brand
        self.minimum_stock = minimum_stock
        self.maximum_stock = maximum_stock
        self.long_description = long_description
        self.short_description = short_description
        self.sale_price = sale_price
        self.available = available
        self.height = height
        self.widht = widht
        self.length = length
        self.weight = weight
        self.maximum_discount = maximum_discount

    def list_product(self):
        return {
            "id": self.id_product,
            "name": self.name,
            "category": self.category,
            "brand": self.brand,
            "current_stock": 1,
            "sale_price": self.sale_price,
            "available": self.available,
            "images": [image.list_images() for image in self.images]
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
                       long_description, short_description, sale_price, weight,
                       available, height, widht, length, maximum_discount):
        self.name = name
        self.category = category
        self.brand = brand
        self.minimum_stock = minimum_stock
        self.maximum_stock = maximum_stock
        self.long_description = long_description
        self.short_description = short_description
        self.sale_price = sale_price
        self.available = available
        self.height = height
        self.widht = widht
        self.length = length
        self.weight = weight
        self.maximum_discount = maximum_discount
