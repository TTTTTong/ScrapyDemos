from scrapy.spiders import Spider
from ..items import DBMovieItem
from scrapy import Request
from bs4 import BeautifulSoup


class DBMovieSpider(Spider):
    name = 'DBMovie'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_requests(self):
        url = 'https://movie.douban.com/top250'
        yield Request(url, headers=self.headers)

    def parse(self, response):
        item = DBMovieItem()
        movie_items = response.css('ol.grid_view li').extract()

        for movie in movie_items:
            soup = BeautifulSoup(movie, 'lxml')
            # soup = BeautifulSoup(movie, 'lxml', from_encoding='gb18030')
            # item['movie_name'] = movie.css('span.title::text').extract_first()
            # item['rankl'] = movie.css('em::text').extract_first()
            # item['score'] = movie.css('span.rating_num::text').extract_first()
            # item['score_num'] = movie.css('div.star span::text').extract_first()
            item['movie_name'] = soup.select_one('span.title').get_text()
            item['rank'] = soup.select_one('em').get_text()
            item['score'] = soup.select_one('span.rating_num').get_text()
            item['score_num'] = soup.select_one('div > div.info > div.bd > div > span:nth-of-type(4)').get_text()

            yield item

        next_url = response.css('div.paginator > span.next > a::attr("href")').extract_first()
        if next_url:
            next_url = response.urljoin(next_url)
            # next_url = 'https://movie.douban.com/top250' + next_url
            # 或者用 response.follow()
            yield Request(next_url, headers=self.headers)
