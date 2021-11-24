from bs4 import BeautifulSoup
import urllib.request

def main():
    baseurl = "https://movie.douban.com/top250?start="
    # 1. craw the website
    # datalist = getData(baseurl=baseurl)


def getData(baseurl):
    datalist = []

    for i in range(0,10):
        url = baseurl + str(i * 25)
        html = askURL(url)

        # 2. Parse the data from url
        

# Get the content from a specific url
def askURL(url):
    head = {
       "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36" 
    }

    request = urllib.request.Request(url, headers=head)
    html = ""

    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)

    return html



if __name__ == "__main__":
    print("------------------")
    main()