# -*- coding: utf-8 -*-

from db import db


class ModelDeliveryStatus(db.Model):
    __tablename__ = 'delivery_status'
    id_status = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(200))

    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description

    def list_delivery_status(self):
        return {
            "id": self.id_status,
            "name": self.name,
            "description": self.description
        }

    @classmethod
    def find_status(cls, id_status):

        if not id_status:
            return None

        status = cls.query.filter_by(id_status=id_status).first()

        if status:
            return status

        return None

    def save_status(self):
        db.session.add(self)
        db.session.commit()

    def update_status(self, id, name, description):
        self.name = name
        self.description = description


class ModelPaymentStatus(db.Model):
    __tablename__ = 'payment_status'
    id_status = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(200))

    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description

    def list_Payment_status(self):
        return {
            "id": self.id_status,
            "name": self.name,
            "description": self.description
        }

    @classmethod
    def find_status(cls, id_status):

        if not id_status:
            return None

        status = cls.query.filter_by(id_status=id_status).first()

        if status:
            return status

        return None

    def save_status(self):
        db.session.add(self)
        db.session.commit()

    def update_status(self, id, name, description):
        self.name = name
        self.description = description


class ModelPaymentForm(db.Model):
    __tablename__ = 'payment_form'
    id_form = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(200))

    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description

    def list_Payment_form(self):
        return {
            "id": self.id_form,
            "name": self.name,
            "description": self.description
        }

    @classmethod
    def find_form(cls, id_form):

        if not id_form:
            return None

        form = cls.query.filter_by(id_form=id_form).first()

        if form:
            return form

        return None

    def save_form(self):
        db.session.add(self)
        db.session.commit()

    def update_form(self, id, name, description):
        self.name = name
        self.description = description


class ModelPaymentMethod(db.Model):
    __tablename__ = 'payment_method'
    id_method = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(200))

    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description

    def list_Payment_method(self):
        return {
            "id": self.id_method,
            "name": self.name,
            "description": self.description
        }

    @classmethod
    def find_method(cls, id_method):

        if not id_method:
            return None

        method = cls.query.filter_by(id_method=id_method).first()

        if method:
            return method

        return None

    def save_method(self):
        db.session.add(self)
        db.session.commit()

    def update_method(self, id, name, description):
        self.name = name
        self.description = description


@db.event.listens_for(ModelDeliveryStatus.__table__, 'after_create')
def initial_delivery_status(*args, **kwargs):
    db.session.add(ModelDeliveryStatus(
        "1", "Pendente", "Envio pendente pelo fornecedor"))
    db.session.add(ModelDeliveryStatus(
        "2", "Em Trânsito", "Produto enviado pelo fornecedor"))
    db.session.add(ModelDeliveryStatus("3", "Entregue", "Pedido Entregue"))
    db.session.commit()


@db.event.listens_for(ModelPaymentForm.__table__, 'after_create')
def initial_payment_form(*args, **kwargs):
    db.session.add(ModelPaymentForm(
        1, "À vista", "Pagamento Efetuado a vista"))
    db.session.add(ModelPaymentForm(2, "Depósito Bancário",
                                    "Pagamento efetuado por meio de depósito bancário"))
    db.session.add(ModelPaymentForm(3, "A Prazo", "Pagamento a prazo"))
    db.session.commit()


@db.event.listens_for(ModelPaymentMethod.__table__, 'after_create')
def initial_payment_method(*args, **kwargs):
    db.session.add(ModelPaymentMethod(
        1, "Dinheiro", "Pagemento efetuado em dinheiro"))
    db.session.add(ModelPaymentMethod(
        2, "Cartão", "Pagemento efetuado em cartão de débito ou crédito"))
    db.session.commit()


@db.event.listens_for(ModelPaymentStatus.__table__, 'after_create')
def initial_payment_status(*args, **kwargs):
    db.session.add(ModelPaymentStatus(1, "Pendente", "Pagamento Pendente"))
    db.session.add(ModelPaymentStatus(2, "Pago", "Pagamento efetuado"))
    db.session.add(ModelPaymentStatus(3, "Cancelado", "Pagamento cancelado"))
    pass
