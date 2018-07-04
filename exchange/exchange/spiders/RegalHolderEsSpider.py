#!/usr/bin/python
# -*- coding: utf-8 -*-

import scrapy
from scrapy import Request
from bs4 import BeautifulSoup
import math
from ..items import RegalHolderItem
import urllib


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

        # todo 从文件读取
        contract_dict = {'Maker': '0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2',
                         'DGD': '0xe0b7927c4af23765cb51314a0e0521a9645f0e2a',
                         'Golem': '0xa74476443119A942dE498590Fe1f2454d7D4aC0d',
                         '0chain': '0xb9EF770B6A5e12E45983C5D80545258aA38F3B78',
                         '0xBitcoin Token': '0xb6ed7644c69416d67b522e20bc294a9a9b405b31',
                         '1World': '0xfdbc1adc26f0f8f8606a5d63b7d3a3cd21c22b23',
                         '300Token': '0xaec98a708810414878c3bcdf46aad31ded4a4557',
                         'ABYSS': '0x0e8d6b471e332f140e7d9dbb99e5e3822f728da6',
                         'Accelerator': '0x13f1b7fdfbe1fc66676d56483e21b1ecb40b58e2',
                         'ACE': '0x06147110022b768ba8f99a8f385df11a151a9cc8',
                         'AdBank': '0x2baac9330cf9ac479d819195794d79ad0c7616e3',
                         'AdEx': '0x4470BB87d77b963A013DB939BE332f927f2b992e',
                         'Aditus': '0x8810c63470d38639954c6b41aac545848c46484a',
                         'Adshares': '0x422866a8f0b032c5cf1dfbdef31a20f4509562b0',
                         'AdToken': '0xd0d6d6c5fe4a677d343cc433536bb717bae167dd',
                         'Aeron': '0xBA5F11b16B155792Cf3B2E6880E8706859A8AEB6',
                         'Aeternity': '0x5ca9a71b1d01849c0a95490cc00559717fcf0d1d',
        }

        for currency, addr in contract_dict.items():
            yield Request(url=baseinfo_url.format(addr), headers=self.headers, meta={'currency': currency, 'addr': addr},
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
        # param_s = urllib.quote('{0:.2E}'.format(int(total)*math.pow(10, int(decimals))))
        param_s = urllib.request.quote('{0:.2E}'.format(int(float(total))*math.pow(10, int(decimals))))

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