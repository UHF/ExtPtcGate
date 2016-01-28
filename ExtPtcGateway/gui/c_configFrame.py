'''
Created on 11.03.2015

@author: f.uhlenbruck
'''
import os

from tkinter import Tk ,ttk, Text, IntVar, StringVar, filedialog
from tkinter.constants import *

from lib.app import c_configData, c_itemData

class c_configFrame(ttk.Frame):
    '''
    classdocs
    '''

    def __init__(self,master,owner,config_data,**params):
        '''
        Constructor
        '''
        try:
            super().__init__(master,**params)
            self.owner = owner
            self.config_data = config_data
            self.validation_result = StringVar()
            self.validation_result.trace('w',self.__on_change_validation_result)
            self.__create_children(config_data)

        except: raise


    def __del__(self):
        '''
        Destructor
        '''
        for child in self.children:
            self.children[child].destroy()

    def __create_children(self,config_data):
        try:
            row=0
            ttk.Label(self,text="Required Settings").grid(column=0,row=row,sticky='w')
            row=row+1

            ttk.Label(self,text="Text Editor").grid(column=0,row=row,sticky='w')
            ttk.Entry(self,textvariable=self.config_data.text_edit,width=100,state="readonly").grid(column=1,row=row,sticky='w')
            ttk.Button(self,name="btn_select_textedit",text="Select",command=self.__on_btn_select_textedit).grid(column=2,row=row,sticky='w')
            row=row+1
            
            ttk.Label(self,text="File Compare").grid(column=0,row=row,sticky='w')
            ttk.Entry(self,textvariable=self.config_data.file_compare,width=100,state="readonly").grid(column=1,row=row,sticky='w')
            ttk.Button(self,name="btn_select_fielcompare",text="Select",command=self.__on_btn_select_file_compare).grid(column=2,row=row,sticky='w')
            row=row+1

            ttk.Label(self,text="PTC Client directory").grid(column=0,row=row,sticky='w')
            ttk.Entry(self,textvariable=self.config_data.ptc_client_dir,width=100,state="readonly").grid(column=1,row=row,sticky='w')
            ttk.Button(self,name="btn_select_ptc_client",text="Select",command=self.__on_btn_select_ptc_client).grid(column=2,row=row,sticky='w')
            row=row+1

            ttk.Label(self,text="PTC Gateway(Rif.bat)").grid(column=0,row=row,sticky='w')
            ttk.Entry(self,textvariable=self.config_data.rif_bat,width=100,state="readonly").grid(column=1,row=row,sticky='w')
            ttk.Button(self,name="btn_select_rifbat",text="Select",command=self.__on_btn_select_rifbat).grid(column=2,row=row,sticky='w')
            row=row+1

            ttk.Label(self,text="Mapping Template").grid(column=0,row=row,sticky='w')
            ttk.Entry(self,textvariable=self.config_data.template,width=100,state="readonly").grid(column=1,row=row,sticky='w')
            ttk.Button(self,name="btn_select_template",text="Select",command=self.__on_btn_select_template).grid(column=2,row=row,sticky='w')
            row=row+1

            ttk.Label(self,text="Options").grid(column=0,row=row,sticky='w')
            row=row+1

            ttk.Label(self,text="Max number of paralell processes").grid(column=0,row=row,sticky='w')
            ttk.Entry(self,textvariable=self.config_data.max_threads,width=2,).grid(column=1,row=row,sticky='w')
            row=row+1
            
            ttk.Label(self,text="Ptc Gateway Mapping GUI").grid(column=0,row=row,sticky='w')
            ttk.Checkbutton(self,variable=self.config_data.gw_mapping_gui,onvalue=True, offvalue=False).grid(column=1,row=row,sticky='w')
            row=row+1

            
            ttk.Label(self,text="Ptc Gateway GUI").grid(column=0,row=row,sticky='w')
            ttk.Checkbutton(self,variable=self.config_data.gw_gui,onvalue=True, offvalue=False).grid(column=1,row=row,sticky='w')
            row=row+1

            ttk.Label(self,text="Ptc Gateway NoGUI All Yes").grid(column=0,row=row,sticky='w')
            ttk.Checkbutton(self,variable=self.config_data.gw_all_yes,onvalue=True, offvalue=False).grid(column=1,row=row,sticky='w')
            row=row+1

            ttk.Label(self,text="Project Settings").grid(column=0,row=row,sticky='w')
            row=row+1

            ttk.Label(self,text="PTC Project").grid(column=0,row=row,sticky='w')
            ttk.Entry(self,textvariable=self.config_data.ptc_project,width=100).grid(column=1,row=row,sticky='w')
            row=row+1

            ttk.Label(self,text="Input directory").grid(column=0,row=row,sticky='w')
            ttk.Entry(self,textvariable=self.config_data.input_dir,width=100,state="readonly").grid(column=1,row=row,sticky='w')
            ttk.Button(self,name="btn_select_input_dir",text="Select",command=self.__on_btn_select_input_dir).grid(column=2,row=row,sticky='w')

            row=row+1
            ttk.Label(self).grid(column=0,row=row,sticky='w')
            row=row+1
            ttk.Label(self).grid(column=0,row=row,sticky='w')
            row=row+1
            ttk.Label(self).grid(column=0,row=row,sticky='w')

            row=row+1
            self.textfield=Text(self,height=8,width=75,state='disabled')
            self.textfield.grid(column=1,row=row)
            ttk.Button(self,name="btn_validate",text="Validate",command=self.__on_btn_validate).grid(column=2,row=row)
            
        except: raise
        else: pass

    def __on_btn_select_rifbat(self):       self.config_data.cmd_select_rifbat()
    def __on_btn_select_template(self):     self.config_data.cmd_select_template()
    def __on_btn_select_textedit(self):     self.config_data.cmd_select_textedit()
    def __on_btn_select_file_compare(self): self.config_data.cmd_select_filecompare()
    def __on_btn_select_ptc_client(self):   self.config_data.cmd_select_ptc_client()
    def __on_btn_select_input_dir(self):    self.config_data.cmd_select_input_dir()

    def __on_chk_use_ptc(self):
        pass

    def __on_btn_validate(self):
        (result,text) = self.config_data.cmd_validate_config()
        self.validation_result.set(text) 
        if(result==True):
            self.owner.config_valid()
        pass
    
    def __on_change_validation_result(self,*args):
        try:
            self.textfield.configure(state='normal')
            self.textfield.delete(1.0,END)
            self.textfield.insert(END,self.validation_result.get())
            self.textfield.configure(state='disabled')
        except: raise