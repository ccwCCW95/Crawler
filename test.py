'''
Author: Changwei Cao
Date: 2021-11-24 18:40:17
LastEditors: Changwei Cao
LastEditTime: 2021-11-26 15:44:20
Description: Test for Python Clawler
'''

from bs4 import BeautifulSoup
import urllib.request
import re
import xlwt
import sqlite3

def main():
    baseurl = "https://movie.douban.com/top250?start="
    # 1. craw the website
    datalist = getData(baseurl=baseurl)
    savepath = "./MovieTop250.xls"
    dbpath = "Movie.db"

    # 3. record the data
    saveData(datalist=datalist, savepath=savepath)

    saveData2DB(datalist,dbpath)

findlink = re.compile(r'<a href="(.*?)">')
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)
findTitle = re.compile(r'<span class="title">(.*)</span>')
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findJudge = re.compile(r'<span>(\d*)人评价</span>')
findInq = re.compile(r'<span class="inq">(.*)</span>')
findBd = re.compile(r'<p class="">(.*?)</p>',re.S)

'''
description: Get the data from url and prase them
param {*} baseurl
return {*}
author: Changwei Cao
'''
def getData(baseurl):
    datalist = []

    for i in range(0,10):
        url = baseurl + str(i * 25)
        html = askURL(url)

        # 2. Parse the data from url
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_ = "item"):
            # print(item)
            data = []
            item = str(item)

            link = re.findall(findlink, item)[0]
            data.append(link)

            imgSrc = re.findall(findImgSrc, item)[0]
            data.append(imgSrc)

            titles = re.findall(findTitle, item)
            if len(titles) == 2:
                ctitle = titles[0]
                data.append(ctitle)
                otitle = titles[1].replace("/", "")
                data.append(otitle)
            else:
                data.append(titles[0])
                data.append(' ')

            rating = re.findall(findRating, item)[0]
            data.append(rating)

            judgeNum = re.findall(findJudge, item)[0]
            data.append(judgeNum)

            inq = re.findall(findInq, item)
            if len(inq) != 0:
                inq = inq[0].replace("。", "")
                data.append(inq)
            else:
                data.append(' ')

            bd = re.findall(findBd, item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?', " ", bd)
            bd = re.sub('/', " ", bd)
            data.append(bd.strip())

            datalist.append(data)

    return datalist


'''
description: Get the content from a specific url
param {*} url
return {*}
author: Changwei Cao
'''
def askURL(url):
    head = {
       "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36" 
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

'''
description: Save the data to the Excel
param {*} datalist
param {*} savepath
return {*}
author: Changwei Cao
'''
def saveData(datalist, savepath):
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = book.add_sheet('MovieTop250', cell_overwrite_ok=True)
    col = ("MovieDetails","ImgLink","Chinese Name","English Name","Score","ScoreNum","Abstract","Related Info")

    for i in range(0,8):
        sheet.write(0,i,col[i])

    for i in range(0,250):
        # print("Num %d"%i)
        data = datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])

    book.save(savepath)

'''
description: Save the data to the database
param {*} datalist
param {*} dbpath
return {*}
author: Changwei Cao
'''
def saveData2DB(datalist, dbpath):
    init_db(dbpath=dbpath)

    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    for data in datalist:
        for index in range(len(data)):
            if index == 4 or index == 5:
                continue
            data[index] = '"' + data[index] + '"'

        sql = '''
            
                insert into movie250 (
                    info_link,pic_link,cname,ename,score,rated,introduction,info)

                values(%s)
            
        '''%",".join(data)

        cur.execute(sql)
        conn.commit()
    
    cur.close()
    conn.close()

'''
description: Initialize the database
param {*} dbpath
return {*}
author: Changwei Cao
'''
def init_db(dbpath):
    sql = '''
    
       create table movie250 
       (
           id integer primary key autoincrement,
           info_link text,
           pic_link text,
           cname varchar,
           ename varchar,
           score numeric,
           rated numeric,
           introduction text,
           info text
       ) 
    
    '''

    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()



if __name__ == "__main__":
    print("------------------")
    main()
    print("Crawler Over")