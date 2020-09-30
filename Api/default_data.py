# -*- coding: utf-8 -*-


from model.purchase_options import ModelDeliveryStatus, ModelPaymentStatus
from model.products_category import ModelCategoryProduct
from model.products import ModelProducts
from model.provider import ModelProvider


def delivery_data():

    delivery_status = [{
        "id": 1,
        "name": "Pendente",
        "description": "Envio pendente pelo fornecedor"
    },
        {
        "id": 2,
        "name": "Em Trânsito",
        "description": "Produto enviado pelo fornecedor"

    },
        {
        "id": 3,
        "name": "Entregue",
        "description": "Pedido Entregue"
    },
        {
        "id": 4,
        "name": "Cancelado",
        "description": "Envio cancelado pelo fornecedor ou transportadora"
    }
    ]

    for delivery in delivery_status:
        status = ModelDeliveryStatus.find_status(delivery.get("id"))

        if not status:
            status = ModelDeliveryStatus(**delivery)
            status.save_status()

    payment_status = [{
        "id": 1,
        "name": "Pendente",
        "description": "Pagamento Pendente"
    },
        {
        "id": 2,
        "name": "Pago",
        "description": "Pagamento efetuado"
    },
        {
        "id": 3,
        "name": "Cancelado",
        "description": "Pagamento Cancelado"
    }]

    for payment in payment_status:
        status = ModelPaymentStatus.find_status(payment.get("id"))

        if not status:
            status = ModelPaymentStatus(**payment)
            status.save_status()

    category = {
        "id": "1",
        "name": "Categoria Teste",
        "description": ""
    }

    cat = ModelCategoryProduct.find_category(category.get("id"))

    if not cat:
        cat = ModelCategoryProduct(**category)
        cat.save_category()

    provider = {
        "id": "1",
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
    }

    prov = ModelProvider.find_provider(provider.get("id"))

    if not prov:
        provider = ModelProvider(**provider)
        provider.save_provider()

    product = {
        "id": "0",
        "name": "Produto Teste",
        "brand": 1,
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
        "widht": 1.25,
        "maximum_discount": 10.00
    }

    prod = ModelProducts.find_product(product.get("id"))

    if not prod:

        for _ in range(1):
            ModelProducts(**product).save_product()
