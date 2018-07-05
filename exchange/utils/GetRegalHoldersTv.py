import json
import sys
if sys.version_info[0] == 3:
    sys.path.append('/Users/tongxiaoyu/Documents/Work/Code/ScrapyDir/exchange')
else:
    sys.path.append('/srv/node-app/crawl')
from utils import GetDbConn

result_dict = {}

sql = "SELECT `currency`  FROM `currency_info` WHERE `blockchain_source` !=0"
conn = GetDbConn.get_mysqlconn()
cur = conn.cursor()
cur.execute(sql)
currency_list = cur.fetchall()
cur.close()

select_holders_sql = "select address from regal_holder WHERE currency='{}'"
for currency in currency_list:
    cur = conn.cursor()
    cur.execute(select_holders_sql.format(currency[0]))
    address_list = []
    for address in cur.fetchall():
        address_list.append(address[0])
    cur.close()
    result_dict[currency[0]] = address_list


with open('regal_list.json', 'w') as f:
    json.dump(result_dict, f)