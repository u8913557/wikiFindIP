# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 21:23:09 2017

@author: alter
"""

import requests
import random
from bs4 import BeautifulSoup
import urllib
import datetime
import re

user_agents = ['Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+(KHTML, like Gecko) Element Browser 5.0',
               'IBM WebExplorer/v0.94, Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)',
               'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
               'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.02785.143 Safari/537.36']

Connections = ['Keep-Alive']
Accepts = ['text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8']
Accept_Languages = ['zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-CN;q=0.2,ja;q=0.2']
Accept_Encodings = ['gzip, deflate, sdch']

random.seed(datetime.datetime.now())
#index = random.randrange(0, len(user_agents))
index = random.randint(0, len(user_agents)-1)
user_agent = user_agents[index]
Connection = Connections[0]
Accept = Accepts[0]
Accept_Language = Accept_Languages[0]
Accept_Encoding = Accept_Encodings[0]
headers = {'user-agent':user_agent, 'Connection':Connection, 'Accept':Accept,
           'Accept_Language':Accept_Language, 'Accept-Encoding':Accept_Encoding}


#==============================================
def getwebcontent(url, header):
    try:
        res = requests.get(url, headers=header, timeout=1000)
    except requests.exceptions.RequestException as e:
        print(e)
        return None
    return res

def parsewebcontent(content, xml_format):
    try:
        soup = BeautifulSoup(content, xml_format)
    except AttributeError as e:
        print("BeautifulSoup error:" + e)
        return None
    return soup

def getLinks(articleUrl):
    response = getwebcontent("http://en.wikipedia.org"+ articleUrl, headers)
    if response is None:
        print("get wiki Web Site Error")
        return 0
    else:
        response.encoding = 'utf-8'
        soup = parsewebcontent(response.text, "lxml")
        if soup is None:
            print("Parse wiki Web Site Error")
        else:     
            return soup.find("div", {"id":"bodyContent"}).findAll("a",href=re.compile("^(/wiki/)((?!:).)*$"))

def getHistoryIPs(pageUrl):
# 编辑历史页面URL链接格式是：
# http://en.wikipedia.org/w/index.php?title=Title_in_URL&action=history
    pageUrl = pageUrl.replace("/wiki/", "")
    historyUrl = "http://en.wikipedia.org/w/index.php?title="+pageUrl+"&action=history"
    print("history url is: "+ historyUrl)
    response = getwebcontent(historyUrl, headers)
    if response is None:
        print("get history IP Error")
        return 0
    else:
        response.encoding = 'utf-8'
        soup = parsewebcontent(response.text, "lxml")
        if soup is None:
            print("Parse get history IP Error Error")
        else:
# 找出class属性是"mw-anonuserlink"的链接
# 它们用IP地址代替用户名
            ipAddresses = soup.findAll("a", {"class":"mw-anonuserlink"})
            addressList = set()
            for ipAddress in ipAddresses:
                addressList.add(ipAddress.get_text())
                return addressList    
    
links = getLinks("/wiki/Python_(programming_language)")

while(len(links) > 0):
    for link in links:
        print("-------------------")
        historyIPs = getHistoryIPs(link.attrs["href"])
        for historyIP in historyIPs:
            print(historyIP)
   
    newLink = links[random.randint(0, len(links)-1)].attrs["href"]
    links = getLinks(newLink)    