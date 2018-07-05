#!/usr/bin/python
# -*- coding: utf-8 -*-

import scrapy
from scrapy import Request
import json
from ..items import RegalHolderItem
import sys
if sys.version_info[0] == 3:
    sys.path.append('/Users/tongxiaoyu/Documents/Work/Code/ScrapyDir/exchange')
else:
    sys.path.append('/srv/node-app/crawl/exchange')
from utils import GetDbConn


# 大户持币spider, from tokenview
class RegalHolderTvSpider(scrapy.Spider):

    name = 'regal_holder_tokenview'
    # 获取前100个持币大户信息
    hold_url = 'https://tokenview.com/api/address/richrange/{0}/1/100'
    # 获取币种的流通量, 因为tokenview只返回quantity不返回百分比,需要自己计算
    total_url = 'https://tokenview.com/api/coin/circulation/{0}'

    def start_requests(self):
        conn = GetDbConn.get_mysqlconn()
        cur = conn.cursor()
        # 获取blockchain_source为1的币
        sql = "SELECT `currency`,`blockchain_pram` FROM `currency_info` WHERE `blockchain_source` = 1;"
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        conn.close()

        for currency in result:
            # QTUM的返回数据和其他不同，特殊处理
            if currency[1] == 'qtum_eth':
                yield Request(url=self.hold_url.format(currency[1]), callback=self.parse_holder,
                              meta={'currency': currency[0], 'circulation': 100000000})
            else:
                yield Request(url=self.total_url.format(currency[1]), callback=self.parse_circulation,
                              meta={'currency': currency[0]})

    # 获取币种流通量
    def parse_circulation(self, response):
        currency = response.meta['currency']
        result = json.loads(response.body)
        data = result['data']
        circulation = float(data['circulation'])

        yield Request(url=self.hold_url.format(currency),
                      callback=self.parse_holder, meta={'currency': currency, 'circulation': circulation})

    # 获取持币榜
    def parse_holder(self, response):
        currency = response.meta['currency']
        circulation = response.meta['circulation']
        result = json.loads(response.body)
        data = result['data']
        item = RegalHolderItem()

        rank = 1
        for value in data:
            # 数据格式 address:quantity
            for addr, quantity in value.items():
                # todo
                item['currency'] = currency
                item['rank'] = rank
                item['address'] = addr
                item['quantity'] = quantity
                item['per'] = round(quantity/circulation, 6)
                yield item
            rank += 1
