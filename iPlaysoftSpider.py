import requests
from bs4 import BeautifulSoup

import sys

URL = r'http://www.iplaysoft.com'

def getHTML(url):
    r = requests.get(url)
    return r.content

# 分离内容与导航
def seperateListAndNavi(node):
    postNodes = node.find_all("div", attrs={"class": "entry"})
    naviNode = node.find("div", attrs={"class": "pagenavi-simple"})

    if postNodes and naviNode:
        return (postNodes, naviNode)
    
    return None

# 获取单个内容
def getSingleArticleInfo(node):
    temp = node.div.h2.a
    if temp:
        href = temp["href"]
        title = temp.get_text()
        return (title, href)
    
    return None

# 获取列表
def extractPostListFromHTML(html):
    soup = BeautifulSoup(html, "html.parser")

    body = soup.body
    postBody = body.find("div", attrs={'id': 'section_post'})
    postList = postBody.find("div", attrs={'id': "postlist"})

    return postList

def extractAricalsFromHTML(html):
    postList = extractPostListFromHTML(html)
    contentList, naviSection = seperateListAndNavi(postList)

    articles = []
    for content in contentList:
        article= getSingleArticleInfo(content)
        articles.append(article)

    navis = naviSection.find_all("a")
    navi = navis[-1]
    naviLink = navi['href']
    
    return (articles, naviLink)

def processResultOfAPage(articles):
    for article in articles:
        title, href = article
        print(title + "\n" + href)
        print("\n")

if __name__ == "__main__":
    try:
        pageCount = int(sys.argv[-1])
    except ValueError:
        pageCount = 3
    
    print("Analysing....\n")
    nextLink = URL
    for i in range(0, pageCount):
        html = getHTML(nextLink)
        articles, nextLink = extractAricalsFromHTML(html)

        print("Page %d" % (i+1))
        processResultOfAPage(articles)
    
