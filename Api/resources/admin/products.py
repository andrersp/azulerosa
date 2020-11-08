# -*- coding: utf-8 -*-

from base64 import b64decode
import os
import imghdr
from datetime import datetime
from uuid import uuid4
from PIL import Image
from resizeimage import resizeimage
import io

from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from wraps import required_params

from model.products import ModelProducts
from model.products_image import ModelImagesProduct
from model.provider import ModelProvider
from model.products_category import ModelCategoryProduct
from model.products_brand import ModelBrandProduct
from model.products_unit import ModelProductUnit

schema = {
    "internal_code": {"type": "string", "required": True, "empty": False, "description": "Código interno do produto"},
    "name": {"type": "string", "required": True, "empty": False, "description": "Nome do produto"},
    "category": {"type": "integer", "required": True, "min": 1, "description": "int ID da categoria"},
    "brand": {"type": "integer", "required": True, "description": "int ID da marca ou 0 para nenhuma"},
    "unit": {"type": "integer", "required": True, "min": 1, "description": "int ID Unidade de medida"},
    "minimum_stock": {"type": "float", "required": True, "min": 1, "description": "Float Quantidade mínima em estoque."},
    "maximum_stock": {"type": "float", "required": True, "min": 1, "description": "Float Quantidade máxima em estoque"},
    "subtract": {"type": "boolean", "required": True, "description": "Reduzir estoque ao efetuar venda"},
    "short_description": {"type": "string", "required": True, "empty": False, "description": "Descrição curta do produto, Máximo 200 caracteres ", "maxlength": 200},
    "long_description": {"type": "string", "required": True, "empty": True, "description": "Descrição longa do produto. Aceita HTML"},
    "cover": {"type": "string", "required": True, "empty": True, "description": "Imagem de descate do produto."},
    "height": {"type": "float", "required": True, "description": "Altura da embalagem. "},
    "width": {"type": "float", "required": True, "description": "Largura da embalagem"},
    "length": {"type": "float", "required": True, "description": "Comprimento da embalagem"},
    "weight": {"type": "float", "required": True, "description": "Peso da embalagem"},
    "minimum_sale": {"type": "float", "required": True, "min": 1, "description": "Float Quantidade mínima de venda."},
    "sale_price": {"type": "float", "required": True, "description": "Float valor de venda."},
    "maximum_discount": {"type": "float", "required": True, "description": "Float porcentagem desconto máximo"},
    "available": {"type": "boolean", "required": True, "description": "Se produto esta disponível"},
    "images": {"type": "list", "schema": {"type": "string"}, "required": True, "empty": True, "description": "List com as imagens codificadas em base64"},
    "provider": {"type": "list", "schema": {"type": "integer", "required": True}, "required": True, "empty": True, "description": "List com ID de fornecedores deste produto"}
}


# Function to converte base64 image to file

def upload_image(image, cover=False):

    image = b64decode(image.encode())
    extension = imghdr.what(None, h=image)
    filename = str(uuid4()) + "." + extension

    pic = io.BytesIO(image)
    with Image.open(pic) as image_pil:
        cover = resizeimage.resize_height(image_pil, 600, validate=False)
        cover.save("static/images/{}".format(filename), image_pil.format)

    return filename


class ProductApi(MethodView):

    def get(self, product_id):

        if product_id is None:

            data = ModelProducts.list_product()
            return jsonify({"data": data}), 200

        product = ModelProducts.find_product(product_id)

        if not product:
            return jsonify({"message": "Product not found"}), 404

        return jsonify({"data": product.get_product()}), 200

    @required_params(schema)
    def post(self):
        """ Adicionar ou editar produto.
        Para criar envie string vazia em id e para editar envie um int com o ID do produto"""

        data = request.json

        product_code = ModelProducts.find_internal_code(
            data.get("internal_code"))
        if product_code:
            return jsonify({"message": "Product Code in use to other product"}), 400

        # Check if category exist
        if not ModelCategoryProduct.find_category(data.get("category")):
            return jsonify({"message": "Category id {} not found".format(data.get("category"))}), 400

        # Check if provider exist
        lst_provider = []

        for id_provider in data.get("provider"):
            provider = ModelProvider.find_provider(id_provider)
            if not provider:
                return jsonify({"message": "provider id {} not found".format(id_provider)}), 400

            lst_provider.append(provider)

        try:

            b64_cover = data.get("cover")

            if b64_cover:
                data["cover"] = upload_image(b64_cover)

            product = ModelProducts(**data)

            # Appending Images
            for images in data.get("images"):
                product.images.append(ModelImagesProduct(
                    upload_image(images), product))

            # Appending provider

            [product.providers.append(provider) for provider in lst_provider]

            # Save Product
            product.save_product()

            return jsonify({"message": "product created", "data": product.get_product()}), 201

        except Exception as err:
            print(err)

            return jsonify({"message": "Internal error"}), 500

    @required_params(schema)
    def put(self, product_id):

        data = request.json

        product = ModelProducts.find_product(product_id)

        # Check if category exist
        if not ModelCategoryProduct.find_category(data.get("category")):
            return jsonify({"message": "Category id {} not found".format(data.get("category"))}), 400

        # Check if provider exist
        lst_provider = []
        for id_provider in data.get("provider"):
            provider = ModelProvider.find_provider(id_provider)
            if not provider:
                return jsonify({"message": "provider id {} not found".format(id_provider)}), 400

            lst_provider.append(provider)

        product_code = ModelProducts.find_internal_code(
            data.get("internal_code"))

        if product_code:
            if len(product_code) > 1:
                return jsonify({"message": "Product Code in use to other product"}), 400
            if product_code[0] != int(product_id):
                return jsonify({"message": "Product Code in use to other product"}), 400

        try:
            if data.get("cover"):
                data["cover"] = upload_image(data.get("cover"))

            product.update_product(**data)
            # Appending Images
            for images in data.get("images"):
                product.images.append(ModelImagesProduct(
                    upload_image(images), product))

            # Appending provider
            [product.providers.append(provider) for provider in lst_provider]

            # Save Prodict
            product.save_product()

            return jsonify({"message": "Product Updated", "data": product.get_product()}), 200
        except Exception as err:
            print(err)
            return {"message": "internal error"}, 500

    def delete(self, image_id):
        """ 
        Deletar imagem por ID do produto e ID da Imagem.
        """

        image = ModelImagesProduct.find_image(image_id)

        if image:
            try:
                image.delete_image()
                return jsonify({"message": "Image deleted!"}), 200

            except:
                return jsonify({"message": "Internal Error"})

        return jsonify({"message": "Image not found"}), 404


class ProductSelect(MethodView):

    def get(self):
        """ Itens Cadastro de Produto
        Lista contendo todos os itens necessários para cadastro de produto """

        providers = ModelProvider.list_provider_product()

        categories = [category.list_category()
                      for category in ModelCategoryProduct.query.all()]

        units = [unit.json_units() for unit in ModelProductUnit.query.all()]

        brands = [brand.list_brand()
                  for brand in ModelBrandProduct.query.all()]

        return {"data": {"providers": providers, "categories": categories, "brands": brands,  "units": units}}, 200
