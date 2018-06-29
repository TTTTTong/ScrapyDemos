import scrapy
from scrapy import Request
import json
from ..items import RegalHolderItem


# 大户持币spider, from tokenview
class RegalHolderTvSpider(scrapy.Spider):

    name = 'regal_holder_tokenview'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                             ' Chrome/53.0.2785.143 Safari/537.36', }
    # 获取前100个持币大户信息
    hold_url = 'https://tokenview.com/api/address/richrange/{0}/1/100'

    def start_requests(self):
        # 获取币种的流通量, 因为tokenview只返回quantity不返回百分比,需要自己计算
        total_url = 'https://tokenview.com/api/coin/circulation/{0}'

        # todo  读取文件的currency
        curency_list = ['btc', 'eth']
        for currency in curency_list:
            yield Request(url=total_url.format(currency), headers=self.headers,
                          callback=self.parse_circulation, meta={'currency': currency})

    # 获取币种流通量
    def parse_circulation(self, response):
        currency = response.meta['currency']
        result = json.loads(response.body)
        data = result['data']
        circulation = float(data['circulation'])

        yield Request(url=self.hold_url.format(currency), headers=self.headers,
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
