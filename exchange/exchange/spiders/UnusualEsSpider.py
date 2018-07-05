#!/usr/bin/python
# -*- coding: utf-8 -*-

import scrapy
from scrapy import Request
import json
from ..items import UnusualItem
import sys
if sys.version_info[0] == 3:
    sys.path.append('/Users/tongxiaoyu/Documents/Work/Code/ScrapyDir/exchange')
else:
    sys.path.append('/srv/node-app/crawl/exchange')
from utils import GetDbConn


# 爬取行情异动 from etherscan
# todo 因为不间断爬取, 需要把'https://etherscan.io/token/generic-tokentxns2'加入到scrapy重复请求过滤白名单里
class UnusualEsSpider(scrapy.Spider):
    name = 'unusual_etherscan'
    # 获取某个币种的交易信息
    start_url1 = 'https://api.etherscan.io/api?module=account&action=tokentx&contractaddress={0}' \
                 '&page={1}&offset=3000&sort=desc&apikey=YourApiKeyToken'
    # 存储获取每个币交易信息爬取的起始页, 已获取到的大额交易记录, 大额交易的判断量, contract_address
    currency_dict = {}

    conn = GetDbConn.get_mysqlconn()
    cur = conn.cursor()
    # 获取每个币的价格
    price_sql = "select 24h_price from currency_holder_info WHERE currency='{}'"
    # 获取需要从etherscan上爬取的币
    currency_sql = "SELECT `currency`,`blockchain_pram`  FROM `currency_info` WHERE `blockchain_source` = 2;"
    cur.execute(currency_sql)
    result = cur.fetchall()
    cur.close()
    for currency, addr in result:
        cur = conn.cursor()
        cur.execute(price_sql.format(currency))
        price = cur.fetchone()[0]
        # 定义大额交易的判断量
        big = 50000/price
        cur.close()
        currency_dict[currency] = [1, 0, big, addr]
    conn.close()

    def start_requests(self):
        for currency, params in self.currency_dict.items():
            if currency == 'STORJ':
                continue
            yield Request(url=self.start_url1.format(params[3], params[0]), meta={'currency': currency})

    def parse(self, response):
        currency = response.meta['currency']
        result = json.loads(response.body)['result']
        # 只获取100条
        for r in result:
            if int(r['value'])/pow(10, int(r['tokenDecimal'])) > self.big:
                item = UnusualItem()
                item['currency'] = currency
                item['txid'] = r['hash']
                item['quantity'] = int(r['value'])/pow(10, int(r['tokenDecimal']))
                item['time'] = r['timeStamp']
                # todo 判断大户
                item['is_regal'] = 0
                item['from_addr'] = r['from']
                item['to_addr'] = r['to']
                self.currency_dict[currency][1] += 1

                yield item

            if self.currency_dict[currency][1] == 100:
                break
        if self.currency_dict[currency][1] < 100:
            self.currency_dict[currency][0] += 1

            yield Request(url=self.start_url1.format(self.currency_dict[currency][3], self.currency_dict[currency][0]),
                          meta={'currency': currency}, callback=self.parse)