# -*- coding: utf-8 -*-


from model.purchase_options import ModelDeliveryStatus, ModelPaymentStatus


def delivery_data():

    delivery_status = [{
        "id": 1,
        "name": "Entregue",
        "description": "Pedido Entregue"
    },
    {
        "id": 2,
        "name": "Pendente",
        "description": "Envio pendente pelo fornecedor"        
    },
    {
        "id": 3,
        "name": "Cancelado",
        "description": "Entrega cancelada pela transportadora / Fornecedor"        
    }]


    for delivery in delivery_status:
        status = ModelDeliveryStatus.find_status(delivery.get("id"))

        if not status:
            status = ModelDeliveryStatus(**delivery)
            status.save_status()
    

    payment_status = [{
        "id": 1,
        "name": "Pago",
        "description": "Pagamento efetuado"
    },
    {
        "id": 2,
        "name": "Pendente",
        "description": "Pagamento Pendente"
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