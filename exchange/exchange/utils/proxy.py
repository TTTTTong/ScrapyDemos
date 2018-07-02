import mysql.connector
# from exchange import settings
from exchange.exchange import settings

cnx = mysql.connector.connect(user=settings.MYSQL_USER, password=settings.MYSQL_PASSWORD,
                              host=settings.MYSQL_HOSTS, database=settings.MYSQL_DB)
cur = cnx.cursor()


sql = "select * from ip_list;"
cur.execute(sql)
result = cur.fetchall()
for row in result:
    with open('ip_list.txt', 'a') as f:
        f.write(row[0] + ':' + row[1] + '\n')
