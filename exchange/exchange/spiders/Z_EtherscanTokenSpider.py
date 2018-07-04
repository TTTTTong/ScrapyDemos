#!/usr/bin/python
# -*- coding: utf-8 -*-

import scrapy
from scrapy import Request
from bs4 import BeautifulSoup
import re
import random
from ..items import TokenInfoItem


# 爬取etherscan所有tokens
class EtherScanTokenSpider(scrapy.Spider):
    name = 'etherscantoken'
    headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'accept-language': 'zh-CN,zh;q=0.9'}
    start_url = "https://etherscan.io/tokens?p={0}"
    detail_url = "https://etherscan.io{0}"
    #  提取token名字中小括号内的缩写，例如Tronix(TRX)
    # pattern = re.compile(r'[(](.*?)[)]', re.S)

    def start_requests(self):

        for i in range(1, 12):
            yield Request(url=self.start_url.format(i))

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        result = soup.select('tr td.hidden-xs h5 a')
        for i in result:
            href = i.get('href')
            # name = re.findall(self.pattern, i.get_text())[0].lower()

            yield Request(url=self.detail_url.format(href), callback=self.parse_detail, )

    # 获取每个token的contract_address
    def parse_detail(self, response):
        # name = response.meta['name']
        soup = BeautifulSoup(response.body, 'lxml')
        contract = soup.select('td.tditem a')[0].get_text()
        name = soup.select('span.lead-modify')[0].get_text()

        item = TokenInfoItem()
        item['currency'] = name
        item['contract'] = contract

        yield item