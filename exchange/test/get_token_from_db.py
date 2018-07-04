# import mysql.connector
# from exchange.exchange import settings
#
#
# cnx = mysql.connector.connect(user=settings.MYSQL_USER, password=settings.MYSQL_PASSWORD,
#                               host=settings.MYSQL_HOSTS, database=settings.MYSQL_DB)
# cur = cnx.cursor()
# sql = " select * from token_info;"
# cur.execute(sql)
# result = cur.fetchall()
# cnx.commit()
#
# for i in result:
#     with open('token_info.txt', 'a+') as f:
#         f.write(i[0] + ':' + i[1] + '\n')
import sys
sys.version_info[0]
