# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 03:59:25 2017

@author: freedli
"""

import wx
import GUI_win
import zhihu_crawler

# login
zhihu_crawler.user_login()

"""
url_list = []
url_list = zhihu_crawler.search_URL('question', 'AI', url_list)
print(len(url_list))
"""


#GUI window
app = wx.App()
frame = wx.Frame(None)

Gui_main = GUI_win.MyFrame1(frame)

Gui_main.Show()

app.MainLoop()
