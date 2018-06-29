# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RegalHolderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    currency = scrapy.Field()
    rank = scrapy.Field()
    address = scrapy.Field()
    quantity = scrapy.Field()
    per = scrapy.Field()


class UnusualItem(scrapy.Item):
    currency = scrapy.Field()
    txid = scrapy.Field()
    quantity = scrapy.Field()
    time = scrapy.Field()
    is_regal = scrapy.Field()
    from_addr = scrapy.Field()
    to_addr = scrapy.Field()