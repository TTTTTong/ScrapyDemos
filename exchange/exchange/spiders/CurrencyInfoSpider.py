import scrapy


# 币种信息爬虫
class CurrencyInfoSpider(scrapy.Spider):
    name = 'currency_info'

    def start_requests(self):
        pass

    def parse(self, response):
        pass