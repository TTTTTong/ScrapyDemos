from .sql import sql
from exchange.items import RegalHolderItem


class ExchangePipeline:
    def process_item(self, item, spider):
        if isinstance(item, RegalHolderItem):
            sql.insert(item['currency'], item['rank'], item['address'], item['quantity'], item['per'])