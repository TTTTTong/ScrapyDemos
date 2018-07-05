#!/usr/bin/python
# -*- coding: utf-8 -*-

import scrapy
from scrapy import Request
from bs4 import BeautifulSoup
from ..items import CurrencyHolderInfoItemEs
import sys
if sys.version_info[0] == 3:
    sys.path.append('/Users/tongxiaoyu/Documents/Work/Code/ScrapyDir/exchange')
else:
    sys.path.append('/srv/node-app/crawl/exchange')
from utils import GetDbConn


class CurrencyInfoEsSpider(scrapy.Spider):
    name = 'currency_info_es'
    start_url = 'https://etherscan.io/token/{}'
    # 获取每个币种的总转账笔数
    total_url = 'https://etherscan.io/token/generic-tokentxns2?contractAddress={}&a=&mode='

    def start_requests(self):
        conn = GetDbConn.get_mysqlconn()
        cur = conn.cursor()
        # 获取blockchain_source为2的币
        sql = "SELECT `currency`,`blockchain_pram`  FROM `currency_info` WHERE  `blockchain_source` = 2 ;"
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        conn.close()

        for currency_addr in result:
            yield Request(url=self.start_url.format(currency_addr[1]),
                          meta={'addr': currency_addr[1], 'name': currency_addr[0]})

    def parse(self, response):
        item = CurrencyHolderInfoItemEs()
        soup = BeautifulSoup(response.body, 'lxml')
        item['currency'] = response.meta['name']
        item['day_price'] = soup.find('tr', id='ContentPlaceHolder1_tr_valuepertoken').find_all('td')[1].get_text().split()[0].replace('$', '')
        item['holders'] = soup.find('tr', id='ContentPlaceHolder1_tr_tokenHolders').find_all('td')[1].get_text().split()[0]

        yield Request(url=self.total_url.format(response.meta['addr']), callback=self.parse_total, meta={'item': item})

    def parse_total(self, response):
        item = response.meta['item']
        soup = BeautifulSoup(response.body, 'lxml')
        item['trans'] = soup.select('span.hidden-xs')[0].get_text().split()[3]

        yield item