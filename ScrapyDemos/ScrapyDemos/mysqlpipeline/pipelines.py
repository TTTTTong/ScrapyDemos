from .sql import sql
from ScrapyDemos.items import DBMovieItem


class DoubanPipeline:
    def process_item(self, item, spider):
        if isinstance(item, DBMovieItem):
            sql.insert(item['rank'], item['movie_name'], item['score'], item['score_num'])
            print('保存了第：' + item['rank'])
