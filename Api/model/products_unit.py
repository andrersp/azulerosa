# -*- coding: utf-8 -*-

from db import db


class ModelProductUnit(db.Model):
    __tablename__ = 'product_unit'
    id_unit = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(120))

    def __repr__(self):
        return "<Unit %r>" % self.name

    @classmethod
    def find_unit(cls, id_unit):
        if not id_unit:
            return None
        unit = cls.query.filter_by(id_unit=id_unit).first()

        if unit:
            return unit

        return None

    @classmethod
    def find_unit_name(cls, name):

        unit = cls.query.filter_by(name=name).all()

        units = [data.id_unit for data in unit]

        if unit:
            return units
        return None

    # Return List Units json
    def json_units(self):
        return {
            "id": self.id_unit,
            "name": self.name,
            "description": self.description
        }

    def save_unit(self):
        db.session.add(self)
        db.session.commit()

    def delete_unit(self):
        db.sesstion.delete(self)
        db.session.commit()

    def update_unit(self, name, description):
        self.name = name
        self.description = description


@db.event.listens_for(ModelProductUnit.__table__, 'after_create')
def inicial_units(*args, **kwargs):
    db.session.add(ModelProductUnit(name="UN", description=""))
    db.session.add(ModelProductUnit(name="KG", description=""))
    db.session.add(ModelProductUnit(name="CX", description=""))
    db.session.commit()
