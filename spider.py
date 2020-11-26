# -*- coding: utf-8 -*-

import re  # 正则表达式，文字匹配
import sqlite3  # 进行SQL
import urllib.error  # 制定URL，获取网页数据
import urllib.request
import xlwt  # 进行excel操作
from bs4 import BeautifulSoup  # 网页解析，获取数据

# 获取影片的规则
findLink = re.compile(r'<a href="(.*?)">')  # 创建正则表达式对象，表示规则
findImage = re.compile(r'<img.*src="(.*?)".*', re.S)  # re.S忽略换行符
findTitle = re.compile(r'<span class="title">(.*?)</span>')
findScore = re.compile(r'<span class="rating_num" property="v:average">(.*?)</span>')
findJudge = re.compile(r'<span>(\d*)人评价</span>')
findInq = re.compile(r'<span class="inq">(.*?)</span>')
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)


def main():
    baseurl = "https://movie.douban.com/top250?start="
    # 1：爬取网页
    datalist = getData(baseurl)
    # savepath = "豆瓣电影Top250.xls"
    dbpath = "movie.db"
    # 3：保存数据
    # saveData(datalist, savepath)
    saveData2DB(datalist, dbpath)

    # askURL("https://movie.douban.com/top250?start=")


# 爬取网页
def getData(baseurl):
    datalist = []  # 所有电影的信息
    for i in range(0, 10):
        url = baseurl + str(i * 25)
        html = askURL(url)
        # 2：逐一解析数据
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="item"):  # 查找符合要求的字符串，形成列表
            data = []  # 保存一部电影的所有信息
            item = str(item)

            # 获取影片详情的超链接
            link = re.findall(findLink, item)[0]  # 通过正则表达式查找指定字符串
            data.append(link)

            image = re.findall(findImage, item)[0]
            data.append(image)

            title = re.findall(findTitle, item)
            if len(title) == 2:
                ctitle = title[0]  # 添加中文名
                data.append(ctitle)
                otitle = title[1].replace("/", "")  # 把/替换成空格
                data.append(otitle)
            else:
                data.append(title[0])
                data.append(' ')  # 如果没有其他名字，就留空

            score = re.findall(findScore, item)[0]
            data.append(score)

            judgeNum = re.findall(findJudge, item)[0]
            data.append(judgeNum)

            inq = re.findall(findInq, item)
            if len(inq) != 0:
                inq = inq[0].replace("。", "")  # 去掉句号
                data.append(inq)
            else:
                data.append(" ")  # 如果没有评论，就留空

            bd = re.findall(findBd, item)[0]
            bd = re.sub('<br(\s+)/>(\s+)', " ", bd)
            bd = re.sub('/', " ", bd)
            data.append(bd.strip())  # 去掉前后空格

            datalist.append(data)
    print(datalist)
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
def saveData(datalist, savepath):
    print("save...")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建对象
    sheet = book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True)  # 创建工作表
    col = ('电影详情链接', '图片链接', '影片中文名', '影片外文名', '评分', '评价数', '概况', '相关信息')

    for i in range(0, 8):
        sheet.write(0, i, col[i])
    for i in range(0, 250):
        print("第%d条" % int(i + 1))
        data = datalist[i]
        for j in range(0, 8):
            sheet.write(i + 1, j, data[j])

    book.save(savepath)


def saveData2DB(datalist, dbpath):
    init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    for data in datalist:
        for index in range(len(data)):
            if index == 4 or index == 5:
                continue
            data[index] = '"' + data[index] + '"'
        sql = '''
            insert into movie250 (
            info_link, pic_info, cname, ename, score, rated, introduction, info)
            values(%s)''' % ",".join(data)
        print(sql)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()


def init_db(dbpath):
    sql = '''
        create table movie250
        (
        id integer primary key autoincrement,
        info_link text,
        pic_link text,
        cname varchar,
        ename varchar,
        score numeric ,
        rated numeric ,
        introduction text,
        info text
        )
    '''  # 创建数据表
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    # 调用函数
    main()
    # init_db("movietest.db")
    print('保存完毕')
