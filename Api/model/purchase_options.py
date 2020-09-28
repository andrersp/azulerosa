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