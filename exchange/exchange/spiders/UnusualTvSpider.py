import scrapy
from scrapy import Request


# 爬取行情异动 from tokenview
class UnusualTvSpider(scrapy.Spider):
    curency_list = ['btc', 'eth']
    name = 'Unusual_tokenview'

    def start_requests(self):
        start_url = 'https://tokenview.com/api/tx/unusuallist/btc/1/50'
        start_url = 'https://tokenview.com/api/tx/unusuallist/btc/2/50'

