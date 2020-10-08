# -*- coding: utf-8 -*-

import os

from flask import request, url_for

from db import db

from model.stock import ModelStock
from model.products_unit import ModelProductUnit
providers = db.Table('providers',
                     db.Column('privider_id', db.Integer, db.ForeignKey(
                         'provider.provider_id'), primary_key=True),
                     db.Column('product_id', db.Integer, db.ForeignKey(
                         'product.id_product'), primary_key=True)
                     )


class ModelProducts(db.Model):

    __tablename__ = "product"
    id_product = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    category = db.Column(db.Integer, db.ForeignKey(
        'product_category.id_category'), nullable=False)
    brand = db.Column(db.Integer)
    unit = db.Column(db.Integer, db.ForeignKey(
        'product_unit.id_unit'), nullable=False)
    minimum_stock = db.Column(db.Float(precision=2))
    maximum_stock = db.Column(db.Float(precision=2))
    short_description = db.Column(db.String(200))
    long_description = db.Column(db.Text)
    cover = db.Column(db.String(80))
    height = db.Column(db.Float(precision=2))
    widht = db.Column(db.Float(precision=2))
    length = db.Column(db.Float(precision=2))
    weight = db.Column(db.Float(precision=2))
    percentage_sale = db.Column(db.Float(precision=2), nullable=True)
    update_price = db.Column(db.Boolean, default=False)
    sale_price = db.Column(db.Float(precision=2))
    maximum_discount = db.Column(db.Float(precision=2))
    available = db.Column(db.Boolean)
    images = db.relationship("ModelImagesProduct",
                             backref="product", lazy=True)

    category_name = db.relationship(
        "ModelCategoryProduct", foreign_keys=category)

    unit_name = db.relationship("ModelProductUnit", foreign_keys=unit)

    # category_name = db.relationship(    ##fast
    #     "ModelCategoryProduct", backref=db.backref('category', lazy='dynamic'))

    providers = db.relationship('ModelProvider', secondary=providers, lazy='subquery',
                                backref=db.backref('providers', lazy=True))
    latest_purchases = db.relationship(
        'ModelPurchaseItem', backref='product', lazy=True)

    stock = db.relationship("ModelStock", backref='product',
                            lazy='joined', uselist=False)

    __mapper_args__ = {
        "order_by": id_product
    }

    def __init__(self, id, name, category, brand, unit,
                 minimum_stock, maximum_stock, percentage_sale,
                 long_description, short_description, cover,
                 sale_price, weight, update_price,
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
        self.cover = cover
        self.update_price = update_price
        self.percentage_sale = percentage_sale
        self.unit = unit

    def list_product(self):
        return {
            "id": self.id_product,
            "name": self.name,
            "category": self.category_name.name,
            "brand": self.brand,
            "cover": request.url_root[:-1] + url_for("api.static", filename="images/{}".format(self.cover)) if self.cover else "",
            "available_stock": self.stock.available_stock,
            "sale_price": self.sale_price,
        }

    def json_product(self):
        return {
            "id": self.id_product,
            "name": self.name,
            "category": self.category,
            "brand": self.brand,
            "unit": self.unit,
            "minimum_stock": self.minimum_stock,
            "maximum_stock": self.maximum_discount,
            "short_description": self.short_description,
            "long_description": self.long_description,
            "cover": request.url_root[:-1] + url_for("api.static", filename="images/{}".format(self.cover)) if self.cover else "",
            "height": self.height,
            "widht": self.widht,
            "length": self.length,
            "weight": self.weight,
            "percentage_sale": self.percentage_sale,
            "update_price": self.update_price,
            "sale_price": self.sale_price,
            "maximum_discount": self.maximum_discount,
            "images": [image.list_images() for image in self.images],
            "providers": [data.list_provider_product() for data in self.providers],
            "latest_purchases": [data.latest() for data in self.latest_purchases],
            "stock": {
                "purchase_price": self.stock.purchase_price,
                "available_stock": self.stock.available_stock
            }
        }

    def list_product_provider(self):
        return {
            "id": self.id_product,
            "name": self.name
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
                       cover, images, provider, available_stock,
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
        # self.provider = provider
        self.providers.clear()

        if cover:
            path = "static/images/{}".format(self.cover)
            os.remove(path)
            self.cover = cover


# Triger Function to inserto product into stock table
""" Trigers """
func = db.DDL(
    """
    CREATE OR REPLACE FUNCTION create_stock()
    RETURNS TRIGGER AS $TGR_Stock$
    BEGIN
    INSERT INTO stock (id_product, available_stock, purchase_price, initial_stock)
    VALUES
    (NEW.id_product, 0.00, 0.00, False);
    RETURN NEW;
    END; $TGR_Stock$ LANGUAGE PLPGSQL
    """

)


trigger = db.DDL(
    """
    CREATE TRIGGER  create_stock
    AFTER INSERT ON product
    FOR EACH ROW
    EXECUTE PROCEDURE create_stock();
    """

)
db.event.listen(
    ModelProducts.__table__,
    'after_create',
    func.execute_if(dialect='postgresql')
)
db.event.listen(
    ModelProducts.__table__,
    'after_create',
    trigger.execute_if(dialect='postgresql')
)

# End Triger
