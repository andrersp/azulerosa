# -*- coding: utf-* -*-

from sqlalchemy import event, DDL

from db import db


class ModelBrandProduct(db.Model):

    __tablename__ = "product_brand"
    id_brand = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(120))

    def list_brand(self):
        return {
            "id": self.id_brand,
            "name": self.name,
            "description": self.description
        }

    @classmethod
    def find_brand(cls, id_brand):

        if not id_brand:
            return None

        brand = cls.query.filter_by(id_brand=id_brand).first()

        if brand:
            return brand

        return None

    def save_brand(self):
        db.session.add(self)
        db.session.commit()

    def delete_brand(self):
        db.session.delete(self)
        db.session.commit()

    def update_brand(self, name, description):
        self.name = name
        self.description = description
