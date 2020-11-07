# -*- coding: utf-8 -*-

from unittest import TestCase
from app import app
from random import randint


class TestProduct(TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_post_product_return_201_created(self):
        data = {
            "name": "Produto Teste 25 ",
            "brand": 1,
            "category": 1,
            "minimum_sale": 1,
            "internal_code": "abc{}".format(randint(0, 666)),
            "subtract": False,
            "long_description": "",
            "short_description": "Descrição curta do produto",
            "maximum_stock": 30,
            "minimum_stock": 10,
            "sale_price": 10.50,
            "available": True,
            "height": 10,
            "provider": [1],
            "cover": "",
            "unit": 1,
            "images": [],
            "length": 1.5,
            "weight": 0.75,
            "width": 1.25,
            "maximum_discount": 10.00
        }

        response = self.client.post(("/api/v1/admin/products/"), json=data)
        self.assertEqual(201, response.status_code)

    def test_put_product_return_200_updated(self):
        data = {
            "name": "Produto Teste 25 ",
            "brand": 1,
            "category": 1,
            "minimum_sale": 1,
            "internal_code": "abc{}".format(randint(0, 666)),
            "subtract": False,
            "long_description": "",
            "short_description": "Descrição curta do produto",
            "maximum_stock": 30,
            "minimum_stock": 10,
            "sale_price": 10.50,
            "available": True,
            "height": 10,
            "provider": [1],
            "cover": "",
            "unit": 1,
            "images": [],
            "length": 1.5,
            "weight": 0.75,
            "width": 1.25,
            "maximum_discount": 10.00
        }

        response = self.client.put(("/api/v1/admin/products/1"), json=data)
        self.assertEqual(200, response.status_code)

    def test_get_product_by_id_return_200(self):
        response = self.client.get("/api/v1/admin/products/1")
        self.assertEqual(200, response.status_code)

    def test_get_all_products_return_200(self):
        response = self.client.get("/api/v1/admin/products/")
        self.assertEqual(200, response.status_code)

    def test_put_product_return_400_duplicate_internal_code(self):
        data = {
            "name": "Produto Teste 25 ",
            "brand": 1,
            "category": 1,
            "minimum_sale": 1,
            "internal_code": "can123",
            "subtract": False,
            "long_description": "",
            "short_description": "Descrição curta do produto",
            "maximum_stock": 30,
            "minimum_stock": 10,
            "sale_price": 10.50,
            "available": True,
            "height": 10,
            "provider": [1],
            "cover": "",
            "unit": 1,
            "images": [],
            "length": 1.5,
            "weight": 0.75,
            "width": 1.25,
            "maximum_discount": 10.00
        }

        response = self.client.put(("/api/v1/admin/products/1"), json=data)
        self.assertEqual(400, response.status_code)

    def test_put_product_return_400_category_not_found(self):
        data = {
            "name": "Produto Teste 25 ",
            "brand": 1,
            "category": 10,
            "minimum_sale": 1,
            "internal_code": "can123",
            "subtract": False,
            "long_description": "",
            "short_description": "Descrição curta do produto",
            "maximum_stock": 30,
            "minimum_stock": 10,
            "sale_price": 10.50,
            "available": True,
            "height": 10,
            "provider": [1],
            "cover": "",
            "unit": 1,
            "images": [],
            "length": 1.5,
            "weight": 0.75,
            "width": 1.25,
            "maximum_discount": 10.00
        }

        response = self.client.put(("/api/v1/admin/products/1"), json=data)
        self.assertEqual(400, response.status_code)

    def test_put_product_return_400_provider_not_found(self):
        data = {
            "name": "Produto Teste 25 ",
            "brand": 1,
            "category": 10,
            "minimum_sale": 1,
            "internal_code": "can123",
            "subtract": False,
            "long_description": "",
            "short_description": "Descrição curta do produto",
            "maximum_stock": 30,
            "minimum_stock": 10,
            "sale_price": 10.50,
            "available": True,
            "height": 10,
            "provider": [10],
            "cover": "",
            "unit": 1,
            "images": [],
            "length": 1.5,
            "weight": 0.75,
            "width": 1.25,
            "maximum_discount": 10.00
        }

        response = self.client.put(("/api/v1/admin/products/1"), json=data)
        self.assertEqual(400, response.status_code)

    def test_put_product_return_400_invalid_param(self):
        data = {
            "brand": 1,
            "category": 10,
            "minimum_sale": 1,
            "internal_code": "can123",
            "subtract": False,
            "long_description": "",
            "short_description": "Descrição curta do produto",
            "maximum_stock": 30,
            "minimum_stock": 10,
            "sale_price": 10.50,
            "available": True,
            "height": 10,
            "provider": [10],
            "cover": "",
            "unit": 1,
            "images": [],
            "length": 1.5,
            "weight": 0.75,
            "width": 1.25,
            "maximum_discount": 10.00
        }

        response = self.client.put(("/api/v1/admin/products/1"), json=data)
        self.assertEqual(400, response.status_code)

    def test_get_product_by_id_return_404_not_found(self):
        response = self.client.get("/api/v1/admin/products/66666")
        self.assertEqual(404, response.status_code)
