'''
Author: Changwei Cao
Date: 2021-11-24 18:40:17
LastEditors: Changwei Cao
LastEditTime: 2021-11-26 14:46:48
Description: Test for Python Clawler
'''

from bs4 import BeautifulSoup
import urllib.request
import re
import xlwt

def main():
    baseurl = "https://movie.douban.com/top250?start="
    # 1. craw the website
    datalist = getData(baseurl=baseurl)
    savepath = "./MovieTop250.xls"

    # 3. record the data
    saveData(datalist=datalist, savepath=savepath)

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
        print("Num %d"%i)
        data = datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])

    book.save(savepath)



if __name__ == "__main__":
    print("------------------")
    main()
    print("Crawler Over")