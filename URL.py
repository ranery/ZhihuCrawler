# -*- coding: utf-8 -*-
"""
Created on 24/10/2017
@author : Haoran You

"""
import re
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

headers = {
    "Host": "www.zhihu.com",
    "Referer" : "https://www.zhihu.com",
    'X-Requested-With' : 'XMLHttpRequest',
    'User-Agent' : 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'
}

def getHTMLText(url):
    try:
        r = requests.get(url, headers=headers)
        # r.status_code    200
        # r.encoding    'utf-8'
        return r.content
    except:
        return "Error"

def get_topic_id(url, url_list):
    demo = getHTMLText(url)
    soup = BeautifulSoup(demo, "html.parser")
    for link in soup.find_all('a'):
        url_temp = link.get('href')
        if not url_temp:
            pass
        elif '/topic' in url_temp and not 'http' in url_temp:
            topic_id = url_temp[7:15]
            url_list.append('https://www.zhihu.com/topic/' + topic_id)
    return url_list

def get_question_id(url, url_list):
    page_url = url + '/questions?page=1'
    demo = getHTMLText(page_url)
    soup = BeautifulSoup(demo, "html.parser")
    # get total page
    num_page = 1
    for link in soup.find_all('a'):
        url_temp = link.get('href')
        if '?page=' in url_temp:
            num_page = max(num_page, int(url_temp[6:len(url_temp)]))
    print('the number of page in topic ' + url[28:len(url)] + ' is : ' + str(num_page))
    # get all questions under topic
    for page in range(1, min(2, num_page+1)):
        page_url = url + '/questions?page=' + str(page)
        demo = getHTMLText(page_url)
        soup = BeautifulSoup(demo, "html.parser")
        for link in soup.find_all('a'):
            url_temp = link.get('href')
            if '/question' in url_temp and not 'http' in url_temp:
                question_id = url_temp[10:19]
                url_list.append('https://www.zhihu.com/question/' + question_id)
    return url_list

def get_content(url, url_list):
    driver = webdriver.PhantomJS(executable_path=r"E:/phantomjs/bin/phantomjs.exe")
    driver.implicitly_wait(10)
    driver.maximize_window()
    driver.get(url)

    demo_temp = []
    time.sleep(1)
    while True:
        if len(demo_temp) > 10:
            demo_temp = demo_temp[-10:]
            if demo_temp[0] == demo_temp[9]:
                break
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(1)
        demo_temp.append(driver.page_source)

    demo = demo_temp.pop()
    soup = BeautifulSoup(demo, 'html.parser')
    """
    for link in soup.find_all('a'):
        url_temp = link.get('href')
        if '/question' in url_temp and not 'http' in url_temp:
            question_id = url_temp[10:18]
            url_list.append('https://www.zhihu.com/question/' + question_id)
    """
    for meta in soup.find_all('meta', attrs={'itemprop': 'url'}):
        url_temp = meta.get('content')
        url_list.append(url_temp)

    return url_list