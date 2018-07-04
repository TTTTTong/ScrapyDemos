# # !/usr/bin/python
# # -*- coding: utf-8 -*-
# import sys
# if sys.version_info[0] == 3:
#     sys.path.append('/Users/tongxiaoyu/Documents/Work/Code/ScrapyDir/exchange')
# else:
#     sys.path.append('/srv/node-app/crawl/exchange')
# import scrapy
# from scrapy import Request
# from utils import GetDbConn
# import json
# from ..items import CurrencyHolderInfoItem
#
#
# class CurrencyInfoTv(scrapy.Spider):
#     name = 'currency_info_tv'
#     conn = GetDbConn.get_mysqlconn()
#     cur = conn.cursor()
#     sql = "SELECT `currency`,`blockchain_source`,`blockchain_pram` FROM `currency_info` WHERE `blockchain_source` =1;"
#     cur.execute(sql)
#     # (('BCH', 1, 'bch'), ('BTC', 1, 'btc'), ('DASH', 1, 'dash'), ('ETC', 1, 'etc'), ('QTUM', 1, 'qtum_eth'))
#     currency_params = cur.fetchall()
#     cur.close()
#     conn.close()
#     # 获取币种流通量
#     circulation_url = 'https://tokenview.com/api/coin/circulation/{}'
#     # 获取前n%的持币量
#     balanceratio_url = 'https://tokenview.com/api/coin/balanceratio/{}'
#
#     def start_requests(self):
#         for currency in self.currency_params:
#             if currency[2] == 'qtum_eth':
#                 yield Request(url=self.balanceratio_url.format(currency[2]), callback=self.parse_ratio,
#                               meta={'currency': currency[2], 'circulation': 100000000})
#             else:
#                 yield Request(url=self.circulation_url.format(currency[2]), meta={'currency': currency[2]})
#
#     def parse(self, response):
#         circulation = json.loads(response.body)['data']['circulation']
#         currency = response.meta['currency']
#
#         yield Request(url=self.balanceratio_url.format(currency), callback=self.parse_ratio,
#                       meta={'currency': currency, 'circulation': circulation})
#
#     def parse_ratio(self, response):
#         currency = response.meta['currency']
#         circulation = float(response.meta['circulation'])
#         ratios = json.loads(response.body)['data']
#         ratio_10 = ratios['r1To10']/circulation
#         ratio_50 = ratios['r11To50']/circulation + ratio_10
#         ratio_100 = ratios['r51To200']/circulation + ratio_50
#
#         item = CurrencyHolderInfoItem()
#         item['currency'] = currency
#         item['concentration_10'] = ratio_10
#         item['concentration_50'] = ratio_50
#         item['concentration_100'] = ratio_100
#
#         yield item
#
#
#
