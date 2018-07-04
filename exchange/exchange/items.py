# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# 大户持币
class RegalHolderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    currency = scrapy.Field()
    rank = scrapy.Field()
    address = scrapy.Field()
    quantity = scrapy.Field()
    per = scrapy.Field()


# 大额转账
class UnusualItem(scrapy.Item):
    currency = scrapy.Field()
    txid = scrapy.Field()
    quantity = scrapy.Field()
    time = scrapy.Field()
    is_regal = scrapy.Field()
    from_addr = scrapy.Field()
    to_addr = scrapy.Field()


class IpItem(scrapy.Item):
    ip = scrapy.Field()


class CurrencyHolderInfoItem(scrapy.Item):
    currency = scrapy.Field()
    holders = scrapy.Field()
    trans = scrapy.Field()
    day_trans = scrapy.Field()
    day_price = scrapy.Field()
    concentration_10 = scrapy.Field()
    concentration_50 = scrapy.Field()
    concentration_100 = scrapy.Field()


# temp
class TokenInfoItem(scrapy.Item):
    currency = scrapy.Field()
    contract = scrapy.Field()
