# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 07:34:53 2017

@author: freedli
"""

# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import zhihu_crawler
import threading
import time
import os.path

###########################################################################
## Class MyFrame1
###########################################################################
class MyFrame1 ( wx.Frame ):
	filename = ''
	search_item = ''
	pattern = ''
	url_list = []
	num_of_url = 0
	num_of_done = 0
	thread_flag = True

	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"知乎爬虫", pos = wx.DefaultPosition, size = wx.Size( 450,500 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		try:  
				image_file = 'bg.jpg'  
				to_bmp_image = wx.Image(image_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()  
				self.bitmap = wx.StaticBitmap(self, -1, to_bmp_image, (0, 0))  
		except IOError:
				print ('Image file %s not found' , image_file  )
				raise SystemExit  

		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText1 = wx.StaticText( self.bitmap, wx.ID_ANY, u"存储目录", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		bSizer7.Add( self.m_staticText1, 0, wx.ALL, 5 )
		
		self.savePathTextCtrl = wx.TextCtrl( self.bitmap, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, (200,30), 0 )
		bSizer7.Add( self.savePathTextCtrl, 0, wx.ALL, 5 )
		
		self.savePathButton = wx.Button( self.bitmap, wx.ID_ANY, u"确定", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.savePathButton, 0, wx.ALL, 5 )
		
		
		bSizer5.Add( bSizer7, 1, wx.EXPAND, 5 )
		
		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText2 = wx.StaticText( self.bitmap, wx.ID_ANY, u"搜索问题", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		bSizer8.Add( self.m_staticText2, 0, wx.ALL, 5 )
		
		self.searchTextCtrl = wx.TextCtrl(self.bitmap, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, (200,30), 0 )
		bSizer8.Add( self.searchTextCtrl, 0, wx.ALL, 5 )
		
		m_comboBox1Choices = ['question','topic']
		self.m_comboBox1 = wx.ComboBox( self.bitmap, wx.ID_ANY, u"搜索类型", wx.DefaultPosition, (80,30), m_comboBox1Choices, 0 )
		bSizer8.Add( self.m_comboBox1, 0, wx.ALL, 5 )
		
		
		bSizer5.Add( bSizer8, 1, wx.EXPAND, 5 )
		
		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText3 = wx.StaticText( self.bitmap, wx.ID_ANY, u"运行情况", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		bSizer9.Add( self.m_staticText3, 0, wx.ALL, 5 )
		
		self.startButton = wx.Button( self.bitmap, wx.ID_ANY, u"开始", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer9.Add( self.startButton, 0, wx.ALL, 5 )
		
		self.pauseButton = wx.Button( self.bitmap, wx.ID_ANY, u"暂停", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer9.Add( self.pauseButton, 0, wx.ALL, 5 )
		
		self.resumeButtton = wx.Button( self.bitmap, wx.ID_ANY, u"继续", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer9.Add( self.resumeButtton, 0, wx.ALL, 5 )
		
		
		bSizer5.Add( bSizer9, 1, wx.EXPAND, 5 )
		
		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText4 = wx.StaticText( self.bitmap, wx.ID_ANY, u"爬取进度", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		bSizer11.Add( self.m_staticText4, 0, wx.ALL, 5 )
		
		self.processTextCtrl = wx.TextCtrl( self.bitmap, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11.Add( self.processTextCtrl, 0, wx.ALL, 5 )
		
		self.m_staticText5 = wx.StaticText( self.bitmap, wx.ID_ANY, u"话题爬取页数", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		bSizer11.Add( self.m_staticText5, 0, wx.ALL, 5 )
		
		self.topicPageTextCtrl = wx.TextCtrl( self.bitmap, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11.Add( self.topicPageTextCtrl, 0, wx.ALL, 5 )
		
		
		bSizer5.Add( bSizer11, 1, wx.EXPAND, 5 )
		
		
		bSizer2.Add( bSizer5, 1, wx.EXPAND, 5 )
		
		
		bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )
		
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		self.console_textctrl = wx.TextCtrl( self.bitmap, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, (450,200), wx.TE_MULTILINE )
		bSizer4.Add( self.console_textctrl, 0, wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer4, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.savePathButton.Bind( wx.EVT_BUTTON, self.savePathButtonClick )
		self.startButton.Bind( wx.EVT_BUTTON, self.startButtonClick )
		self.pauseButton.Bind( wx.EVT_BUTTON, self.pauseButtonClick )
		self.resumeButtton.Bind( wx.EVT_BUTTON, self.resumeButtonClick )
	
	def __del__( self ):
		wx.Exit()
	
	# Virtual event handlers, overide them in your derived class
	def savePathButtonClick( self, event ):
		savePath = self.savePathTextCtrl.GetLineText(1)
		if os.path.exists(savePath):
				savePath = savePath.replace('\\','/')
				if not savePath.endswith('/'):
						savePath = savePath + '/'
				self .filename = savePath
				text = "Save path is "+self.filename
				self.consoleText(text)
		else:
				self.savePathTextCtrl.Clear()

	def startButtonClick( self, event ):
		self.search_item = self.searchTextCtrl.GetLineText(1)
		self.pattern = self.m_comboBox1.GetString(self.m_comboBox1.GetCurrentSelection())
		text = "-------Search URL Start!---------"
		self.consoleText(text)
		if self.pattern == 'question':
				self.url_list = zhihu_crawler.search_URL_question(self.search_item, self.url_list)
		else:
				num_page = int(self.topicPageTextCtrl.GetLineText(1))
				self.url_list = zhihu_crawler.search_URL_topic(self.search_item, self.url_list, num_page)
		self.num_of_url = len(self.url_list)
		text = "------Search URL Completed-------"
		self.consoleText(text)
		text = "Here are " + str(self.num_of_url) + "URLs"
		self.consoleText(text)
		t1 = threading.Thread(target=self.runTask,args=())
		t1.start()
	 
	def pauseButtonClick( self, event ):
		self.thread_flag = False
		self.consoleText("---Crawling Pause---")

	def resumeButtonClick( self, event ):
		self.thread_flag = True
		self.consoleText("---Crawling resume---")

	def processText(self):
		processStr = str(round(self.num_of_done/self.num_of_url*100 , 3))+'%'
		self.processTextCtrl.SetValue(processStr)

	def consoleText( self ,text):
		self.console_textctrl.AppendText("\n"+text)

	def runTask(self):
		lock = threading.Lock()
		start = time.clock()
		self.consoleText("---URL Crawling---")
		while self.url_list:
				if (len(threading.enumerate())<11)&self.thread_flag :
						lock.acquire()
						url = self.url_list.pop(0)
						lock.release()
						zhihu_crawler.crawl_web_into_json(url, self.filename)
						self.num_of_done = self.num_of_done + 1
						self.processText()
						self.consoleText(url)
		elapsed = (time.clock() - start)
		self.consoleText("Time Cost: "+str(elapsed)+"s")