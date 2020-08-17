# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3

class OfertacasasPipeline(object):
    NameBD = '../MeHouse.db'

    def __init__(self):
        self.conn = sqlite3.connect(self.NameBD)
        self.curr = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS DataHouses""")
        self.curr.execute("""
            CREATE TABLE DataHouses(
            url text,
            location text,
            description text,
            bedrooms text,
            baths text,
            garage text,
            area text,
            price text)
            """)

    def store_db(self, row_tuple):
        self.curr.execute("""
            insert into DataHouses 
            (url,location,description,bedrooms,baths,garage,area,price) 
            values (?,?,?,?,?,?,?,?)
            """, row_tuple)
        self.conn.commit()

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        row_tuple = (
            item['url'],
            item['location'],
            item['description'],
            item['bedrooms'],
            item['baths'],
            item['garage'],
            item['area'],
            item['price']
        )
        self.store_db(row_tuple)
        return item
