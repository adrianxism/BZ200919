#-*- codeing = utf-8 -*-
#@Time : 2020/11/25 20:51
#@Author : Lixiang
#@File : testSqlite.py
#@Software : PyCharm


import sqlite3

conn = sqlite3.connect("test.db")    #打开或创建数据库文件

print("Opened database successfully")