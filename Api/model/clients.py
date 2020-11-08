# -*- coding: utf-8 -*-

from datetime import datetime

from flask_jwt_extended import get_jwt_identity


from db import db


class ModelClient(db.Model):

    __tablename__ = "client"

    client_id = db.Column(db.Integer, primary_key=True)
    enable = db.Column(db.Boolean, default=True)
    type_registration = db.Column(db.Integer)
    cnpj = db.Column(db.String(20))
    state_registration = db.Column(db.String(20))
    municipal_registration = db.Column(db.String(12))
    fancy_name = db.Column(db.String(80))
    company_name = db.Column(db.String(80))
    contact_name = db.Column(db.String(40))
    phone = db.Column(db.String(80))
    cell_phone = db.Column(db.String(12))
    email = db.Column(db.String(50))
    zip_code = db.Column(db.String(11))
    address = db.Column(db.String(80))
    number = db.Column(db.String(60))
    complement = db.Column(db.String(40))
    neighborhood = db.Column(db.String(80))
    city = db.Column(db.String(80))
    state = db.Column(db.String(2))
    obs = db.Column(db.Text)
    date_register = db.Column(db.DateTime, server_default=db.func.now())
    register_by = db.Column(db.Integer)
    salesman = db.Column(db.Integer)
    notify = db.Column(db.Boolean)
    date_update = db.Column(db.DateTime)
    delivery_address = db.relationship(
        "ModelDelivereAdrressClient", backref='addresses', lazy="joined")

    def __repr__(self):
        return "<client %r>" % self.fancy_name

    def __init__(self,  delivery_address, **kwargs):
        super(ModelClient, self).__init__(**kwargs)

    def list_client(self):
        return {
            "id": self.client_id,
            "fancy_name": self.fancy_name,
            "type_registration": "CPF" if self.type_registration == 1 else "CNPJ",
            "contact_name": self.contact_name,
            "phone": self.phone,
            "email": self.email,
            "enable": self.enable

        }

    def json_client(self):
        return {
            "client_id": self.client_id,
            "enable": self.enable,
            "type_registration": self.type_registration,
            "cnpj": self.cnpj,
            "state_registration": self.state_registration,
            "municipal_registration": self.municipal_registration,
            "fancy_name": self.fancy_name,
            "company_name": self.company_name,
            "contact_name": self.contact_name,
            "phone": self.phone,
            "cell_phone": self.cell_phone,
            "email": self.email,
            "zip_code": self.zip_code,
            "address": self.address,
            "number": self.number,
            "complement": self.complement,
            "neighborhood": self.neighborhood,
            "city": self.city,
            "state": self.state,
            "obs": self.obs,
            "date_register": "{}-{}-{}".format(self.date_register.day,
                                               self.date_register.month,
                                               self.date_register.year),
            "notify": self.notify,
            "delivery_address": [address.list_address() for address in self.delivery_address]
            # "cadastrado_por": self.cadastrado_por,
            # "produtos": [products.lista_json() for products in self.products]
        }

    @classmethod
    def find_client(cls, client_id):

        if not client_id:
            return None

        client = cls.query.filter_by(client_id=client_id).first()

        if client:
            return client
        return None

    def save_client(self):
        db.session.add(self)
        db.session.commit()

    def delete_client(self):
        db.session.delete(self)
        db.session.commit()

    def update_client(self, enable, type_registration, cnpj, state_registration,
                      municipal_registration,
                      fancy_name, company_name, contact_name, phone, cell_phone,
                      email, zip_code, address, number, complement,
                      neighborhood, city, state, obs, notify, **kwargs):
        self.id = id
        self.enable = enable
        self.type_registration = type_registration
        self.cnpj = cnpj
        self.state_registration = state_registration
        self.municipal_registration = municipal_registration
        self.fancy_name = fancy_name
        self.company_name = company_name
        self.contact_name = contact_name
        self.phone = phone
        self.cell_phone = cell_phone
        self.email = email
        self.zip_code = zip_code
        self.address = address
        self.number = number
        self.complement = complement
        self.neighborhood = neighborhood
        self.city = city
        self.state = state
        self.obs = obs
        self.date_update = datetime.now()
        self.notify = notify


class ModelDelivereAdrressClient(db.Model):

    __tablename__ = "delivery_address_cliente"
    id = db.Column(db.Integer, primary_key=True)
    zip_code = db.Column(db.String(8))
    address = db.Column(db.String(80))
    number = db.Column(db.String(60))
    complement = db.Column(db.String(40))
    neighborhood = db.Column(db.String(80))
    city = db.Column(db.String(80))
    state = db.Column(db.String(2))
    current = db.Column(db.Boolean)
    client = db.Column(db.Integer, db.ForeignKey(
        "client.client_id"), nullable=False)

    def list_address(self):
        return {
            "id": self.id,
            "zip_code": self.zip_code,
            "address": self.address,
            "number": self.number,
            "complement": self.complement,
            "neighborhood": self.neighborhood,
            "city": self.city,
            "state": self.state,
            "current": self.current
        }

    @classmethod
    def find_address(cls, id_address):

        if not id_address:
            return False

        address = cls.query.filter_by(id=id_address).first()

        if address:
            return address

        return None

    def save_address(self):
        db.session.add(self)
        db.session.commit()

    def delete_address(self):
        db.session.delete(self)
        db.session.commit()

    def update_address(self, zip_code, address, number, complement, neighborhood,
                       city, state, current):
        self.zip_code = zip_code
        self.address = address
        self.number = number
        self.complement = complement
        self.neighborhood = neighborhood
        self.state = state
        self.current = current
        self.city = city
