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
    # 到后面请求返回变得很慢，把偏移量变小
    start_url1_big = 'https://api.etherscan.io/api?module=account&action=tokentx&contractaddress={0}' \
                     '&page={1}&offset=500&sort=desc&apikey=YourApiKeyToken'
    # 存储获取每个币交易信息爬取的起始页, 已获取到的大额交易记录, 大额交易的判断量, contract_address, 最近的一次大额交易时间
    currency_dict = {}

    conn = GetDbConn.get_mysqlconn()
    cur = conn.cursor()
    # 获取每个币的价格
    price_sql = "select 24h_price from currency_chain_info WHERE currency='{}'"
    # 获取需要从etherscan上爬取的币
    currency_sql = "SELECT `currency`,`blockchain_pram`  FROM `currency_info` WHERE `blockchain_source` = 2;"
    # 获取最近一次的大额交易时间，每次爬虫到这里就结束，减少请求数量
    time_sql = "SELECT `time`  FROM `unusual`  WHERE `currency` ='{}'  ORDER BY `time` DESC LIMIT 1"
    cur.execute(currency_sql)
    result = cur.fetchall()
    cur.close()

    for currency, addr in result:
        cur = conn.cursor()
        cur.execute(price_sql.format(currency))
        price = cur.fetchone()[0]
        # 定义大额交易的判断量
        big = 50000/price
        # 获取最近一次的大额交易时间
        # todo 改良
        try:
            cur.execute(time_sql.format(currency))
            last_time = cur.fetchone()[0]
        except Exception:
            last_time = 0
        cur.close()
        currency_dict[currency] = [1, 0, big, addr, last_time]
    conn.close()

    def start_requests(self):
        for currency, params in self.currency_dict.items():
            # if currency == 'STORJ':
            #     continue
            yield Request(url=self.start_url1.format(params[3], params[0]), meta={'currency': currency})

    def parse(self, response):
        currency = response.meta['currency']
        result = json.loads(response.body)['result']
        stop_flag = False
        for r in result:
            if int(float(r['value']))/pow(10, int(float(r['tokenDecimal']))) > self.big:
                item = UnusualItem()
                item['currency'] = currency
                item['txid'] = r['hash']
                item['quantity'] = int(r['value'])/pow(10, int(r['tokenDecimal']))
                item['time'] = r['timeStamp']
                item['from_addr'] = r['from']
                item['to_addr'] = r['to']
                self.is_regal(item)
                self.currency_dict[currency][1] += 1
                # 到达上次获取的大额交易时间
                if int(item['time']) < int(self.currency_dict[currency][4]):
                    stop_flag = True
                    break

                yield item

            if self.currency_dict[currency][1] == 100:
                with open('monitor.txt', 'a+') as f:
                    f.write(currency + ':' + str(self.currency_dict[currency][0]) + ' 页 ' + str(
                        self.currency_dict[currency][1]) + '个\n')
                break
        if (self.currency_dict[currency][1] < 100) and (self.currency_dict[currency][0] <= 15) and (not stop_flag):
        # if (self.currency_dict[currency][1] < 100) and (not stop_flag):
            self.currency_dict[currency][0] += 1
            if self.currency_dict[currency][0] > 7:
                yield Request(url=self.start_url1_big.format(self.currency_dict[currency][3], self.currency_dict[currency][0]),
                              meta={'currency': currency}, callback=self.parse)
            else:
                yield Request(url=self.start_url1.format(self.currency_dict[currency][3], self.currency_dict[currency][0]),
                              meta={'currency': currency}, callback=self.parse)

    def is_regal(self, item):
        with open('/srv/node-app/crawl/utils/regal_list.json', 'r') as f:
            regal = json.load(f)
        if item['from_addr'] in regal[item['currency']]:
            item['is_regal'] = 1
        elif item['to_addr'] in regal[item['currency']]:
            item['is_regal'] = 2
        else:
            item['is_regal'] = 0