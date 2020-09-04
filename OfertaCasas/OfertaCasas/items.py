# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class OfertacasasItems(scrapy.Item):
    # define the fields for your item here like:

    # General
    house_id = scrapy.Field()
    url = scrapy.Field()
    # Filters
    location = scrapy.Field()
    description = scrapy.Field()
    bedrooms = scrapy.Field()
    baths = scrapy.Field()
    garage = scrapy.Field()
    area = scrapy.Field()
    price = scrapy.Field()
    images = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()

    # Others Filters
    land_1 = scrapy.Field()
    land_2 = scrapy.Field()
    built_1 = scrapy.Field()
    built_2 = scrapy.Field()
    garage_1 = scrapy.Field()
    garage_2 = scrapy.Field()
    seller = scrapy.Field()
    real_estate = scrapy.Field()
    year_construction_1 = scrapy.Field()
    year_construction_2 = scrapy.Field()

