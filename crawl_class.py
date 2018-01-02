# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 20:17:20 2018

@author: freedli
"""
import threading
import traceback
import sys

class Crawler(threading.Thread):
    #class_lock = threading.Lock()
    
    def __init__(self,funcName=None,args=()):
        threading.Thread.__init__(self)  
        self.args = args
        self.funcName = funcName  
        self.exitcode = 0  
        self.exception = None  
        self.exc_traceback = ''  

    def run(self):
        try:
            self._run()
        except Exception as e:
            self.exitcode = 1
            self.exception = e
            self.exc_traceback = ''.join(traceback.format_exception(*sys.exc_info()))
            print("URL Crawler Exception: ", self.args[0])
            print(self.exc_traceback)

    def _run(self):
        try:  
            self.funcName(self.args[0],self.args[1])   
        except Exception as e:  
            raise e
