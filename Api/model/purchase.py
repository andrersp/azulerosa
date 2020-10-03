# -*- coding: utf-8 -*-

from datetime import datetime


from db import db


class ModelPurchase(db.Model):
    __tablename__ = 'purchase'

    id_purchase = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.provider_id'))
    value = db.Column(db.Float(precision=2), default=0.00)
    freight = db.Column(db.Float(precision=2), default=0.00)
    discount = db.Column(db.Float(precision=2), default=0.00)
    total_value = db.Column(db.Float(precision=2))
    delivery_time = db.Column(db.DateTime)
    tracking_cod = db.Column(db.String(20))
    payment_form = db.Column(db.Integer, db.ForeignKey('payment_form.id_form'))
    payment_method = db.Column(
        db.Integer, db.ForeignKey('payment_method.id_method'))
    parcel = db.Column(db.Integer, default=1)
    delivery_status = db.Column(
        db.Integer, db.ForeignKey('delivery_status.id_status'), default=2)
    payment_status = db.Column(db.Integer, db.ForeignKey(
        'payment_status.id_status'), default=1)
    obs = db.Column(db.String(80))
    date = db.Column(db.DateTime, default=datetime.now())
    itens = db.relationship('ModelPurchaseItem',
                            backref='purchase_item', lazy=True)

    provider_name = db.relationship(
        "ModelProvider", foreign_keys=provider_id, lazy='joined')

    delivery_status_name = db.relationship(
        "ModelDeliveryStatus", foreign_keys=delivery_status, lazy='joined')

    # payment_form_name = db.relationship(
    #     'ModelPaymentForm', foreign_keys=payment_form, lazy="joined")
    # payment_method_name = db.relationship(
    #     'ModelPaymentMethod', foreign_keys=payment_method, lazy='joined')

    payment_status_name = db.relationship('ModelPaymentStatus',
                                          foreign_keys=payment_status, lazy='joined')

    __mapper_args__ = {
        "order_by": id_purchase
    }

    def __init__(self, id, provider_id, value, freight, discount, total_value,
                 delivery_time, payment_method, parcel, delivery_status,
                 payment_form,
                 obs, itens):
        self.id = id
        self.provider_id = provider_id
        self.value = value
        self.freight = freight
        self.discount = discount
        self.total_value = total_value
        self.delivery_status = delivery_status
        self.delivery_time = delivery_time
        self.payment_method = payment_method
        self.parcel = parcel
        self.obs = obs
        self.payment_form = payment_form
        # self.itens = itens

    def list_purchases(self):
        return {
            "id": self.id_purchase,
            "provider": self.provider_name.fancy_name,
            "delivery_time": "{}-{}-{}".format(self.delivery_time.day,
                                               self.delivery_time.month,
                                               self.delivery_time.year),
            "delivery_status": self.delivery_status_name.name,
            "payment_status": self.payment_status_name.name,
            "total_value": "%.2f" % (self.total_value)
        }

    def json_purchase(self):
        return {
            "id": self.id_purchase,
            "provider_id": self.provider_id,
            "value": self.value,
            "freight": self.freight,
            "discount": self.discount,
            "total_value": self.total_value,
            "delivery_time": "{}-{}-{}".format(self.delivery_time.day,
                                               self.delivery_time.month,
                                               self.delivery_time.year),
            "tracking_cod": self.tracking_cod if self.tracking_cod else "",
            "payment_form": self.payment_form,
            "payment_method": self.payment_method,
            "parcel": self.parcel,
            "delivery_status": self.delivery_status,
            "payment_status": self.payment_status,
            "obs": self.obs,
            "itens": [item.list_itens() for item in self.itens]
        }

    def save_purchase(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_purchase(cls, id_purchase):

        if not id_purchase:
            return None
        purchase = cls.query.filter_by(id_purchase=id_purchase).first()

        if purchase:
            return purchase

        return None

    def update_purchase(self, id, provider_id, value, freight, discount, total_value,
                        delivery_time, payment_method, parcel, delivery_status,
                        payment_form,
                        obs, itens):
        self.id = id
        self.provider_id = provider_id
        self.value = value
        self.freight = freight
        self.discount = discount
        self.total_value = total_value
        self.delivery_status = delivery_status
        self.delivery_time = delivery_time
        self.payment_method = payment_method
        self.parcel = parcel
        self.obs = obs
        self.payment_form = payment_form

        [item.delete_item() for item in self.itens]

    def update_livery_status(self, status):
        self.delivery_status = status


class ModelPurchaseItem(db.Model):
    __tablename__ = "purchase_item"
    id_item = db.Column(db.Integer, primary_key=True)
    id_purchase = db.Column(db.Integer, db.ForeignKey('purchase.id_purchase'))
    id_product = db.Column(db.Integer, db.ForeignKey(
        'product.id_product'), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.provider_id'))
    unit_price = db.Column(db.Float(precision=2), default=0.00)
    qtde = db.Column(db.Float(precision=2))
    total_price = db.Column(db.Float(precision=2), default=0.00)
    delivery_date = db.Column(db.DateTime)
    obs = db.Column(db.String(120))

    product_name = db.relationship(
        "ModelProducts", backref='product', lazy=True)

    privider_name = db.relationship("ModelProvider",
                                    backref='provider', lazy=True)

    def __init__(self, id_purchase, product_id, unit_price,
                 provider_id,
                 qtde, total_price, obs, **kwargs):
        self.id_purchase = id_purchase
        self.id_product = product_id
        self.unit_price = unit_price
        self.qtde = qtde
        self.provider_id = provider_id
        self.total_price = total_price
        self.obs = obs

    def list_itens(self):
        return {
            "product_id": self.id_product,
            "product_name": self.product_name.name,
            "unit_price": self.unit_price,
            "qtde": self.qtde,
            "total_price": self.total_price,
            "obs": self.obs
        }

    def latest(self):
        return {
            "qtde": self.qtde,
            "unit_price": self.unit_price,
            "provider": self.privider_name.fancy_name,
            "delivery_date": "{}-{}-{}".format(self.delivery_date.year,
                                               self.delivery_date.month, self.delivery_date.day)
        }

    def delete_item(self):
        db.session.delete(self)
        db.session.commit()


""" Trigger """

func = db.DDL(
    """
    CREATE OR REPLACE FUNCTION purchase_audit()
    RETURNS TRIGGER as $TGR_Purchase$
    DECLARE 
        item record;
        old_qtde integer;

    BEGIN

    IF (NEW.delivery_status = 1) THEN
        
        FOR item IN SELECT * FROM purchase_item WHERE id_purchase=NEW.id_purchase
        LOOP

        SELECT (available_stock) into old_qtde FROM product WHERE id_product=item.id_product;
        UPDATE purchase_item SET delivery_date=now() WHERE id_item=item.id_item;
        UPDATE product SET available_stock=(old_qtde + item.qtde), purchase_price=item.unit_price  WHERE id_product=item.id_product;
        
        END LOOP;
    END IF;
    RETURN NEW;
    END; $TGR_Purchase$ LANGUAGE PLPGSQL
    """
)

trigger = db.DDL(
    """
    CREATE TRIGGER purchase_audit
    AFTER INSERT OR UPDATE OR DELETE ON purchase
    FOR EACH ROW
    EXECUTE PROCEDURE purchase_audit();
    """
)

db.event.listen(
    ModelPurchase.__table__,
    "after_create",
    func.execute_if(dialect='postgresql')
)

db.event.listen(
    ModelPurchase.__table__,
    "after_create",
    trigger.execute_if(dialect='postgresql')
)
