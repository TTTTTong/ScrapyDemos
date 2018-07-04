from .sql import sql
from exchange.items import RegalHolderItem, UnusualItem, TokenInfoItem, IpItem


class ExchangePipeline:
    def process_item(self, item, spider):

        if isinstance(item, RegalHolderItem):
            sql.insert_regal_holder(item['currency'], item['rank'], item['address'], item['quantity'], item['per'])

        if isinstance(item, UnusualItem):
            sql.insert_unusual(item['currency'], item['txid'], item['quantity'], item['time'],
                             item['is_regal'], item['from_addr'], item['to_addr'])

        if isinstance(item, TokenInfoItem):
            sql.indert_tokeninfo(item['currency'], item['contract'])

        if isinstance(item, IpItem):
            sql.insert_ip(item['ip'])

    def close_spider(self, spider):
        print('eeeeeeeend')


