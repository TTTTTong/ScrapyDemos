# import MySQLdb
# todo
import mysql.connector
from .. import settings


cnx = mysql.connector.connect(user=settings.MYSQL_USER, password=settings.MYSQL_PASSWORD, host=settings.MYSQL_HOSTS,
                              database=settings.MYSQL_DB)
cur = cnx.cursor()


class sql:
    @classmethod
    def insert(cls, currency, rank, address, quantity, per):
        sql = "insert into regal_holder values('{0}',{1},'{2}',{3},{4}) on duplicate key " \
              "update address='{2}',quantity={3},per={4};"
        cur.execute(sql.format(currency, rank, address, quantity, per))
        cnx.commit()