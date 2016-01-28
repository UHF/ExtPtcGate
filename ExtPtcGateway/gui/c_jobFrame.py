'''
Created on 12.03.2015

@author: f.uhlenbruck
'''
import os
import subprocess
import datetime
import time
from threading import *

from tkinter import ttk, IntVar, StringVar, messagebox
from tkinter.constants import *

from lib.app import c_configData, c_itemData, c_jobData

class c_jobFrame(ttk.Frame):
    def __init__(self,master,owner,config_data,**params):
        try:
            super().__init__(master,**params)
            self.owner = owner
            self.config_data = config_data
            self.job_data = config_data.job_data
            self.__create_children()
        except: raise

    def __create_children(self):
        try:
            row=0
            ttk.Label(self,text="Executing Job:").grid(column=0,row=row)
            ttk.Entry(self,textvariable=self.job_data.job_title,state="readonly").grid(column=1,row=row)
            
            ttk.Label(self,text="Active Workers:").grid(column=2,row=row)
            ttk.Entry(self,textvariable=self.job_data.active_workers,state="readonly").grid(column=3,row=row)
            row = row+1
            ttk.Label(self,text="Tatal Jobs:").grid(column=0,row=row)
            ttk.Entry(self,textvariable=self.job_data.jobs_total,state="readonly").grid(column=1,row=row)
            row = row+1
            ttk.Label(self,text="Open:").grid(column=0,row=row)
            ttk.Entry(self,textvariable=self.job_data.jobs_open,state="readonly").grid(column=1,row=row)
            row = row+1
            ttk.Label(self,text="Running:").grid(column=0,row=row)
            ttk.Entry(self,textvariable=self.job_data.jobs_running,state="readonly").grid(column=1,row=row)
            row = row+1
            ttk.Label(self,text="Closed:").grid(column=0,row=row)
            ttk.Entry(self,textvariable=self.job_data.jobs_closed,state="readonly").grid(column=1,row=row)
            pass
        except: raise


    def job_start(self):
        try:
            self.__jobwatch = Thread(target=self.__t_job_watch)
            time.sleep(2)
            self.__jobwatch.start()
        except: raise
    
    def __t_job_watch(self):
        try:    
            self.job_data.job_timer.join()
            self.job_end()
        except: raise

    def job_end(self):
        try:
            self.owner.job_end()
        except:raise
    
        
    
        
