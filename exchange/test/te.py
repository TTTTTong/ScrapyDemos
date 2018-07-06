import sys


if sys.version_info[0] == 3:
    import mysql.connector
    sys.path.append('/Users/tongxiaoyu/Documents/Work/Code/ScrapyDir/exchange')
    from exchange import settings

    def get_mysqlconn():
        cnx = mysql.connector.connect(user=settings.MYSQL_USER, password=settings.MYSQL_PASSWORD,
                                      host=settings.MYSQL_HOSTS, database=settings.MYSQL_DB)
        return cnx
else:
    import MySQLdb

    def get_mysqlconn():
        conn = MySQLdb.connect(host='rm-j6ccb77fan1q3p0n8.mysql.rds.aliyuncs.com',
                               user='rshvip', passwd='Aa112255', db='coindata')
        return conn


cnx = get_mysqlconn()
cur = cnx.cursor()

sql = "SELECT DISTINCT(`currency`) FROM `unusual`"
cur.execute(sql)
alread = cur.fetchall()

sql3 = "SELECT `currency`    FROM `currency_info` WHERE `blockchain_source` =2;"
cur.execute(sql3)
all_li = cur.fetchall()

print(set(all_li).difference(alread))