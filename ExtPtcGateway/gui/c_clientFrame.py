'''
Created on 11.03.2015

@author: f.uhlenbruck
'''

from tkinter import ttk
from tkinter.constants import *

from gui.c_inputFrame import c_inputFrame
from gui.c_configFrame import c_configFrame
from gui.c_jobFrame import c_jobFrame

from lib.app import c_itemData, c_configData, c_jobData

TAB_CONFIG= 0
TAB_INPUT = 1
TAB_JOB   = 2

class c_clientFrame(ttk.Frame):
    '''
    classdocs
    '''
    def __init__(self,master,savedata=None,**params):
            '''
            Constructor
            '''
            try:
                super().__init__(master,**params)
                self.items_data=[]
                self.config_data=c_configData()
                self.__create_children()
                self.__restore_data(savedata=savedata)
                
            except: raise
    def __del__(self):
        '''
        Destructor
        '''
        for child in self.children:
            self.children[child].destroy()
    
    def __create_children(self):
        try:
            self.book = ttk.Notebook(self,name="book")
            
            self.frm_config = c_configFrame(self.book,self,self.config_data,name="config")
            self.frm_input = c_inputFrame(self.book,self,self.config_data,name="input")
            self.frm_job = c_jobFrame(self.book,self,self.config_data,name="job")

            self.frm_config.pack(side=LEFT, fill=BOTH, expand=TRUE)
            self.frm_input.pack(side=LEFT, fill=BOTH, expand=TRUE)
            self.frm_job.pack(side=LEFT, fill=BOTH, expand=TRUE)
            
            self.book.add(self.frm_config,text="Configuration")
            self.book.add(self.frm_input,text="Input",state='disabled')
            self.book.add(self.frm_job,text="Job",state='disabled')
            
            self.book.select(TAB_CONFIG)
            self.book.pack(side=TOP,fill=BOTH,expand=TRUE)
        except: raise
    
    
        
    def get_save_data(self):
        return self.config_data.get_save_data()
        
    def __restore_data(self,savedata):
        try:    
            self.config_data.restore_data(savedata)
            self.frm_input.create_items()
        except: raise
            
                  
    def cmd_transfer(self):
        try:
            self.config_data.cmd_transfer()
            self.job_start()
            
        except: raise
    
    def cmd_finalize(self):
        try:
            self.config_data.cmd_finalize()
            self.job_start()  
        except: raise
    
    def cmd_prepare_files(self):
        try:
            self.config_data.cmd_prepare_files()
            self.job_start()
            
        except: raise
    
    def cmd_scan_for_files(self):
        try:
            self.config_data.cmd_scan_for_files()
            self.job_start()
            
        except: raise
        
    def cmd_delete(self):
        try:  
			self.frm_input.delete_items() 
            self.config_data.cmd_delete()
            self.frm_input.create_items()
        except: raise

    def cmd_add_files(self):
        try:
            self.frm_input.delete_items()    
            self.config_data.cmd_add_files()
            
        except: raise    
                                                   
    def job_start(self):
        self.book.tab(TAB_JOB, state='normal')
        self.book.tab(TAB_INPUT, state='disabled')
        self.book.tab(TAB_CONFIG, state='disabled')
        self.book.select(TAB_JOB)
        self.master.cbk_menue_disable()
        self.frm_job.job_start()

    def job_end(self):
        self.book.tab(TAB_INPUT, state='normal')
        self.book.tab(TAB_CONFIG, state='normal')
        self.master.cbk_menue_enable()
        self.frm_input.job_end()

    def config_valid(self):
        try:    
            self.book.tab(TAB_INPUT, state='normal')
            self.book.select(TAB_INPUT)
        except: raise

    def input_valid(self):
        pass
    
    def __checkFileAddValid(self,filename):
        result = False
        try:
            ending =  filename[-len(INFILE_ENDING):]
            purename = filename[:-len(INFILE_ENDING)]
            rw1 = purename[-len(INFILE_REWORK_1_TAG):]
            rw2 = purename[-len(INFILE_REWORK_2_TAG):]
            mapping = purename[-len(MAPPINGFILE_TAG):]

            if((ending == INFILE_ENDING) and
                (rw1 != INFILE_REWORK_1_TAG) and
                (rw2 != INFILE_REWORK_2_TAG) and
                (mapping != MAPPINGFILE_TAG)):
                result = True
        except: pass
        return result

    def __checkFileAvalible(self,filename):
        result = False
        for item in self.items_data:
            try:
                if(item.file.get() == filename):
                    result = True
            except: pass
        return result
