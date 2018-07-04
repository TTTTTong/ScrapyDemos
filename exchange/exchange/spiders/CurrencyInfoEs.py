#!/usr/bin/python
# -*- coding: utf-8 -*-

import scrapy
from scrapy import Request
from bs4 import BeautifulSoup
from ..items import CurrencyHolderInfoItem


class CurrencyInfoEsSpider(scrapy.Spider):
    name = 'currency_info_es'
    start_url = 'https://etherscan.io/token/{}'
    # 获取每个币种的总转账笔数
    total_url = 'https://etherscan.io/token/generic-tokentxns2?contractAddress={}&a=&mode='

    def start_requests(self):
        contract_dict = {'Maker': '0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2',
                         # 'DGD': '0xe0b7927c4af23765cb51314a0e0521a9645f0e2a',
                         # 'Golem': '0xa74476443119A942dE498590Fe1f2454d7D4aC0d',
                         # '0chain': '0xb9EF770B6A5e12E45983C5D80545258aA38F3B78',
                         # '0xBitcoin Token': '0xb6ed7644c69416d67b522e20bc294a9a9b405b31',
                         # '1World': '0xfdbc1adc26f0f8f8606a5d63b7d3a3cd21c22b23',
                         # '300Token': '0xaec98a708810414878c3bcdf46aad31ded4a4557',
                         # 'ABYSS': '0x0e8d6b471e332f140e7d9dbb99e5e3822f728da6',
                         # 'Accelerator': '0x13f1b7fdfbe1fc66676d56483e21b1ecb40b58e2',
                         # 'ACE': '0x06147110022b768ba8f99a8f385df11a151a9cc8',
                         # 'AdBank': '0x2baac9330cf9ac479d819195794d79ad0c7616e3',
                         # 'AdEx': '0x4470BB87d77b963A013DB939BE332f927f2b992e',
                         # 'Aditus': '0x8810c63470d38639954c6b41aac545848c46484a',
                         # 'Adshares': '0x422866a8f0b032c5cf1dfbdef31a20f4509562b0',
                         # 'AdToken': '0xd0d6d6c5fe4a677d343cc433536bb717bae167dd',
                         # 'Aeron': '0xBA5F11b16B155792Cf3B2E6880E8706859A8AEB6',
                         # 'Aeternity': '0x5ca9a71b1d01849c0a95490cc00559717fcf0d1d',
        }
        for currency, addr in contract_dict.items():
            yield Request(url=self.start_url.format(addr), meta={'addr': addr})

    def parse(self, response):
        item = CurrencyHolderInfoItem()
        soup = BeautifulSoup(response.body, 'lxml')
        item['currency'] = soup.select('td.tditem')[0].get_text().split()[1]
        item['day_price'] = soup.find('tr', id='ContentPlaceHolder1_tr_valuepertoken').find_all('td')[1].get_text().split()[0].replace('$', '')
        item['holders'] = soup.find('tr', id='ContentPlaceHolder1_tr_tokenHolders').find_all('td')[1].get_text().split()[0]

        yield Request(url=self.total_url.format(response.meta['addr']), callback=self.parse_total, meta={'item': item})

    def parse_total(self, response):
        item = response.meta['item']
        soup = BeautifulSoup(response.body, 'lxml')
        item['trans'] = soup.select('span.hidden-xs')[0].get_text().split()[3]

        print(item)