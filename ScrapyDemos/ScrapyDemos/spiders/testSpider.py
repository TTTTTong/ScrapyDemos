from scrapy.spiders import Spider


class test_spider(Spider):
    name = 'test'
    start_urls = ['http://woodenrobot.me']

    def parse(self, response):
        title = response.css('span.site-title::text').extract_first()
        print('--------------------')
        print(title)
        print('-------------------')