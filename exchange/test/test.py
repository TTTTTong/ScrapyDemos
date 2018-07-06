# import sqlite3
#
# conn = sqlite3.connect("PROXIES.db")
# cur = conn.cursor()
# cur.execute("SELECT  * FROM IPPORT;")
#
#
# print(cur.fetchall().__len__())
# cur.close()
# conn.close()

# import mysql.connector
# from exchange.exchange import settings
#
#
# cnx = mysql.connector.connect(user=settings.MYSQL_USER, password=settings.MYSQL_PASSWORD,
#                               host=settings.MYSQL_HOSTS, database=settings.MYSQL_DB)
# cur = cnx.cursor()
#
# sql2 = "select sum(per) FROM (select per from regal_holder WHERE currency='{}' ORDER BY per DESC  limit 10)a"
# cur.execute(sql2.format('eth'))
# last_trans = cur.fetchone()
# print(last_trans)
# # last_transsql1 = "select holder_count from currency_holder_info WHERE currency='{}'"
# # cur.execute(sql1.format('mkr'))
# # last_trans = cur.fetchone()[0]
# # print(last_trans)
print(9.192083455224705e+25/1e27)