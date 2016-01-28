'''
Created on 11.03.2015

@author: f.uhlenbruck
'''
from platform import os
from tkinter import Tk,ttk, PhotoImage, filedialog, IntVar, StringVar
from tkinter.constants import *

from gui.c_scrolledFrame import c_scrolledFrame
from img.d_images import d_images
from lib.app import c_configData, c_itemData
from tkinter.ttk import Style

item_state = {"tbd":"gray","warn":"yellow","ok":"green","error":"red","n/a":"blue"}

class c_inputItem_compact(ttk.Frame):
    def __init__(self,master,owner,item_data,**params):
        '''
        Constructor
        '''
        try:
            super().__init__(master,**params)
            self.owner = owner
            self.item_data = c_itemData
            self.item_data = item_data
            self.__create_traces()
            self.__create_children()
            self.__create_styles()
            self.__sytle_items()
        except: raise
    
    def __create_children(self):
        row=0
        ttk.Checkbutton(self,name="active",variable=self.item_data.active, onvalue=True, offvalue=False).grid(column=0,row=row,sticky='w',rowspan=2)
        ttk.Entry(self,name="file",textvariable=self.item_data.file,width=50,state="readonly").grid(column=1,row=row,sticky='w',columnspan=2)
        
        ttk.Button(self,name="file_auto_rework",text="Rework",command=self.item_data.cmd_auto_rework).grid(column=4,row=row,sticky='w')
        ttk.Button(self,name="file_compare",text="Compare",state='disabled',command=self.item_data.cmd_compare_file).grid(column=5,row=row,sticky='w')
        
        ttk.Label(self,text="Mapping").grid(column=6,row=row,sticky='w',padx=2,pady=2)
        ttk.Button(self,name="mapping_create",text="Create",command=self.item_data.cmd_create_mapping).grid(column=7,row=row,sticky='w')
        ttk.Button(self,name="mapping_edit",text="Edit",state='disabled',command=self.item_data.cmd_edit_mapping).grid(column=8,row=row,sticky='w')
        
        
        ttk.Label(self,text="Process").grid(column=9,row=row,sticky='w',padx=2,pady=2)
        ttk.Button(self,name="validate",text="Validate",command=self.item_data.cmd_validate).grid(column=10,row=row,sticky='w')
        ttk.Button(self,name="transfer",text="Transfer",state='disabled',command=self.item_data.cmd_transfer).grid(column=11,row=row,sticky='w')
        
        ttk.Button(self,name="logfile",text="Logfile",command=self.item_data.cmd_view_log).grid(column=13,row=row,sticky='w',rowspan=2)
        
        
        row=row+1
        ttk.Entry(self,name="rif_id",textvariable=self.item_data.rif_id,width=40,state="readonly").grid(column=1,row=row,sticky='w')
        ttk.Entry(self,name="ptc_id",textvariable=self.item_data.ptc_id,width=10,state="readonly").grid(column=2,row=row,sticky='w')
        ttk.Button(self,name="file_read_rif",text="Read RIF-ID",command=self.item_data.cmd_read_rif_id).grid(column=4,row=row,sticky='w')
        ttk.Button(self,name="file_read_ptc",text="Read PTC-ID",command=self.item_data.cmd_read_ptc_id).grid(column=5,row=row,sticky='w')
        
        ttk.Button(self,name="mapping_compare",text="Compare",state='disabled',command=self.item_data.cmd_compare_mapping).grid(column=7,row=row,sticky='w')
        
        ttk.Button(self,name="finalize",text="Finalize",state='normal',command=self.item_data.cmd_finalize).grid(column=10,row=row,sticky='w')
        
        
    def __create_traces(self):
        try:
            self.item_data.active.trace('w',self.__on_active)
            self.item_data.valide.trace('w',self.__on_valide)
            self.item_data.file.trace('w',self.__on_file)
            self.item_data.file_rw1.trace('w',self.__on_file_rw1)
            self.item_data.rif_id.trace('w',self.__on_rif_id)
            self.item_data.ptc_id.trace('w',self.__on_ptc_id)
            self.item_data.transfered.trace('w',self.__on_transfered)
            self.item_data.mapping.trace('w',self.__on_mapping)
        except: raise
            
    def __on_active(self,*args):pass
    def __on_valide(self,*args):
        try:
            if(self.item_data.valide.get()==True):
                self.children["validate"].configure(style="ok.TButton")
                self.children["transfer"].configure(style="warn.TButton",state='normal')
            else:
                self.children["validate"].configure(style="err.TButton")
                self.children["transfer"].configure(style="tbd.TButton",state='disabled')
        except: raise
        
    def __on_file(self,*args):pass
    
    def __on_file_rw1(self,*args):
        try:
            if(self.item_data.file_rw1.get()!=""):  
                self.children["file_auto_rework"].configure(style="ok.TButton")
                self.children["file_compare"].configure(style="option.TButton",state='normal')
            else:   
                self.children["file_auto_rework"].configure(style="err.TButton")
                self.children["file_compare"].configure(style="tbd.TButton",state='disable')
        except: raise
                
    def __on_rif_id(self,*args):
        try:
            if(self.item_data.rif_id.get()!=""):    
                self.children["file_read_rif"].configure(style="ok.TButton")
                self.children["rif_id"].configure(style="ok.TEntry")
                self.children["file"].configure(style="ok.TEntry")
            else:                                   
                self.children["file_read_rif"].configure(style="err.TButton")
                self.children["rif_id"].configure(style="err.TEntry")
                self.children["file"].configure(style="err.TEntry")
        except: raise
        
    def __on_ptc_id(self,*args):
        try:
            if(self.item_data.ptc_id.get()!=""):
                self.children["file_read_ptc"].configure(style="ok.TButton")
                self.children["ptc_id"].configure(style="ok.TEntry")
            else:
                self.children["file_read_ptc"].configure(style="err.TButton")
                self.children["ptc_id"].configure(style="err.TEntry")
        except: raise
        
    def __on_mapping(self,*args):
        try:
            if(self.item_data.mapping.get()!=""):  
                self.children["mapping_create"].configure(style="ok.TButton")
                self.children["mapping_edit"].configure(style="option.TButton",state='normal')
                self.children["mapping_compare"].configure(style="option.TButton",state='normal')
            else:
                self.children["mapping_create"].configure(style="err.TButton")
                self.children["mapping_edit"].configure(style="tbd.TButton",state='disabled')
                self.children["mapping_compare"].configure(style="tbd.TButton",state='disabled')
        except: raise
        
    def __on_transfered(self,*args):
        if(self.item_data.transfered.get()!=""):
            self.children["finalize"].configure(style="ok.TButton")
        else:
            self.children["finalize"].configure(style="err.TButton")
        pass
    
    def __create_styles(self):
        self.style = ttk.Style()
        pass
    
    def __sytle_items(self):
        if(self.item_data.rif_id.get()!=""):    
            self.children["file_read_rif"].configure(style="ok.TButton")
            self.children["rif_id"].configure(style="ok.TEntry")
            self.children["file"].configure(style="ok.TEntry")
        else:                                   
            self.children["file_read_rif"].configure(style="warn.TButton")
            self.children["rif_id"].configure(style="warn.TEntry")
            self.children["file"].configure(style="warn.TEntry")
            
        if(self.item_data.ptc_id.get()!=""):
            self.children["file_read_ptc"].configure(style="ok.TButton")
            self.children["ptc_id"].configure(style="ok.TEntry")
        else:
            self.children["file_read_ptc"].configure(style="warn.TButton")
            self.children["ptc_id"].configure(style="warn.TEntry")
            
        if(self.item_data.file_rw1.get()!=""):  
            self.children["file_auto_rework"].configure(style="ok.TButton")
            self.children["file_compare"].configure(style="option.TButton",state='normal')
        else:   
            self.children["file_auto_rework"].configure(style="warn.TButton")
        
        if(self.item_data.mapping.get()!=""):  
            self.children["mapping_create"].configure(style="ok.TButton")
            self.children["mapping_edit"].configure(style="option.TButton",state='normal')
            self.children["mapping_compare"].configure(style="option.TButton",state='normal')
        else:
            self.children["mapping_create"].configure(style="warn.TButton")
            
        self.children["logfile"].configure(style="option.TButton")        
        self.children["validate"].configure(style="warn.TButton")
        pass
            
