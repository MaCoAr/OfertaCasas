# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# import sqlite3
from sqlalchemy.orm import sessionmaker
# from OfertaCasas.OfertaCasas.models import db_connect, create_table, HouseAttributes
# from OfertaCasas.OfertaCasas import models
from . import models

class OfertacasasPipeline(object):
    NameBD = '../MeHouse.db'

    def __init__(self):
        # self.conn = sqlite3.connect(self.NameBD)
        # self.curr = self.conn.cursor()
        # self.create_table()
        """
        Initializes database connection and session maker
        Creates tables
        """
        engine = models.db_connect()
        models.create_table(engine)
        self.Session = sessionmaker(bind=engine)

    # def create_table(self):
    #     self.curr.execute("""DROP TABLE IF EXISTS DataHouses""")
    #     self.curr.execute("""
    #         CREATE TABLE DataHouses(
    #         url text,
    #         location text,
    #         description text,
    #         bedrooms text,
    #         baths text,
    #         garage text,
    #         area text,
    #         price text)
    #         """)

    # def store_db(self, row_tuple):
    #     self.curr.execute("""
    #         insert into DataHouses
    #         (url,location,description,bedrooms,baths,garage,area,price)
    #         values (?,?,?,?,?,?,?,?)
    #         """, row_tuple)
    #     self.conn.commit()

    # def open_spider(self, spider):
    #     pass
    #
    # def close_spider(self, spider):
    #     self.conn.close()

    # def process_item(self, item, spider):
    #     row_tuple = (
    #         item['url'],
    #         item['location'],
    #         item['description'],
    #         item['bedrooms'],
    #         item['baths'],
    #         item['garage'],
    #         item['area'],
    #         item['price']
    #     )
    #     self.store_db(row_tuple)
    #     return item

    def process_item(self, item, spider):
        """Save information in the database
        This method is called for every item pipeline component
        """
        session = self.Session()

        house = models.HouseAttributes()

        house.url = item['url']
        house.location = item['location']
        house.description = item['description']
        house.bedrooms = item['bedrooms']
        house.baths = item['baths']
        house.garage = item['garage']
        house.area = item['area']
        house.price = item['price']

        # # check whether the house exists
        # exits_house = session.query(house).filter_by(url=house.url).first()
        # if exits_house is None:     # The house not exist
        session.add(house)      # Add the house to BD
        session.commit()        # Confirm

        return item
