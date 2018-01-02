# -*- coding: utf-8 -*-
"""
Created on 22/10/2017
@author : Haoran You

"""
import requests
import os,time
import re
from PIL import Image
from bs4 import BeautifulSoup
import http.cookiejar as cookielib

url = "https://www.zhihu.com/"

headers = {
    "Host": "www.zhihu.com",
    "Referer" : url,
    'X-Requested-With' : 'XMLHttpRequest',
    'User-Agent' : 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'
}

session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies')

# login with cookie!
try:
    session.cookies.load(ignore_discard=True)
except:
    print('Cookie cannot be load!')

def get_captcha():
    t = str(int(time.time()*1000))
    captcha_url = url + 'captcha.gif?r=' + t + "&type=login"
    r = session.get(url=captcha_url, headers=headers)
    with open('captcha.gif', 'wb') as f:
        f.write(r.content)
        f.close()
    im = Image.open('captcha.gif')
    im.show()
    im.close()
    captcha = input("please input the captcha:")
    return captcha

def isLogin():
    user_url = url + 'settings/profile'
    setting_page = session.get(url=user_url, headers=headers)
    # print('the response status code of profile page: ', setting_page.status_code)
    profilesoup = BeautifulSoup(setting_page.text, 'html.parser')
    name = profilesoup.find('span', {'name'})
    print('your name: ', name)
    # print('the title of setting page: ', profilesoup.title)
    if not name:
        return False
    else:
        return True

def login(secret, account):
    if re.match(r"^1\d{10}$", account):
        # login with phone number
        post_url = 'https://www.zhihu.com/login/phone_num'
        postdata = {
            'phone_num': account,
            'password' : secret
        }
    else:
        # login with email
        post_url = url + 'login/email'
        postdata = {
            'email' : account,
            'password': secret
        }
    # with captcha
    postdata["captcha"] = get_captcha()
    login_page = session.post(url=post_url, headers=headers, data=postdata)
    print('the status code returned by server:', login_page.status_code)
    if login_page.status_code != 200:
        print('login error!')
    else:
        print(login_page.json())
        while login_page.json()['r'] == 1:
            postdata["captcha"] = get_captcha()
            login_page = session.post(url=post_url, headers=headers, data=postdata)
            print('the status code returned by server:', login_page.status_code)
            print(login_page.json())

    session.cookies.save()

if __name__ == '__main__':
    if isLogin():
        print('you have already logined!')
    else:
        account = input('please input your account:')
        secret = input('please input your secret:')
        login(secret, account)
        isLogin()
