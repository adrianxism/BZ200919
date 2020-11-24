# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，文字匹配
import urllib.request, urllib.error  # 制定URL，获取网页数据
import xlwt  # 进行excel操作
import sqlite3  # 进行SQL


findlink = re.compile(r'<a href="(.*?)">') #创建正则表达式对象，表示规则

def main():
    baseurl = "https://movie.douban.com/top250?start="
    # 1：爬取网页
    datalist = getData(baseurl)
    savepath = ".\\豆瓣电影Top250.xls"
    # 3：保存数据
    # saveData(saveData)

    # askURL("https://movie.douban.com/top250?start=")


# 爬取网页
def getData(baseurl):
    datalist = []
    for i in range(0, 1):
        url = baseurl + str(i*25)
        html = askURL(url)
    # 2：逐一解析数据
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="item"):  #查找符合要求的字符串，形成列表
            data = []   #保存一部电影的所有信息
            item = str(item)

            link = re.findall(findlink, item)[0]    #通过正则表达式查找指定字符串
            print(link)

    return datalist


# 得到一个制定URL
def askURL(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0"
    }

    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)

    return html

# 保存数据
def saveData(savepath):

    print("save...")


if __name__ == "__main__":
    # 调用函数
    main()
