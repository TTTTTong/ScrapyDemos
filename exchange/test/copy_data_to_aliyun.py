
import MySQLdb

conn = MySQLdb.connect(host='rm-j6ccb77fan1q3p0n8.mysql.rds.aliyuncs.com',
                       user='rshvip', passwd='Aa112255', db='coindata')
cu = conn.cursor()
sql0 = "SELECT `fullname` from `currency_info`;"
cu.execute(sql0)
re = cu.fetchall()
cu.close()
conn.close()
result = []
for i in re:
    result.append(i[0])
# print(result)
sql = "update currency_info set blockchain_source={0}, blockchain_pram='{1}' WHERE currency='{2}'"
# sql = "insert into currency_info VALUES (blockchain_source={0}, blockchain_pram='{1}') WHERE currency='{2}'"

with open('token_info.txt', 'r') as f:
    k = 0
    for i in f:
        # print(i.split(':')[0])
        if i.split(':')[0] in result:
            conn = conn = MySQLdb.connect(host='rm-j6ccb77fan1q3p0n8.mysql.rds.aliyuncs.com',
                       user='rshvip', passwd='Aa112255', db='coindata')
            cu = conn.cursor()
            cu.execute(sql.format(2, i.split(':')[1].strip('\n'), i.split(':')[0]))
            print('insert', i.strip('\n'))
            cu.close()
            conn.commit()
            conn.close()
            k += 1
    print(k)
