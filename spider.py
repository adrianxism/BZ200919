# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，文字匹配
import urllib.request, urllib.error  # 制定URL，获取网页数据
import xlwt  # 进行excel操作
import sqlite3  # 进行SQLite数据库操作


def main():
    baseurl = "https://movie.douban.com/top250?start="
    # 1：爬取网页
    datalist = getData(baseurl)
    savepath = ".\\豆瓣电影Top250.xls"
    # 3：保存数据
    saveData(saveData)


# 爬取网页
def getData(baseurl):
    datalist = []
    # 2：逐一解析数据
    return datalist


def saveData(savepath):
    # 3：保存数据
    print("save...")


if __name__ == "__main__":
    # 调用函数
    main()
