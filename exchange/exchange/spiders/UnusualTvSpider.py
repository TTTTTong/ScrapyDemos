import scrapy
from scrapy import Request
import json
from ..items import UnusualItem
from scrapy.exceptions import CloseSpider


# 爬取行情异动 from tokenview
# todo 因为需要不间断爬取, 所以需要把'https://tokenview.com/api/tx/unusuallist/'加入到scrapy重复请求过滤白名单里
class UnusualTvSpider(scrapy.Spider):
    currency_list = ['mkr']
    name = 'unusual_tokenview'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                             ' Chrome/53.0.2785.143 Safari/537.36', }

    def start_requests(self):
        # 每页50个大额交易记录
        page1_url = 'https://tokenview.com/api/tx/unusuallist/{0}/1/2'
        page2_url = 'https://tokenview.com/api/tx/unusuallist/{0}/2/50'

        for currency in self.currency_list:
            yield Request(url=page1_url.format(currency), headers=self.headers)
            yield Request(url=page2_url.format(currency), headers=self.headers)

    def parse(self, response):
        result = json.loads(response.body)
        if result['code'] == 404:
            return
            # raise CloseSpider('tokenview returned null data')
        currency = result['data']['network']
        data = result['data']['unusualTxs']

        for txs in data:
            item = UnusualItem()
            txs = eval(txs)
            item['currency'] = currency
            item['txid'] = txs['txid']
            item['quantity'] = float(txs['amount'])
            item['time'] = txs['time']
            item['from_addr'] = txs['addr']
            self.is_regal(item)

            # 不同货币的返回格式不同
            if item['txid'].startswith('0x'):
                yield Request(url='http://www.tokenview.com:8088/search/{0}'.format(item['txid']), headers=self.headers,
                              meta={'item': item}, callback=self.parse_outaddr2)
            else:
                yield Request(url='http://www.tokenview.com:8088/search/{0}'.format(item['txid']), headers=self.headers,
                              meta={'item': item}, callback=self.parse_outaddr1)

    def is_regal(self, item):
        # todo
        item['is_regal'] = 1

    # 获取每笔交易的转出地址
    def parse_outaddr1(self, response):
        result_list = json.loads(response.body)['data'][0]['outputs']
        # 有多个转出地址,取值最大的一个
        outaddr = sorted(result_list, key=lambda x: float(x['value']), reverse=True)[0]['address']
        item = response.meta['item']
        item['to_addr'] = outaddr

        yield item

    def parse_outaddr2(self, response):
        to_addr = json.loads(response.body)['data'][0]['to']
        item = response.meta['item']
        item['to_addr'] = to_addr

        yield item
