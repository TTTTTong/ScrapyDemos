# !/usr/bin/python
# -*- coding: utf-8 -*-

import sys


class sql:
    if sys.version_info[0] == 3:
        @classmethod
        def get_conn(cls):
            import mysql.connector
            sys.path.append('/Users/tongxiaoyu/Documents/Work/Code/ScrapyDir/exchange')
            from exchange import settings
            conn = mysql.connector.connect(user=settings.MYSQL_USER, password=settings.MYSQL_PASSWORD,
                                      host=settings.MYSQL_HOSTS, database=settings.MYSQL_DB)
            return conn
    else:
        @classmethod
        def get_conn(cls):
            import MySQLdb
            conn = MySQLdb.connect(host='rm-j6ccb77fan1q3p0n8.mysql.rds.aliyuncs.com', user='rshvip', passwd='Aa112255',
                                  db='coindata')
            return conn

    @classmethod
    def insert_regal_holder(cls, currency, rank, address, quantity, per):
        sql = "insert into regal_holder values('{0}',{1},'{2}',{3},{4}) on duplicate key " \
              "update address='{2}',quantity={3},per={4};"
        conn = cls.get_conn()
        cur = conn.cursor()
        cur.execute(sql.format(currency, rank, address, quantity, per))
        conn.commit()
        cur.close()
        conn.close

    @classmethod
    def insert_unusual(cls, currency, txid, quantity, time, is_regal, from_addr, to_addr):
        sql = "insert into unusual VALUES('{0}', '{1}', {2}, {3}, {4}, '{5}', '{6}') ON duplicate KEY " \
              "UPDATE quantity={2},time={3},is_regal={4},from_addr='{5}',to_addr='{6}';"
        conn = cls.get_conn()
        cur = conn.cursor()
        cur.execute(sql.format(currency, txid, quantity, time, is_regal, from_addr, to_addr))
        conn.commit()
        cur.close()
        conn.close

    @classmethod
    def indert_tokeninfo(cls, currency, contract):
        sql = "insert into token_info VALUES('{0}', '{1}') ON duplicate KEY UPDATE contract='{1}';"
        conn = cls.get_conn()
        cur = conn.cursor()
        cur.execute(sql.format(currency, contract))
        conn.commit()
        cur.close()
        conn.close

    @classmethod
    def insert_ip(cls, ip):
        sql = "insert into ip_list VALUES('{0}') ON duplicate KEY UPDATE ip='{0}';"
        conn = cls.get_conn()
        cur = conn.cursor()
        cur.execute(sql.format(ip))
        conn.commit()
        cur.close()
        conn.close

    @classmethod
    def insert_currency_info_fromes(cls, name, holders, day_price, trans):
        # 查询上次转账总数
        sql1 = "select trans_count from currency_holder_info WHERE currency='{}'"
        conn = cls.get_conn()
        cur = conn.cursor()
        cur.execute(sql1.format(name))
        try:
            last_trans = cur.fetchone()[0]
        except TypeError:
            last_trans = 0
        day_trans = int(trans)-last_trans
        # 查询持币集中度
        sql_10 = "select sum(per) FROM (select per from regal_holder WHERE currency='{}' ORDER BY per DESC  limit 10) a"
        sql_50 = "select sum(per) FROM (select per from regal_holder WHERE currency='{}' ORDER BY per DESC  limit 50) a"
        sql_100= "select sum(per) FROM (select per from regal_holder WHERE currency='{}' ORDER BY per DESC  limit 100)a"
        cur.execute(sql_10.format(name))
        concentration_10 = cur.fetchone()[0]
        cur.execute(sql_50.format(name))
        concentration_50 = cur.fetchone()[0]
        cur.execute(sql_100.format(name))
        concentration_100 = cur.fetchone()[0]

        sql3 = "insert into currency_holder_info VALUES ('{0}',{1},{2},{3},{4},{5},{6},{7})ON duplicate KEY UPDATE " \
               "holder_count={1}, trans_count={2},24h_trans={3}, 24h_price={4},concentration_10={5}," \
               "concentration_50={6},concentration_100={7}"
        conn = cls.get_conn()
        cur = conn.cursor()
        cur.execute(sql3.format(name, holders, trans, day_trans, day_price, concentration_10, concentration_50, concentration_100))
        conn.commit()
        cur.close()
        conn.close

    @classmethod
    def insert_currency_info_fromtv(cls, name, day_price, concentration_10, concentration_50, concentration_100):
        query_sql = "select * from `currency_holder_info` where `currency`='{}'"
        try:
            conn = cls.get_conn()
            cur = conn.cursor()
            cur.execute(query_sql.format(name))
            if cur.fetchone() is not None:
                update_sql = "update currency_holder_info set 24h_price={0}, concentration_10={1}, " \
                             "concentration_50={2}, concentration_100={3} WHERE currency='{4}'"
                cur.execute(update_sql.format(day_price, concentration_10, concentration_50, concentration_100, name))
                conn.commit()
                cur.close()
                conn.close
            else:
                insert_sql = "insert into currency_holder_info VALUES ('{0}',0,0,0,{1},{2},{3},{4})"
                cur.execute(insert_sql.format(name, day_price, concentration_10, concentration_50, concentration_100))
                conn.commit()
                cur.close()
                conn.close
        # todo 有问题
        except Exception:
            conn = cls.get_conn()
            cur = conn.cursor()
            insert_sql = "insert into currency_holder_info VALUES ('{0}',0,0,0,{1},{2},{3},{4})"
            cur.execute(insert_sql.format(name, day_price, concentration_10, concentration_50, concentration_100))
            conn.commit()
            cur.close()
            conn.close