#!/usr/bin/python
# -*- coding: utf-8 -*-

import scrapy
from scrapy import Request
from bs4 import BeautifulSoup
import re
from ..items import CurrencyHolderInfoItemEs


# 废弃  只能获取到530个
# 爬取etherscan所有tokens
class CurrencyInfoEsSpider(scrapy.Spider):
    name = 'currencyinfoes'
    headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'accept-language': 'zh-CN,zh;q=0.9'}
    start_url = "https://etherscan.io/tokens?p={0}"
    detail_url = "https://etherscan.io{0}"
    #  提取token名字中小括号内的缩写，例如Tronix(TRX)
    pattern = re.compile(r'[(](.*?)[)]', re.S)

    def start_requests(self):

        # for i in range(1, 12):
        yield Request(url=self.start_url.format(1))

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        result = soup.select('tr td.hidden-xs h5 a')
        for i in result:
            href = i.get('href')
            name = re.findall(self.pattern, i.get_text())[0].lower()

            yield Request(url=self.detail_url.format(href), callback=self.parse_detail, meta={'name': name})

    # 获取每个token的contract_address
    def parse_detail(self, response):
        name = response.meta['name']
        soup = BeautifulSoup(response.body, 'lxml')
        contract = soup.select('td.tditem a')[0].get_text()
        holders = soup.select('table.table tr')[3].select('td')[1].get_text().split()[0]
        transfers = soup.select('table.table tr')[4].select('td')[1].get_text()

        item = CurrencyHolderInfoItemEs()
        item['currency'] = name
        item['holders'] = holders
        item['trans'] = transfers
        item['blockchain_source'] = 2
        item['blockchain_pram'] = contract
        #
        # print(item)
        # yield item
