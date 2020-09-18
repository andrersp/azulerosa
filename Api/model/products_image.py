# -*- coding: utf-8 -*-

from db import db
from flask import request, url_for


class ModelImagesProducts(db.Model):
    id_image = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(80))
    product_id = db.Column(db.Integer, db.ForeignKey(
        "product.id_product"), nullable=False)

    def __init__(self, path, product_id):
        self.path = path
        self.product_id = product_id

    def list_images(self):
        return {
            "id": self.id_image,
            "url": request.url_root[:-1] + url_for("api.static", filename="images/{}".format(self.path))
        }

    @classmethod
    def find_image(cls, id_image):
        if not id_image:
            return None

        image = cls.query.filter_by(id_image=id_image).first()

        if image:
            return image
        return None

    def delete_image(self):
        db.session.delete(self)
        db.session.commit()
