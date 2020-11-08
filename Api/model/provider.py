# -*- coding: utf-8 -*-

from datetime import datetime


from db import db


class ModelProvider(db.Model):

    __tablename__ = "provider"

    provider_id = db.Column(db.Integer, primary_key=True)
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
    email = db.Column(db.String(40))
    site = db.Column(db.String(50))
    zip_code = db.Column(db.String(11))
    address = db.Column(db.String(80))
    number = db.Column(db.String(60))
    complement = db.Column(db.String(40))
    neighborhood = db.Column(db.String(80))
    city = db.Column(db.String(80))
    state = db.Column(db.String(2))
    obs = db.Column(db.Text)
    date_register = db.Column(db.DateTime(
        timezone=True), default=datetime.now())
    # register_by = db.Column(
    #     db.Integer, db.ForeignKey("usuario.usuario_id"))
    products = db.relationship('ModelProducts', secondary="providers", lazy='dynamic',
                               backref=db.backref('provider', lazy=True))
    date_update = db.Column(db.DateTime(timezone=True))

    def __repr__(self):
        return "<provider %r>" % self.fancy_name

    def list_provider(self):
        return {
            "id": self.provider_id,
            "fancy_name": self.fancy_name,
            "type_registration": "CPF" if self.type_registration == 1 else "CNPJ",
            "contact_name": self.contact_name,
            "phone": self.phone,
            "email": self.email,
            "enable": self.enable,
            "products": [data.list_product_provider() for data in self.products]
        }

    def list_provider_product(self):
        return {
            "id": self.provider_id,
            "fancy_name": self.fancy_name
        }

    def json_provider(self):
        return {
            "id": self.provider_id,
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
            "site": self.site,
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
                                               self.date_register.year)

        }

    @classmethod
    def find_provider(cls, provider_id):

        if not provider_id:
            return None

        provider = cls.query.filter_by(provider_id=provider_id).first()

        if provider:
            return provider
        return None

    def save_provider(self):
        db.session.add(self)
        db.session.commit()

    def delete_provider(self):
        db.session.delete(self)
        db.session.commit()

    def update_provider(self, enable, type_registration, cnpj, state_registration,
                        municipal_registration,
                        fancy_name, company_name, contact_name, phone, cell_phone,
                        email, site, zip_code, address, number, complement,
                        neighborhood, city, state, obs):
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
        self.site = site
        self.zip_code = zip_code
        self.address = address
        self.number = number
        self.complement = complement
        self.neighborhood = neighborhood
        self.city = city
        self.state = state
        self.obs = obs
        self.date_update = datetime.now()
