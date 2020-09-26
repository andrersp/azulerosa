# -*- coding: utf-* -*-

from db import db


class ModelCategoryProduct(db.Model):

    __tablename__ = "category"
    id_category = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.Text)

    __mapper_args__ = {
        "order_by": id_category
    }

    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description

    def list_category(self):
        return {
            "id": self.id_category,
            "name": self.name,
            "description": self.description
        }

    @classmethod
    def find_category(cls, id_category):

        if not id_category:
            return None

        category = cls.query.filter_by(id_category=id_category).first()

        if category:
            return category

        return None

    def save_category(self):
        db.session.add(self)
        db.session.commit()

    def delete_category(self):
        db.session.delete(self)
        db.session.commit()

    def update_category(self, id, name, description):
        self.name = name
        self.description = description
