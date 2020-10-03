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
