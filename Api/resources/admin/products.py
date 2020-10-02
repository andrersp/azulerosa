# -*- coding: utf-8 -*-

from base64 import b64decode
import os
import imghdr
from datetime import datetime
from uuid import uuid4
from PIL import Image
from resizeimage import resizeimage
import io

from flask import request
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required

from wraps import required_params

from model.products import ModelProducts
from model.products_image import ModelImagesProduct
from model.provider import ModelProvider
from model.products_category import ModelCategoryProduct

product_space = Namespace(
    "Products Manager", description="Resources for Produtos")

schema = {
    "id": {"type": "numeric", "required": True, "description": "numeric string value or int"},
    "name": {"type": "string", "required": True, "empty": False, "description": "name of product"},
    "category": {"type": "integer", "required": True, "description": "integer value of category"},
    "brand": {"type": "integer", "required": True, "description": "integer valur of brand"},
    "minimum_stock": {"type": "float", "required": True, "description": "float value of minimum stock"},
    "maximum_stock": {"type": "float", "required": True, "description": "float value of maximum stock"},
    "long_description": {"type": "string", "required": True, "empty": True, "description": "Long Description of product"},
    "short_description": {"type": "string", "required": True, "empty": False, "description": "Short Description of product, max 200", "maxlength": 200},
    "cover": {"type": "string", "required": True, "empty": True, "description": "tumbnail cover image"},
    "sale_price": {"type": "float", "required": True, "description": "value of sale price of product"},
    "available": {"type": "boolean", "required": True, "description": "if product is unavailable for sale"},
    "height": {"type": "float", "required": True, "description": "product height for shipping"},
    "available_stock": {"type": "float", "required": True, "description": "Avalilable stock"},
    "widht": {"type": "float", "required": True, "description": "product widht for shipping"},
    "length": {"type": "float", "required": True, "description": "product length for shipping"},
    "weight": {"type": "float", "required": True, "description": "product weight for shipping"},
    "maximum_discount": {"type": "float", "required": True, "description": "maximum_discount for this product"},
    "images": {"type": "list", "schema": {"type": "string"}, "required": True, "empty": True},
    "provider": {"type": "list", "schema": {"type": "integer", "required": True}, "required": True, "empty": True, "description": "List of id providers"}
}


# Function to converte base64 image to file

def upload_image(image, cover=False):

    image = b64decode(image.encode())
    extension = imghdr.what(None, h=image)
    filename = str(uuid4()) + "." + extension

    if cover:
        filename = str(uuid4()) + "-cover." + extension
        pic = io.BytesIO(image)
        with Image.open(pic) as image_pil:
            cover = resizeimage.resize_cover(image_pil, [100, 100])
            cover.save("static/images/{}".format(filename), image_pil.format)
    else:
        with open(os.path.join("static/images/" + filename), "wb") as file_to_save:
            file_to_save.write(image)

    return filename


@product_space.route("")
class ProductsGet(Resource):
    # @jwt_required
    def get(self):
        """ Get all products in Stock """
        return {"data": [product.list_product() for product in ModelProducts.query.all()]}

    # @jwt_required
    @required_params(schema)
    @product_space.doc(params=schema)
    def post(self):
        """ Create or Update product.
        For create a new product send a empty string value or send a int id product value for update """

        data = request.json

        product = ModelProducts.find_product(data.get("id"))
        if product:
            return self.put()

        try:

            b64_cover = data.get("cover")

            if b64_cover:
                data["cover"] = upload_image(b64_cover, cover=True)

            product = ModelProducts(**data)
            for images in data.get("images"):
                product.images.append(ModelImagesProduct(
                    upload_image(images), product))

            # Check if category exist
            if not ModelCategoryProduct.find_category(data.get("category")):
                return {"message": "Category id {} not found".format(data.get("category"))}, 400

            lst_provider = []
            for id_provider in data.get("provider"):
                provider = ModelProvider.find_provider(id_provider)
                if not provider:
                    return {"message": "provider id {} not found".format(id_provider)}, 400
                else:
                    lst_provider.append(provider)

            [product.providers.append(provider) for provider in lst_provider]

            product.save_product()

            return {"message": "product created", "data": product.list_product()}, 201
        except Exception as err:
            print(err)
            return {"message": "Internal error"}, 500

        return {"messa": "ok"}, 200

    @jwt_required
    @product_space.hide
    def put(self):
        data = request.json
        product = ModelProducts.find_product(data.get("id"))

        try:
            if data.get("cover"):
                data["cover"] = upload_image(data.get("cover"), cover=True)

            product.update_product(**data)

            for images in data.get("images"):
                product.images.append(ModelImagesProduct(
                    upload_image(images), product))

            product.save_product()
            return {"message": "product updated", "data": product.list_product()}
        except Exception as err:
            print(err)
            return {"message": "internal error"}, 500


@product_space.route("/<int:id_product>")
class ProductGet(Resource):

    def get(self, id_product):
        """ Get Product by id """

        product = ModelProducts.find_product(id_product)

        if product:
            return {"data": product.json_product()}, 200

        return {"message": "product not found"}, 404

    # def get(self, id_product):
    #     """ Get Product by id """

    #     product = ModelProducts.find_product(id_product)

    #     if product:
    #         return {"data": product.list_product()}, 200

    #     return {"message": "product not found"}, 404


@product_space.route("/image/<int:id_image>")
class ProductImage(Resource):

    def delete(self, id_image):
        """ Delete Image of product by id """

        image = ModelImagesProduct.find_image(id_image)

        if image:
            try:
                image.delete_image()

                return {"message": "image deleted"}, 200
            except:
                return {"message": "Internal error"}, 500

        return {"message": "Image not found"}, 404

        return {"message": "Delete Image"}
