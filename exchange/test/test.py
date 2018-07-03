import sqlite3

conn = sqlite3.connect("PROXIES.db")
cur = conn.cursor()
cur.execute("SELECT  * FROM IPPORT;")


print(cur.fetchall().__len__())
cur.close()
conn.close()