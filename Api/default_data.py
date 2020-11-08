# -*- coding: utf-8 -*-


from model.purchase_options import (ModelDeliveryStatus,
                                    ModelPaymentStatus,
                                    ModelPaymentForm,
                                    ModelPaymentMethod)
from model.products_category import ModelCategoryProduct
from model.products import ModelProducts
from model.provider import ModelProvider
from model.purchase import ModelPurchase, ModelPurchaseItem
from model.products_brand import ModelBrandProduct

from lorem.text import TextLorem
from random import randint


def delivery_data():

    category = [
        {
            "name": "Caneca",
            "description": ""
        },
        {
            "name": "Azulejo",
            "description": ""
        },
        {
            "name": "SmartWatch",
            "description": ""
        },
        {
            "name": "Fone de Ouvido",
            "description": ""
        }
    ]

    for cat in category:
        cate = ModelCategoryProduct.find_category(cat.get("id"))
        if not cate:
            cat = ModelCategoryProduct(**cat)
            cat.save_category()

    brand = [
        {
            "name": "Marca 1",
            "description": ""
        },
        {
            "name": "Azulejo",
            "description": "Marca 2"
        },
        {
            "name": "Marca 3",
            "description": ""
        },
        {
            "name": "Marca 4",
            "description": ""
        }
    ]

    for bran in brand:
        cate = ModelBrandProduct.find_brand(bran.get("id"))
        if not cate:
            cat = ModelBrandProduct(**bran)
            cat.save_brand()

    providers = [{
        "enable": True,
        "type_registration": 2,
        "cnpj": "16897733000100",
        "cell_phone": "22997069161",
        "phone": "",
        "company_name": "Azul e Rosa Teste Update",
        "contact_name": "andre",
        "fancy_name": "AZUl e Rosa",
        "municipal_registration": "",
        "state_registration": "",
        "address": "Rua Major Euclides",
        "city": "Campos dos Goytacazes",
        "complement": "",
        "email": "",
        "neighborhood": "Turf",
        "number": "",
        "obs": "",
        "site": "",
        "state": "RJ",
        "zip_code": "28015161"
    },
        {
        "enable": True,
        "type_registration": 2,
        "cnpj": "16897733000100",
        "cell_phone": "22997069161",
        "phone": "",
        "company_name": "Azul e Rosa Teste Update",
        "contact_name": "andre",
        "fancy_name": "Fornecedor 2",
        "municipal_registration": "",
        "state_registration": "",
        "address": "Rua Major Euclides",
        "city": "Campos dos Goytacazes",
        "complement": "",
        "email": "",
        "neighborhood": "Turf",
        "number": "",
        "obs": "",
        "site": "",
        "state": "RJ",
        "zip_code": "28015161"
    }
    ]

    for provider in providers:
        prov = ModelProvider.find_provider(provider.get("id"))
        if not prov:
            provider = ModelProvider(**provider)
            provider.save_provider()

    product = {
        "internal_code": "acb123",
        "name": "Produto Teste",
        "brand": randint(1, 4),
        "unit": 1,
        "category": 1,
        "long_description": "Descrição longa do produto",
        "short_description": "Descrição curta do produto",
        "maximum_stock": 30,
        "minimum_stock": 10,
        "sale_price": 10.50,
        "available": True,
        "height": 10,
        "provider": [1],
        "cover": "",
        "images": [],
        "length": 1.5,
        "weight": 0.75,
        "width": 1.25,
        "maximum_discount": 10.00,
        "minimum_sale": 1,
        "subtract": False
    }

    prod = ModelProducts.find_product(product.get("id"))

    if not prod:

        for _ in range(1):
            lorem = TextLorem(srange=(1, 2))
            product["name"] = lorem.sentence()
            ModelProducts(**product).save_product()

    purchase = {
        "provider_id": 1,
        "value": 20.10,
        "freight": 1,
        "discount": 0,
        "total_value": 21.1,
        "payment_form": 1,
        "payment_method": 2,
        "delivery_status": 2,
        "parcel": 1,
        "delivery_time": "2017-10-10",
        "obs": "",
        "itens": [
            {
                "id": "",
                "product_id": 1,
                "product_name": "NOme do produto",
                "unit_price": 10.05,
                "qtde": 2,
                "total_price": 20.1,
                "obs": ""
            }
        ]

    }

    for _ in range(1):

        puchase = ModelPurchase(**purchase)

        for item in purchase.get("itens"):
            puchase.itens.append(ModelPurchaseItem(
                **item, id_purchase=puchase, provider_id=purchase.get("provider_id")))
        puchase.save_purchase()
