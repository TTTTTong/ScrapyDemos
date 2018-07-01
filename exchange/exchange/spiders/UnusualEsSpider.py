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

    currency_dict = {'snt': '0x744d70fdbe2ba4cf95131626614a1763df805b9e'}
    page1_url = 'https://etherscan.io/token/generic-tokentxns2?contractAddress={0}&a={1}&mode={2}&p={3}'
    start_url = 'http://api.etherscan.io/api?module=account&action=tokentx&address={0}&startblock=0&' \
                'endblock=999999999&sort=asc&apikey=YourApiKeyToken'
    def start_requests(self):
        pass