import mysql.connector
from ScrapyDemos import settings

cnx = mysql.connector.connect(user=settings.MYSQL_USER, password=settings.MYSQL_PASSWORD, host=settings.MYSQL_HOSTS,
                              database=settings.MYSQL_DB)
cur = cnx.cursor(buffered=True)


class sql:

    @classmethod
    def insert(cls, rank, name, score, score_name):
        sql = 'INSERT INTO douban_top VALUES (%(1)s, %(2)s, %(3)s, %(4)s)'
        params = {'1': rank, '2': name, '3': score, '4': score_name}
        cur.execute(sql, params=params)
        cnx.commit()
