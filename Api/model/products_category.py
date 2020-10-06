# -*- coding: utf-* -*-

from sqlalchemy import event, DDL

from db import db


class ModelCategoryProduct(db.Model):

    __tablename__ = "product_category"
    id_category = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(120))

    __mapper_args__ = {
        "order_by": id_category
    }

    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description

    def list_category(self):
        return {
            "id": self.id_category,
            "name": self.name,
            "description": self.description
        }

    @classmethod
    def find_category(cls, id_category):

        if not id_category:
            return None

        category = cls.query.filter_by(id_category=id_category).first()

        if category:
            return category

        return None

    def save_category(self):
        db.session.add(self)
        db.session.commit()

    def delete_category(self):
        db.session.delete(self)
        db.session.commit()

    def update_category(self, id, name, description):
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
#       "CREATE TRIGGER dt_ins AFTER INSERT ON category "
#     "FOR EACH ROW EXECUTE PROCEDURE my_func();"
# )

# def test1(self):
#     print("Triggor")

# db.event.listen(
#     ModelCategoryProduct.__table__,
#     'after_create',
#     func.execute_if(dialect='postgresql')
# )

# def test2(self):
#     print("Triggor")

# db.event.listen(
#     ModelCategoryProduct.__table__,
#     'after_create',
#     trigger.execute_if(dialect='postgresql')
# )
