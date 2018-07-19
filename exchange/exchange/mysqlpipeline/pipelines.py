from .sql import sql
import time
from exchange.items import RegalHolderItem, UnusualItem, TokenInfoItem, IpItem,\
    CurrencyHolderInfoItemEs, CurrencyHolderInfoItemTv


class ExchangePipeline:
    def process_item(self, item, spider):

        if isinstance(item, RegalHolderItem):
            sql.insert_regal_holder(item['currency'], item['rank'], item['address'], item['quantity'], item['per'],
                                    item['exchange'])

        if isinstance(item, UnusualItem):
            sql.insert_unusual(item['currency'], item['txid'], item['quantity'], item['time'],
                               item['is_regal'], item['from_addr'], item['to_addr'], item['from_exchange'],
                               item['to_exchange'])

        if isinstance(item, CurrencyHolderInfoItemEs):
            sql.insert_currency_info_fromes(item['currency'], item['holders'], item['day_price'], item['trans'])

        if isinstance(item, CurrencyHolderInfoItemTv):
            sql.insert_currency_info_fromtv(item['currency'], item['day_price'], item['concentration_10'],
                                            item['concentration_50'], item['concentration_100'])

        if isinstance(item, TokenInfoItem):
            sql.indert_tokeninfo(item['currency'], item['contract'])

        if isinstance(item, IpItem):
            sql.insert_ip(item['ip'])

    def close_spider(self, spider):
        with open('/srv/node-app/crawl/exchange/close_spider.log', 'a+') as f:
            f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ':  ' + spider.name + ' finish\n')

    # def start_spider(self, spider):
    #     print('ssssss')
