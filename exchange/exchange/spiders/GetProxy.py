import re
from fake_useragent import UserAgent
import scrapy
from scrapy import Request
from bs4 import BeautifulSoup
from ..items import IpItem
from requests import get


class GetProxy(scrapy.Spider):
    name = 'get_proxy'
    start_url1 = 'https://www.kuaidaili.com/free/inha/{0}/'
    start_url2 = 'http://www.xicidaili.com/nn/{0}'

    def start_requests(self):
        for i in range(1, 50):
            yield Request(url=self.start_url1.format(i))
            yield Request(url=self.start_url2.format(i), callback=self.parse2)

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        tr_list = soup.select('tr')
        for tr in tr_list[1::]:
            item = IpItem()
            tdlist = tr.select('td')
            item['ip'] = tdlist[0].get_text() + ':' + tdlist[1].get_text()

            # self.verify_ip(item)
            ua = UserAgent()
            try:
                url_content = get("https://www.baidu.com/",
                                  proxies={"http": item['ip'], "https": item['ip']},
                                  timeout=10,
                                  headers={
                                      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                      'Accept-Encoding': 'gzip, deflate, compress',
                                      'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ru;q=0.4',
                                      'Cache-Control': 'max-age=0',
                                      'Connection': 'keep-alive',
                                      'User-Agent': ua.random
                                  })

                if int(url_content.status_code) == int(200):
                    yield item

            except BaseException as e:
                pass

    def parse2(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        taglist = soup.find_all('tr', attrs={'class': re.compile("(odd)|()")})
        for trtag in taglist:
            item = IpItem()
            tdlist = trtag.find_all('td')
            item['ip'] = tdlist[1].string + ':' + tdlist[2].string

            # self.verify_ip(item)
            ua = UserAgent()
            try:
                url_content = get("https://www.baidu.com/",
                                  proxies={"http": item['ip'], "https": item['ip']},
                                  timeout=10,
                                  headers={
                                      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                      'Accept-Encoding': 'gzip, deflate, compress',
                                      'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ru;q=0.4',
                                      'Cache-Control': 'max-age=0',
                                      'Connection': 'keep-alive',
                                      'User-Agent': ua.random
                                  })

                if int(url_content.status_code) == int(200):
                    yield item

            except BaseException as e:
                pass

    # 检测获取的代理IP是否可用
    def verify_ip(self, item):
        ua = UserAgent()
        try:
            url_content = get("https://www.baidu.com/",
                              proxies={"http": item['ip'], "https": item['ip']},
                              timeout=10,
                              headers={
                                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                  'Accept-Encoding': 'gzip, deflate, compress',
                                  'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ru;q=0.4',
                                  'Cache-Control': 'max-age=0',
                                  'Connection': 'keep-alive',
                                  'User-Agent': ua.random
                              })

            if int(url_content.status_code) == int(200):
                yield item

        except BaseException as e:
            pass

