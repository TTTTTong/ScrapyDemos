import MySQLdb


conn = MySQLdb.connect(host='rm-j6ccb77fan1q3p0n8.mysql.rds.aliyuncs.com',
                       user='rshvip', passwd='Aa112255', db='coindata')
cu = conn.cursor()
sql0 = "SELECT `fullname` from `currency_info`;"
cu.execute(sql0)
re = cu.fetchall()
result = []
for i in re:
    result.append(i[0])
sql = "update currency_info set blockchain_source={0}, blockchain_pram='{1}' WHERE currency='{2}'"

with open('token_info.txt', 'r') as f:
    k = 0
    for i in f:
        if i.split(':')[0] in result:
            print(i)
            k += 1
    print(k)

