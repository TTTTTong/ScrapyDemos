import scrapy
from scrapy import Request
import json
from ..items import UnusualItem


# 爬取行情异动 from etherscan
# todo 因为需要不间断爬取, 所以需要把'https://etherscan.io/token/generic-tokentxns2'加入到scrapy重复请求过滤白名单里
class UnusualEsSpider(scrapy.Spider):
    name = 'unusual_etherscan'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                             ' Chrome/53.0.2785.143 Safari/537.36', }

    currency_dict = {'snt': '0x744d70fdbe2ba4cf95131626614a1763df805b9e',
                     'btm': '0xcb97e65f07da24d46bcdd078ebebd7c6e6e3d750'}
    # page1_url = 'https://etherscan.io/token/generic-tokentxns2?contractAddress={0}&a={1}&mode={2}&p={3}'
    start_url = 'http://api.etherscan.io/api?module=account&action=tokentx&address={0}&startblock=0&' \
                'endblock=999999999&sort=desc&apikey=YourApiKeyToken'
    start_url1 = 'https://api.etherscan.io/api?module=account&action=tokentx&contractaddress={0}' \
                 '&page=1&offset=10000&sort=desc&apikey=YourApiKeyToken'

    def start_requests(self):
        for item in self.currency_dict.values():
            yield Request(url=self.start_url1.format(item), headers=self.headers)

    def parse(self, response):
        i = 0
        result = json.loads(response.body)['result']
        for r in result:
            if int(r['value']) > 683994000000000000000000:
                i += 1
        print('===')
        print(i)
        # print(len(result))