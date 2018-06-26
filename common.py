# -*- coding: utf-8 -*-

import ccxt, time,datetime ,json,pytz,os,pickle
from decimal import Decimal
#import sqlite3
import pymysql
from config import *
from email.mime.text import MIMEText
from email.utils import formataddr
import smtplib

tz = pytz.timezone('Asia/Shanghai')

#conn = sqlite3.connect(DB)
conn =pymysql.connect(DBHOST,DBUSER, DBPASS, DB)

c = conn.cursor()
try:
    c.execute('''CREATE TABLE t_gbi 
      (dt   DATETIME   NOT NULL,
       davg DECIMAL(40,30) NOT NULL,
       lastdata DECIMAL(40,30) NOT NULL);
     ''')
    c.execute('''CREATE INDEX idx_gbi ON t_gbi(dt DESC);
      ''')
except:
    pass
try:
    c.execute('''CREATE TABLE t_qtum_order
      (id CHAR(20) PRIMARY KEY     NOT NULL,
       dt   DATETIME   NOT NULL,
       symbol  CHAR(30)   NOT NULL,
       side    CHAR(10) NOT NULL,
       amount DECIMAL(40,30) NOT NULL,
       filled DECIMAL(40,30) NOT NULL,
       process  BOOLEAN NOT NULL);''')
    conn.commit()

except:
    pass

try:
    c.execute('''CREATE TABLE t_eos_order
      (id CHAR(20) PRIMARY KEY     NOT NULL,
       dt   DATETIME   NOT NULL,
       symbol  CHAR(30)   NOT NULL,
       side    CHAR(10) NOT NULL,
       amount DECIMAL(40,30) NOT NULL,
       filled DECIMAL(40,30) NOT NULL,
       process  BOOLEAN NOT NULL);''')
    conn.commit()

except:
    pass

try:
    c.execute('''CREATE TABLE t_neo_order
      (id CHAR(20) PRIMARY KEY     NOT NULL,
       dt   DATETIME   NOT NULL,
       symbol  CHAR(30)   NOT NULL,
       side    CHAR(10) NOT NULL,
       amount DECIMAL(40,30) NOT NULL,
       filled DECIMAL(40,30) NOT NULL,
       process  BOOLEAN NOT NULL);''')
    conn.commit()

except:
    pass


try:
    c.execute('''CREATE TABLE t_eth_order
      (id CHAR(20) PRIMARY KEY     NOT NULL,
       dt   DATETIME   NOT NULL,
       symbol  CHAR(30)   NOT NULL,
       side    CHAR(10) NOT NULL,
       amount DECIMAL(40,30) NOT NULL,
       filled DECIMAL(40,30) NOT NULL,
       process  BOOLEAN NOT NULL);''')
    conn.commit()

except:
    pass

try:
    c.execute('''CREATE TABLE t_xrp_order
      (id CHAR(20) PRIMARY KEY     NOT NULL,
       dt   DATETIME   NOT NULL,
       symbol  CHAR(30)   NOT NULL,
       side    CHAR(10) NOT NULL,
       amount DECIMAL(40,30) NOT NULL,
       filled DECIMAL(40,30) NOT NULL,
       process  BOOLEAN NOT NULL);''')
    conn.commit()

except:
    pass
conn.close()


def opensqlconn():
    conn = pymysql.connect(DBHOST, DBUSER, DBPASS, DB)
    return conn

def login():
    exchange = ccxt.huobipro()
    exchange.apiKey = ACCKEY
    exchange.secret = SECKEY
    return exchange

    # balance=exchange.fetch_balance()['info']['data']['list']


# for i in balance:
#    if i['currency'] == 'usdt' and i['type'] == 'trade':
#       print('可用USDT:'+i['balance'])


def getdatetime():
    dt=datetime.datetime.now(tz).isoformat()
    return dt


my_sender = 'cljqqyx@qq.com'  # 发件人邮箱账号
my_pass = 'clj19880729'  # 发件人邮箱密码
my_user = '15002080574@139.com'  # 收件人邮箱账号，我这边发送给自己

def mail(content, subject):
    ret = True
    try:
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = formataddr(["FromRunoob", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["FK", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = subject  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret

def checkbalance():
    exchange = login()
    balance = exchange.fetch_balance()
    leftusdt = Decimal(balance['USDT']['free'])
    mf = os.getcwd() + '/leftmailed'
    if not os.path.exists(mf):
        f = open(mf, 'wb')
        pickle.dump(None, f)
        f.close()
    f = open(mf, 'rb')
    maildate = pickle.load(f)
    f.close()
    if leftusdt < Decimal(LEFTUSDT) and maildate != datetime.date.today():
        ret = mail('USDT数量少于'+str(LEFTUSDT), 'HB余额不足')
    if ret:
        f = open(mf, 'wb')
        pickle.dump(datetime.date.today(), f)
        f.close()


if __name__ == '__main__':
    checkbalance()
