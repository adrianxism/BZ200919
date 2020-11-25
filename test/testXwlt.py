#-*- codeing = utf-8 -*-
#@Time : 2020/11/25 14:08
#@Author : Lixiang
#@File : testXwlt.py
#@Software : PyCharm


import xlwt
'''
workbook = xlwt.Workbook(encoding="utf-8")    #创建workbook对象
worksheet = workbook.add_sheet('sheet1')    #创建工作表
worksheet.write(0, 0, 'hello')    #写数据，第一个参数表示行，第二个参数表示列，第三个参数表示内容
workbook.save('student.xls')
'''

workbook = xlwt.Workbook(encoding="utf-8")    #创建workbook对象
worksheet = workbook.add_sheet('sheet1')    #创建工作表
for j in range(0,9):
    for i in range(0,j+1):
        worksheet.write(i, j, "%d *%d = %d"%(i+1, j+1, (i+1)*(j+1)))

workbook.save('student.xls')