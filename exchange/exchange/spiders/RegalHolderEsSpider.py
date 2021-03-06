#!/usr/bin/python
# -*- coding: utf-8 -*-

import scrapy
from scrapy import Request
from bs4 import BeautifulSoup
import math
from ..items import RegalHolderItem
import urllib
import sys
if sys.version_info[0] == 3:
    sys.path.append('/Users/tongxiaoyu/Documents/Work/Code/ScrapyDir/exchange')
else:
    sys.path.append('/srv/node-app/crawl/exchange')
from utils import GetDbConn


# 大户持币spider, from etherscan
class RegalHolderEsSpider(scrapy.Spider):
    name = 'regal_holder_etherscan'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                             ' Chrome/53.0.2785.143 Safari/537.36', }
    # 每页50条持币记录,共100条
    page1_url = 'https://etherscan.io/token/generic-tokenholders2?a={0}&s={1}&p=1'
    page2_url = 'https://etherscan.io/token/generic-tokenholders2?a={0}&s={1}&p=2'

    def start_requests(self):
        # 获取每个货币的总发行量和decimals参数的值, 来计算获取持币url中s的值
        baseinfo_url = 'https://etherscan.io/token/{0}'

        conn = GetDbConn.get_mysqlconn()
        cur = conn.cursor()
        # 获取blockchain_source为2的币
        sql = "SELECT `currency`,`blockchain_pram`  FROM `currency_info` WHERE  `blockchain_source` = 2 ;"
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        conn.close()

        for currency_addr in result:
            # print(currency_addr)
            yield Request(url=baseinfo_url.format(currency_addr[1]), headers=self.headers,
                          meta={'currency': currency_addr[0], 'addr': currency_addr[1]},
                          callback=self.parse_baseinfo)

    def parse_baseinfo(self, response):
        currency = response.meta['currency']
        addr = response.meta['addr']
        soup = BeautifulSoup(response.body, 'lxml')
        # 总发行量
        total = soup.select('td.tditem')[0].get_text().split()[0].replace(',', '')
        decimals = soup.select('div.col-md-6 table.table tr td')[14].get_text()
        # todo python2用上面的
        # url中参数s的值 = total_supply * decimals, 之后转义为url编码
        param_s = urllib.quote('{0:.2E}'.format(int(float(total))*math.pow(10, int(decimals))))
        # param_s = urllib.request.quote('{0:.2E}'.format(int(float(total))*math.pow(10, int(decimals))))

        yield Request(url=self.page1_url.format(addr, param_s), headers=self.headers,
                      callback=self.parse_holder, meta={'currency': currency})
        yield Request(url=self.page2_url.format(addr, param_s), headers=self.headers,
                      callback=self.parse_holder, meta={'currency': currency})

    def parse_holder(self, response):
        currency = response.meta['currency']
        soup = BeautifulSoup(response.body, 'lxml')
        item = RegalHolderItem()

        tr_list = soup.find_all('tr')
        for tr in tr_list:
            td_list = tr.find_all('td')
            # 第一行存储的是列属性名
            if len(td_list) == 0:
                continue
            item['currency'] = currency
            item['rank'] = int(td_list[0].get_text())
            item['address'] = td_list[1].a.get_text()
            item['quantity'] = float(td_list[2].get_text())
            # 把百分比形式的字符串转换为浮点数
            item['per'] = float(td_list[3].get_text().strip('%'))/100

            yield item