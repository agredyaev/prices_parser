from peewee import *
from confing import Config

db = PostgresqlDatabase(database=Config.DATABASE_NAME,
                        user=Config.USER_NAME,
                        password=Config.PASS,
                        host=Config.HOST
                        )


class Offers(Model):
    create_date = CharField(11)
    location = CharField(20)
    retailer = CharField(40)
    group = CharField(40)
    category = CharField(40)
    subcategory = CharField(40)
    item_description = TextField()
    price_new = CharField(15)
    price_old = CharField(15)
    discount = CharField(20)
    qty = CharField(40)
    dates = CharField(40)

    class Meta:
        database = db


FIELDS = [
    Offers.create_date,
    Offers.location,
    Offers.retailer,
    Offers.group,
    Offers.category,
    Offers.subcategory,
    Offers.item_description,
    Offers.price_new,
    Offers.price_old,
    Offers.discount,
    Offers.qty,
    Offers.dates]
