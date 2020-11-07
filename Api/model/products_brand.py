# -*- coding: utf-* -*-

from sqlalchemy import event, DDL

from db import db


class ModelBrandProduct(db.Model):

    __tablename__ = "product_brand"
    id_brand = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(120))

    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description

    def list_brand(self):
        return {
            "id": self.id_brand,
            "name": self.name,
            "description": self.description
        }

    @classmethod
    def find_brand(cls, id_brand):

        if not id_brand:
            return None

        brand = cls.query.filter_by(id_brand=id_brand).first()

        if brand:
            return brand

        return None

    def save_brand(self):
        db.session.add(self)
        db.session.commit()

    def delete_brand(self):
        db.session.delete(self)
        db.session.commit()

    def update_brand(self, id, name, description):
        self.name = name
        self.description = description

# mytable = db.Table(
#     'mytable', db.metadata,
#     db.Column('id', db.Integer, primary_key=True),
#     db.Column('data', db.String(50))
# )


# func = db.DDL(
#    "CREATE FUNCTION my_func() "
#     "RETURNS TRIGGER AS $teste_trigger$ "
#     "BEGIN "
#     "INSERT INTO mytable (data) VALUES (NEW.name);"
#     "RETURN NEW; "
#     "END; $teste_trigger$ LANGUAGE PLPGSQL"
# )

# trigger = db.DDL(
#       "CREATE TRIGGER dt_ins AFTER INSERT ON brand "
#     "FOR EACH ROW EXECUTE PROCEDURE my_func();"
# )

# def test1(self):
#     print("Triggor")

# db.event.listen(
#     ModelbrandProduct.__table__,
#     'after_create',
#     func.execute_if(dialect='postgresql')
# )

# def test2(self):
#     print("Triggor")

# db.event.listen(
#     ModelbrandProduct.__table__,
#     'after_create',
#     trigger.execute_if(dialect='postgresql')
# )
