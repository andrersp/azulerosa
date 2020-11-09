# -*- coding: utf-8 -*-

import os

from flask import request, url_for

from db import db

from model.stock import ModelStock
from model.products_unit import ModelProductUnit
from model.products_category import ModelCategoryProduct
from model.products_image import ModelImagesProduct
from model.products_brand import ModelBrandProduct
providers = db.Table('providers',
                     db.Column('privider_id', db.Integer, db.ForeignKey(
                         'provider.provider_id'), primary_key=True),
                     db.Column('product_id', db.Integer, db.ForeignKey(
                         'product.id_product'), primary_key=True)
                     )


class ModelProducts(db.Model):

    __tablename__ = "product"
    id_product = db.Column(db.Integer, primary_key=True)
    internal_code = db.Column(db.String(18))
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
    width = db.Column(db.Float(precision=2))
    length = db.Column(db.Float(precision=2))
    weight = db.Column(db.Float(precision=2))
    minimum_sale = db.Column(db.Float(precision=2), nullable=True)
    sale_price = db.Column(db.Float(precision=2))
    maximum_discount = db.Column(db.Float(precision=2))
    available = db.Column(db.Boolean)
    subtract = db.Column(db.Boolean)
    images = db.relationship("ModelImagesProduct",
                             backref="product", lazy=True)

    # unit_name = db.relationship("ModelProductUnit", foreign_keys=unit)

    providers = db.relationship('ModelProvider', secondary=providers, lazy='subquery',
                                backref=db.backref('providers', lazy=True))
    latest_purchases = db.relationship(
        'ModelPurchaseItem', backref='product', lazy=True)

    stock = db.relationship("ModelStock", backref='product',
                            lazy='joined', uselist=False)

    def __init__(self, images, provider, **kwargs):
        super(ModelProducts, self).__init__(**kwargs)

    @classmethod
    def list_product(cls):

        data = cls.query.with_entities(
            cls.id_product, cls.name, cls.stock)

        data = [{
            "id": id,
            "name": name,
            "short_description": description,
            "internal_code": internal_code,
            "category": category,
            "brand": brand if brand else "",
            "cover": request.url_root[:-1] + url_for("api.static", filename="images/{}".format(cover)) if cover else "",
            "sale_price": sale_price,
            "qtde": qtde

        } for id, name, description, internal_code, category, brand, cover,
            sale_price, qtde in
            cls.query.join(ModelStock)
            .join(ModelCategoryProduct)
            .outerjoin(ModelBrandProduct, cls.brand == ModelBrandProduct.id_brand)
            .with_entities(
            cls.id_product, cls.name, cls.short_description, cls.internal_code,
            ModelCategoryProduct.name, ModelBrandProduct.name, cls.cover,
            cls.sale_price, ModelStock.available_stock).order_by(cls.id_product)
        ]

        return data

    def get_product(self):
        return {
            "id": self.id_product,
            "internal_code": self.internal_code,
            "name": self.name,
            "category": self.category,
            "brand": self.brand,
            "unit": self.unit,
            "minimum_stock": self.minimum_stock,
            "maximum_stock": self.maximum_stock,
            "subtract": self.subtract,
            "short_description": self.short_description,
            "long_description": self.long_description,
            "cover": request.url_root[:-1] + url_for("api.static", filename="images/{}".format(self.cover)) if self.cover else "",
            "available": self.available,
            "height": self.height,
            "width": self.width,
            "length": self.length,
            "weight": self.weight,
            "minimum_sale": self.minimum_sale,
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

    @classmethod
    def find_internal_code(cls, code):
        if not code:
            return None

        product = cls.query.filter_by(internal_code=code).all()

        products = [data.id_product for data in product]

        if product:
            return products

        return None

    def save_product(self):
        db.session.add(self)
        db.session.commit()

    def delete_product(self):
        db.session.delete(self)
        db.session.commit()

    def update_product(self, name, category, brand, unit,
                       minimum_stock, maximum_stock, minimum_sale,
                       long_description, short_description, cover,
                       sale_price, weight, subtract, internal_code,
                       available, height, width, length, maximum_discount, images, provider):

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
        self.width = width
        self.length = length
        self.weight = weight
        self.maximum_discount = maximum_discount

        if self.cover:
            path = "static/images/{}".format(self.cover)
            os.remove(path)

        self.cover = cover
        self.minimum_sale = minimum_sale
        self.unit = unit
        self.subtract = subtract
        self.internal_code = internal_code
        # [self.providers.remove(data) for data in self.providers]
        self.providers.clear()


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
