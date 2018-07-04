# !/usr/bin/python
# -*- coding: utf-8 -*-
# import MySQLdb
# todo
import mysql.connector
from .. import settings


cnx = mysql.connector.connect(user=settings.MYSQL_USER, password=settings.MYSQL_PASSWORD,
                              host=settings.MYSQL_HOSTS, database=settings.MYSQL_DB)
cur = cnx.cursor()


class sql:
    @classmethod
    def insert_regal_holder(cls, currency, rank, address, quantity, per):
        sql = "insert into regal_holder values('{0}',{1},'{2}',{3},{4}) on duplicate key " \
              "update address='{2}',quantity={3},per={4};"
        cur.execute(sql.format(currency, rank, address, quantity, per))
        cnx.commit()

    @classmethod
    def insert_unusual(cls, currency, txid, quantity, time, is_regal, from_addr, to_addr):
        sql = "insert into unusual VALUES('{0}', '{1}', {2}, {3}, {4}, '{5}', '{6}') ON duplicate KEY " \
              "UPDATE quantity={2},time={3},is_regal={4},from_addr='{5}',to_addr='{6}';"
        cur.execute(sql.format(currency, txid, quantity, time, is_regal, from_addr, to_addr))
        cnx.commit()

    @classmethod
    def indert_tokeninfo(cls, currency, contract):
        sql = "insert into token_info VALUES('{0}', '{1}') ON duplicate KEY UPDATE contract='{1}';"
        cur.execute(sql.format(currency, contract))
        cnx.commit()

    @classmethod
    def insert_ip(cls, ip):
        sql = "insert into ip_list VALUES('{0}') ON duplicate KEY UPDATE ip='{0}';"
        cur.execute(sql.format(ip))
        cnx.commit()

    @classmethod
    def insert_currency_info_fromes(cls, name, holders, trans):
        # 查询上次转账总数
        sql1 = "select trans_count from currency_holder_info WHERE currency='{}'"
        cur.execute(sql1.format(name))
        last_trans = cur.fetchone()[0]
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

        sql3 = "insert into currency_holder_info VALUES ('{0}',{1},{2},{3},{4},{5},{6},{7},'{8}')"
        cur.execute(sql3.format(name, holders, trans, trans-last_trans, concentration_10, concentration_50,
                                concentration_100))
        cnx.commit()

    # @classmethod
    # def insert_currency_info_fromtv(cls, ):
