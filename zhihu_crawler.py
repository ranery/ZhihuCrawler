# -*- coding: utf-8 -*-
"""
Created on 26/10/2017
@author : Haoran You

"""

import login
import URL
import requests
import http.cookiejar as cookielib
import urllib
import crawl_question as cq 
import threading
import time
import crawl_class

url_temp = []
#url_list = []

# login
def user_login():
    session = requests.session()
    session.cookies = cookielib.LWPCookieJar(filename='cookies')
    try:
        session.cookies.load(ignore_discard=True)
    except:
        pass
    
    if not session.cookies:
        account = input('please input your account:')
        secret = input('please input your secret:')
        login.login(secret, account)
        login.isLogin()
    else:
        if login.isLogin():
            print('you have already logined!')
        else:
            account = input('please input your account:')
            secret = input('please input your secret:')
            login.login(secret, account)
            login.isLogin()

# define the type of data you input
def search_URL_question(content, url_list):
    # get a question url
    content = {'' : content}
    url = "https://www.zhihu.com/search?type=content&q" + urllib.parse.urlencode(content)
    # search url in this page
    url_list = URL.get_content(url, [])
    # duplicate removal
    url_list = list(set(url_list))
    return url_list
    
def search_URL_topic(content, url_list, num_page):
    # get a topic url
    url = "https://www.zhihu.com/search?type=topic&q=" + content

    # search url in this page
    url_temp = URL.get_topic_id(url, [])
    if len(url_temp) > 0:
        url_list = url_list + url_temp

    # duplicate removal
    url_list = list(set(url_list))

    # search url based on BFS
    if len(url_list) > 0:
        url = url_list[0]
    while '/topic' in url and len(url_list) > 0:
        url = url_list.pop(0)
        url_temp = URL.get_question_id(url, [], num_page)
        if len(url_temp) > 0:
            url_list = url_list + url_temp
    # duplicate removal
    url_list = list(set(url_list))
    return url_list


def crawl_web_into_json(url,filename):
    crawl_class.Crawler(funcName=cq.crawl_question,args=(url,filename,)).start()