class c_inputFrame(ttk.Frame):
    '''
    classdocs
    '''
    def __init__(self,master,owner,config_data,**params):
        '''
        Constructor
        '''
        try:
            super().__init__(master,**params)
            self.items=[]
            self.owner = owner
            self.config_data=c_configData
            self.config_data=config_data
            self.items_data = c_itemData
            self.items_data = config_data.items_data
            self.__create_children()
            self.items_data
        except: raise

    def __del__(self):
        '''
        Destructor
        '''
        for child in self.children:
            self.children[child].destroy()

    def __create_children(self):
        try:
            self.__create_command_menue()
            self.__create_folder_frame()
            self.__create_data_frame()
        except: raise
        else: pass

    def __create_command_menue(self):
        try:
            self.frm_command=ttk.Frame(self,name="input")
            self.frm_command.pack(side=TOP,fill=X)
            
            ttk.Button(self.frm_command,name="btn_add",text="Add",command=self.owner.cmd_add_files).pack(side=LEFT)
            ttk.Label(self.frm_command,text="    All").pack(side=LEFT)
            ttk.Button(self.frm_command,name="btn_select_all",text="Select",command=self.config_data.cmd_select_all).pack(side=LEFT)
            ttk.Button(self.frm_command,name="btn_deselect_all",text="Deselect",command=self.config_data.cmd_deselect_all).pack(side=LEFT)
            ttk.Label(self.frm_command,text="    Selected").pack(side=LEFT)
            ttk.Button(self.frm_command,name="btn_delete",text="Delete",command=self.__cmd_delete).pack(side=LEFT)
            ttk.Button(self.frm_command,name="btn_scan_for_files",text="Scan for Files",command=self.__cmd_scan_for_files).pack(side=LEFT)
            ttk.Label(self.frm_command,text="    Process").pack(side=LEFT)
            ttk.Button(self.frm_command,name="btn_prepare_files",text="Prepare",command=self.__cmd_prepare_files).pack(side=LEFT)
            ttk.Button(self.frm_command,name="btn_validate",text="Validate",command=self.__cmd_validate).pack(side=LEFT)
            ttk.Button(self.frm_command,name="btn_transfer",text="Transfer",state = 'disabled',command=self.__cmd_transfer).pack(side=LEFT)
        except: raise
        else: pass
    def __create_folder_frame(self):
        try:    
            self.frm_folder=ttk.Frame(self,name="frm_folder")
            self.frm_folder.pack(side=TOP,fill=X)
            ttk.Label(self.frm_folder,text="Input Directory").pack(side=LEFT)
            ttk.Entry(self.frm_folder,name="e_folder",textvariable=self.config_data.input_dir,state='readonly',width=100).pack(side=LEFT,expand=TRUE,fill=X)
        except: raise
    def __create_data_frame(self):
        try:
            self.frm_data=c_scrolledFrame(self,name="data")
            self.frm_data.pack(side=TOP,fill=BOTH,expand=True)
        except: raise

    def __cmd_delete(self):
        try:    self.owner.cmd_delete()
        except:raise
    def __cmd_scan_for_files(self):
        try:    self.owner.cmd_scan_for_files()
        except:raise
    def __cmd_prepare_files(self):
        try: self.owner.cmd_prepare_files()
        except: raise
    def __cmd_validate(self):
        try:
            if(self.config_data.cmd_validate_item()==True):
                self.frm_command.children["btn_transfer"].configure(state='normal')
        except:raise
    def __cmd_transfer(self):
        try:    self.owner.cmd_transfer()
        except: raise        
    def __cmd_finalize(self):
        try:
            self.config_data.cmd_finalize() 
            self.owner.job_start()
        except: raise
        
    def delete_items(self):
        try:
            idx = len(self.items)-1
            while(idx>=0):
                self.items[idx].destroy()
                idx = idx -1
        except: raise
        
    def create_items(self):
        try:
            self.items.clear()
            for item in self.config_data.items_data:
                self.items.append(c_inputItem_compact(self.frm_data.interior,self,item))
                self.items[-1].pack(fill=Y,padx=1,pady=1)
        except: raise
    
    def job_end(self):
        try:    self.frm_command.children["btn_transfer"].configure(state='disabled')
        except: pass