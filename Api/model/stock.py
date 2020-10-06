# -*- coding: utf-8 -*-

from db import db
from datetime import datetime


class ModelStock(db.Model):
    __tablename__ = 'stock'
    id = db.Column(db.Integer, primary_key=True)
    id_product = db.Column(db.Integer, db.ForeignKey('product.id_product'))
    available_stock = db.Column(db.Float(precision=2), default="0.00")
    purchase_price = db.Column(db.Float(precision=2), default="0.00")
    initial_stock = db.Column(db.Boolean, default=False)


class ModelStockEntry(db.Model):
    __tablename__ = 'stock_entry'
    id = db.Column(db.Integer, primary_key=True)
    id_product = db.Column(db.Integer)
    qtde = db.Column(db.Float(precision=2))
    purchase_price = db.Column(db.Float(precision=2), default=0.00)
    date_entry = db.Column(db.DateTime(timezone=True),
                           server_default=db.func.now())

    def list_entryes(self):
        return {
            "qtde": self.qtde,
            "purchase_price": self.purchase_price
        }


func = db.DDL(
    """
    CREATE OR REPLACE FUNCTION insert_stock()
    RETURNS trigger AS $BODY$
    DECLARE
        old_qtde integer;    

    BEGIN
    IF (TG_OP = 'INSERT') THEN
        SELECT (available_stock) into old_qtde FROM stock WHERE id_product = NEW.id_product;
        UPDATE stock SET available_stock=(old_qtde + NEW.qtde), purchase_price=NEW.purchase_price WHERE id_product = NEW.id_product;
        RETURN NEW;
    
    ELSEIF (TG_OP = 'DELETE') THEN
        SELECT (available_stock) into old_qtde FROM stock WHERE id_product = OLD.id_product;
        UPDATE stock SET available_stock=(old_qtde - OLD.qtde) WHERE id_product = OLD.id_product;
        RETURN OLD;

    END IF;
    
    RETURN NULL;
    END;
    $BODY$ LANGUAGE PLPGSQL
    """
)

trigger = db.DDL(
    """
    CREATE TRIGGER insert_stock
    AFTER INSERT OR DELETE ON stock_entry
    FOR EACH ROW
    EXECUTE PROCEDURE insert_stock();
    """
)

db.event.listen(
    ModelStockEntry.__table__,
    'after_create',
    func.execute_if(dialect='postgresql')
)

db.event.listen(
    ModelStockEntry.__table__,
    "after_create",
    trigger.execute_if(dialect='postgresql')
)
