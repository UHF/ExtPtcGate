#!/usr/bin/env python
# -*- coding: utf8 -*-

#-------------------------------------------------------------------------------
# Name:         Doc.py
# Purpose:
#
# Author:      f.uhlenbruck
#
# Created:     27.01.2015
# Copyright:   (c) f.uhlenbruck 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#global imports
import os
import subprocess
import threading
from threading import *
from queue import *
import time
import datetime
import tkinter
from tkinter import IntVar, StringVar, filedialog, BooleanVar


from lib.d_global import *
from lib.c_gw_wrapper import *
from lib.c_rif_doc import *
from lib.ptc.ptc import *


def run_os_cmd(command):
    cmd = command
    p = subprocess.Popen(command, stdout=subprocess.PIPE,shell=True)
    (out,err) = p.communicate()
    p.wait()
    return (out,err)

class c_itemData(tkinter.Variable):
    def __init__(self,config_data):
        try:    
            super().__init__()
            self.config_data = config_data
            self.active=BooleanVar()
            self.valide=BooleanVar()
            self.file=StringVar()
            self.file.trace('w',self.__file_changed)
            self.file_rw1=StringVar()
            self.rif_id=StringVar()
            self.ptc_id=StringVar()
            self.transfered=StringVar()
            self.logfile = StringVar()
            self.mapping=StringVar()
        except: raise
    
    def __file_changed(self,*args):
        try:
            file = self.file.get()
            log_name = file[:-len(INFILE_ENDING)]+LOGFILE_TAG+LOGFILE_ENDING
            self.logfile.set(log_name)
            if(os.path.isfile(self.config_data.input_dir.get()+"/"+log_name)==False):
                log = open(self.config_data.input_dir.get()+"/"+self.logfile.get(), mode='w')
                log.close()
            pass
        except: raise
        
    def get_save_data(self):
        savedata = {}
        try:
            savedata.update({"active":self.active.get()})
            savedata.update({"file":self.file.get()})
            savedata.update({"rif_id":self.rif_id.get()})
            savedata.update({"ptc_id":self.ptc_id.get()})
            savedata.update({"mapping":self.mapping.get()})
            savedata.update({"file_rw1":self.file_rw1.get()})
            savedata.update({"transfered":self.transfered.get()})
        except: raise
        return savedata

    def restore_data(self,savedata):
        try:
            self.file.set(savedata["file"])
        except:pass
        try:
            self.rif_id.set(savedata["rif_id"])
        except:pass
        try:
            self.ptc_id.set(savedata["ptc_id"])
        except: pass
        try:
            if(savedata["active"]==True):  self.active.set(True)
            else:                           self.active.set(False)
        except: raise
        try:
            self.mapping.set(savedata["mapping"])
        except: pass
        try:
            self.file_rw1.set(savedata["file_rw1"])
        except: pass
        try:
            self.transfered.set(savedata["transfered"])
        except: pass
        
    def write_log(self,command,text):
        try:
            logfile = open(self.config_data.input_dir.get()+"/"+self.logfile.get(), mode='a')
            logfile.write("--------------------------------\n")
            logfile.write(datetime.datetime.now().__str__())
            logfile.write(":")
            logfile.write(command.__str__())
            logfile.write("\n")
            logfile.write(text.__str__())
            logfile.write("\n\n")
            logfile.close()
            
        except: raise
    def cmd_scan_for_files(self):
        try:
            self.cmd_read_rif_id()
            folder = self.config_data.input_dir.get()+'/'
            infile_name = self.file.get()
            r1_name = infile_name[:-len(INFILE_ENDING)]+INFILE_REWORK_1_TAG+INFILE_ENDING
            mapping_name = infile_name[:-len(INFILE_ENDING)]+MAPPINGFILE_TAG+MAPPINGFILE_ENDING
            
            if(os.path.exists(folder+r1_name)):
                self.file_rw1.set(r1_name)
            else:
                self.file_rw1.set("")
            if(os.path.exists(folder+mapping_name)):
                self.mapping.set(mapping_name)
            else:
                self.mapping.set("")          
        except:
            self.write_log("scan_for_files","Fail") 
            raise
        else:   self.write_log("scan_for_files","Pass") 

    def cmd_view_log(self):
        try:
            file = self.logfile.get()
            if(file!=""):
                folder  = self.config_data.input_dir.get()
                command = self.config_data.text_edit.get()+" "+folder+"/"+file
                (out,err) = run_os_cmd(command)
        except: raise
        
    def cmd_compare_file(self):
        try:
            out =""
            err = ""
            folder  = self.config_data.input_dir.get()
            file1   = self.file.get()
            file2 = self.file_rw1.get()
            compare = '"'+self.config_data.file_compare.get()+'"'
            command = compare+' "'+folder+"/"+file1+'" "'+folder+"/"+file2+'"'
            (out,err) = run_os_cmd(command)
        except: 
            self.write_log("compare_file","Fail")
            raise
        else:   self.write_log("compare_file",out.__str__()+"\n"+err.__str__())
        
    def cmd_compare_mapping(self):
        try:
            out =""
            err = ""
            folder  = self.config_data.input_dir.get()
            file1   = self.config_data.template.get()
            file2   = self.mapping.get()
            compare = '"'+self.config_data.file_compare.get()+'"'
            command = compare+" "+file1+" "+folder+"/"+file2
            (out,err) = run_os_cmd(command)
        except: 
            self.write_log("compare_mapping","Fail")
            raise
        else:   self.write_log("compare_mapping",out.__str__()+"\n"+err.__str__())
            
    def cmd_edit_mapping(self):
        try:
            out=""
            err=""
            file = self.mapping.get()
            if(file != ""): 
                if(self.config_data.gw_mapping_gui.get() ==True):
                    """call gateway coonfig gui"""
                    gw=c_gw_wrapper()
                    (out,err) = gw.edit_mapping(self.config_data,self)
                else:
                    """call text editor"""
                    folder  = self.config_data.input_dir.get()
                    command = self.config_data.text_edit.get()+" "+folder+"/"+file
                    (out,err) = run_os_cmd(command)
            pass
            
        except: 
            self.write_log("edit_mapping","Fail")
            raise
        else:   self.write_log("edit_mapping",out.__str__()+"\n"+err.__str__())

    def cmd_validate(self):
        try:
            result = ""
            if(self.file_rw1.get() =="" ):       result = False
            if(self.mapping.get() ==""):         result = False
            if(result != False):                 result = True 
            self.valide.set(result)
        except: 
            self.write_log("validate","Fail")
            raise
        else:   self.write_log("validate","")
        return result
    
    def cmd_transfer(self): 
        try:
            gw=c_gw_wrapper()
            (out,err) = gw.transfer(self.config_data,self)
            
        except: 
            self.write_log("transfer","Fail")
            raise
        else:   self.write_log("transfer",out.__str__()+"\n"+err.__str__())
        self.cmd_read_ptc_id()
    
    def cmd_read_rif_id(self):
        try:
            folder  = self.config_data.input_dir.get()
            rif = c_rif_doc(folder+"/"+self.file.get())
            docinfo = rif.cmd_create_doc_info()
            rifid= docinfo[RIFDOC_TAG_ID]
            self.rif_id.set(rifid)
        except: 
            self.write_log("read_rif_id","Fail: no rif_id found")
            raise
        else:   self.write_log("read_rif_id",rifid)
    
    def cmd_read_ptc_id(self):
        try:
            ptcid = ""
            p = ptc()
            doc = p.GetDocumentbyRIFID(self.rif_id.get())
            ptcid=doc["ID"]
            self.ptc_id.set(doc["ID"])
        except: 
            self.write_log("read_ptc_id","Fail: no ptc_id found")
            raise
        else:   self.write_log("read_ptc_id",ptcid)
    
    def cmd_finalize(self):
        try:
            if(self.ptc_id.get()==""): self.cmd_read_ptc_id()
            self.__fix_mapping_issues()
            self.__push_files_to_ptc()
        except: 
            self.write_log("cmd_finalize","Fail")
            raise
        else:   self.write_log("read_ptc_id","Pass")
    
    def __push_files_to_ptc(self):
        try:
            p =ptc()
            p.cmd_update_attachment(self.ptc_id.get(),"RIF_Attachments",self.config_data.input_dir.get(),self.logfile.get(),"ImportLog.txt","Log from ExtPtcGateway")
            pass
        except: 
            self.write_log("push_files_to_ptc","Fail: no rif_id found")
            raise
        else:   self.write_log("push_files_to_ptc","Pass")
    
    def __fix_mapping_issues(self):
        try:
            """
            Get Module Summary
            """
            folder  = self.config_data.input_dir.get()
            infile = open(folder+"/"+self.file.get(),mode='r')
            data = infile.read()
            infile.close()
            idx= data.find("VALUE-Module Summary")
            module_summary=""
            if(idx>=0):
                start_idx= data.find("<XHTML-CONTENT>",idx)+len("<XHTML-CONTENT>")
                end_idx  = data.find("</XHTML-CONTENT>",idx)
                module_summary = data[start_idx:end_idx]
                module_summary = module_summary.replace("rif-xhtml:", "")
                module_summary = module_summary.replace("<div>","")
                module_summary = module_summary.replace("</div>","")
                """
                module_summary = module_summary.replace("<br/>","\n")
                print(module_summary)
                """
                module_summary = module_summary.replace("<","^<")
                module_summary = module_summary.replace(">","^>")
                
                p= ptc()
                p.cmd_write_notes(self.ptc_id.get(),module_summary)
                pass
            
        except: 
            self.write_log("fix_mapping_issues","Fail")
            raise
        else:   self.write_log("fix_mapping_issues","Pass")
    def cmd_auto_rework(self):
        try:
            folder = self.config_data.input_dir.get()+"/"
            infile_name = self.file.get()
            outfile_name = infile_name[:-len(INFILE_ENDING)]+INFILE_REWORK_1_TAG+INFILE_ENDING
            infile = open(folder+infile_name,mode='r')
            data = infile.read()
            infile.close()
            ''' relpace .ole with .png
            data = data.replace('.ole','.png')
            combine Linksets
            '''
            rif = c_rif_doc(folder+infile_name)
            types = rif.cmd_read_types_list()
            first_hit=True
            secound_hit = True
            type_id = ""
            replace_ids=[]
            
            for type in types:
                hit=type[RIFDOC_TAG_NAME].__str__().find("LINK-TYPE")
                if(hit >= 0):
                    if(first_hit==True):
                        first_hit=False
                        '''Replace Link type name
                        '''
                        
                        type_id = type[RIFDOC_TAG_ID].__str__()
                        name= 'DOORS_LINK-TYPE'
                        data = data.replace(type[RIFDOC_TAG_NAME].__str__(),name)
                        data = data.replace(type[RIFDOC_TAG_Description].__str__(),name)
                        
                    else:
                        '''find and remove old type definition
                        '''
                        start_idx=-1
                        end_idx=-1
                        hit = data.find(type[RIFDOC_TAG_NAME].__str__())
                        starttag = "<"+RIFDOC_TAG_Type+">"
                        start_idx = data.rfind(starttag,0,hit)
                        endtag = "</"+RIFDOC_TAG_Type+">"
                        end_idx = data.find(endtag,hit)+len(endtag)
                        data=data[:start_idx]+data[end_idx:]
                        
                        '''replace type ids
                        '''
                        old_id = type[RIFDOC_TAG_ID].__str__()
                        data = data.replace(old_id,type_id)
                        data = data.replace(type[RIFDOC_TAG_NAME].__str__(),name)
                        data = data.replace(type[RIFDOC_TAG_Description].__str__(),name)
                        
            outfile = open(folder+"/"+outfile_name,mode='w')
            outfile.write(data)
            outfile.close()
            self.file_rw1.set(outfile_name)
        except: 
            self.write_log("auto_rework","Fail")
            raise
        else:   self.write_log("auto_rework","")

    def cmd_create_mapping(self):
        try:
            folder = self.config_data.input_dir.get()+"/"
            itemfile_name  = self.file.get()
            templatefile   = self.config_data.template.get()
            outfile_name = itemfile_name[:-len(INFILE_ENDING)]+MAPPINGFILE_TAG+MAPPINGFILE_ENDING
            infile = open(templatefile,mode='r')
            data = infile.read()
            data = data.replace('mapping name="Transfer_DOORSToIntegrity_mapping"',
                                'mapping name="'+outfile_name[:-len(MAPPINGFILE_ENDING)]+'"')
            infile.close()
            outfile = open(folder+outfile_name,mode='w')
            outfile.write(data)
            outfile.close()
            self.mapping.set(outfile_name)
        except: 
            self.write_log("create_mapping","Fail")
            raise
        else:   self.write_log("create_mapping","")

class c_configData(tkinter.Variable):
    def __init__(self):
        super().__init__()
        self.max_threads   = IntVar()
        self.ptc_project   = StringVar()
        self.ptc_client_dir= StringVar()
        self.rif_bat       = StringVar()
        self.text_edit     = StringVar()
        self.file_compare  = StringVar()
        self.gw_mapping_gui= BooleanVar()
        self.gw_gui        = BooleanVar()
        self.gw_all_yes    = BooleanVar()
    
        self.template      = StringVar()
        self.input_dir     = StringVar()

        self.items_data    = []
        self.job_data      = c_jobData(self)
        
    def __checkFileAddValid(self,filename):
        result = False
        try:
            ending =  filename[-len(INFILE_ENDING):]
            purename = filename[:-len(INFILE_ENDING)]
            rw1 = purename[-len(INFILE_REWORK_1_TAG):]
            mapping = purename[-len(MAPPINGFILE_TAG):]

            if((ending == INFILE_ENDING) and
                (rw1 != INFILE_REWORK_1_TAG) and
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
        
    def get_save_data(self):
        try:
            savedata = {}
            savedata.update({"PtcProject":self.ptc_project.get()})
            savedata.update({"PtcClientDir":self.ptc_client_dir.get()})
            savedata.update({"MaxThreads":self.max_threads.get()})
            savedata.update({"RifBat":self.rif_bat.get()})
            savedata.update({"TextEdit":self.text_edit.get()})
            savedata.update({"FileCompare":self.file_compare.get()})
            savedata.update({"Template":self.template.get()})
            savedata.update({"GwGui":self.gw_gui.get()})
            savedata.update({"GwMappingGui":self.gw_mapping_gui.get()})
            savedata.update({"GwAllYes":self.gw_all_yes.get()})
            savedata.update({"InputDir":self.input_dir.get()})
        
            items_savedata=[]
            for item in self.items_data:
                items_savedata.append(item.get_save_data())
            savedata.update({"items":items_savedata})    
            return savedata
        except: raise
    
    def restore_data(self,savedata=None):
        try:    self.ptc_project.set(savedata["PtcProject"])
        except: pass
        try:    self.ptc_client_dir.set(savedata["PtcClientDir"])
        except: pass
        try:    self.max_threads.set(savedata["MaxThreads"])
        except: self.max_threads.set(20)
        try:    self.rif_bat.set(savedata["RifBat"])
        except: pass
        try:    self.text_edit.set(savedata["TextEdit"])
        except: pass
        try:    self.file_compare.set(savedata["FileCompare"])
        except: pass
        try:    self.gw_gui.set(savedata["GwGui"])
        except: pass
        try:    self.gw_mapping_gui.set(savedata["GwMappingGui"])
        except: pass
        try:    self.gw_all_yes.set(savedata["GwAllYes"])
        except: pass
        try:    self.template.set(savedata["Template"])
        except: pass
        try:    self.input_dir.set(savedata["InputDir"])
        except: pass
        
        try: 
            self.items_data = []
            for item in savedata["items"]:
                    self.items_data.append(c_itemData(self))
                    self.items_data[-1].restore_data(item)
        except: pass
        
    def cmd_select_rifbat(self):
        filename = filedialog.askopenfilename(filetypes=[('Rif.bat', '.bat')],title="Select PTC Gateway Batch file")
        if(filename != ''):
            self.rif_bat.set(filename)

    def cmd_select_template(self):
        filename = filedialog.askopenfilename(filetypes=[('Gateway Mapping Template', '.xml')],title="Select PTC Gateway Mapping Template")
        if(filename != ''):
            self.template.set(filename)

    def cmd_select_textedit(self):
        filename = filedialog.askopenfilename(filetypes=[('Text Editor', '.*')],title="Select Text Editor")
        if(filename != ''):
            self.text_edit.set(filename)
    def cmd_select_filecompare(self):
        filename = filedialog.askopenfilename(filetypes=[('File Compare tool', '.*')],title="Select File Compare tool")
        if(filename != ''):
            self.file_compare.set(filename)
    def cmd_select_ptc_client(self):
        foldername = filedialog.askdirectory(title="Select PTC Client directory")
        if(foldername != ''):
            self.ptc_client_dir.set(foldername)

    def cmd_select_input_dir(self):
        foldername = filedialog.askdirectory(title="Select Input directory")
        if(foldername != ''):
            self.input_dir.set(foldername)
        
 
    def cmd_validate_config(self):
        try:
            result = False
            text   = ""
            temp = self.max_threads.get()
            if(temp < 0):       self.max_threads.set(0)
            if(temp > 15):      self.max_threads.set(15)
            temp = self.ptc_project.get()
            if((temp == "") or (temp.find("/") <0)):
                text=text+"PTC Project invalid\n"
            if((os.path.exists(self.ptc_client_dir.get())==False) or
                (os.path.isdir(self.ptc_client_dir.get())==False)):
                text=text+"PTC Client directory invalid\n"
            if((os.path.exists(self.rif_bat.get())==False) or
                (os.path.isfile(self.rif_bat.get())==False)):
                text=text+"PTC Gateway(Rif.bat) invalid\n"
            if((os.path.exists(self.text_edit.get())==False) or
                (os.path.isfile(self.text_edit.get())==False)):
                text=text+"Text Editor invalid\n"
            if((os.path.exists(self.file_compare.get())==False) or
                (os.path.isfile(self.file_compare.get())==False)):
                text=text+"File Compare invalid\n"
            if((os.path.exists(self.template.get())==False) or
                (os.path.isfile(self.template.get())==False)):
                text=text+"Mapping Template invalid\n"
            if((os.path.exists(self.input_dir.get())==False) or
                (os.path.isdir(self.input_dir.get())==False)):
                text=text+"Input directory invalid\n"
        except: raise
        else:
            if(text==""):
                text ="Ok"
                result = True
        return (result,text)
    
    def cmd_select_all(self):
        try:
            for item in self.items_data:
                item.active.set(True)
        except: raise
        
    def cmd_deselect_all(self):
        try:
            for item in self.items_data:
                item.active.set(False)
        except: raise
        
    def cmd_delete(self):
        try:
            idx=0
            while (idx<len(self.items_data)):
                if(self.items_data[idx].active.get() == True):
                    self.items_data.pop(idx)
                else : idx+=1
        except: raise

    def cmd_add_files(self):
        try:
            foldername = self.input_dir.get()
            if(len(foldername) > 0):
                self.items_data = []
                for file in os.listdir(foldername):
                    if(os.path.isfile(foldername+'/'+file)):
                        if(self.__checkFileAddValid(file) == True):
                            if(self.__checkFileAvalible(file)== False):
                                self.items_data.append(c_itemData(self))
                                self.items_data[-1].file.set(file)
                self.cmd_select_all()
                self.cmd_scan_for_files()
                self.cmd_deselect_all()
        except: raise
        pass
    
    def cmd_validate_item(self):
        try:    
            result = ""
            for item in self.items_data:
                if(item.active.get() == True):
                    if(item.cmd_validate()==False): result = False
            if(result != False):    result = True
        except: raise
        return result
    def cmd_finalize(self):
        try:    self.job_data.start_job("finalize")
        except: raise
        
    def cmd_scan_for_files(self):
        try:
            self.job_data.start_job("scan_for_files")
        except: raise
    
    def cmd_auto_rework(self):
        try:    self.job_data.start_job("auto_rework")
        except: raise
    
    def cmd_transfer(self):
        try:    self.job_data.start_job("transfer")
        except: raise

    def cmd_create_mapping(self):
        try:    self.job_data.start_job("create_mapping")
        except: raise

    def cmd_read_rif_id(self):
        try:     self.job_data.start_job("read_rif_id")
        except: raise
    
    def cmd_prepare_files(self):
        try:     self.job_data.start_job("prepare_files")
        except: raise

                
class c_jobData(tkinter.Variable):
    def __init__(self,config_data):
        super().__init__()
        self.config_data = config_data
        
        self.job_queue = Queue()
        self.job_worker=[]
        
        self.job_title=StringVar()
        self.jobs_total= IntVar()
        self.jobs_open = IntVar()
        self.jobs_running = IntVar()
        self.jobs_closed = IntVar()
        self.active_workers = IntVar()

    def start_job(self,job_name):
        try:
            self.job_title.set(job_name)
            self.jobs = []
            self.job_queue = None
            self.job_queue = Queue()

            for item in self.config_data.items_data:
                if(item.active.get() == True):
                    self.job_queue.put(item)
                    
            self.jobs_total.set(self.job_queue.unfinished_tasks)
            self.job_active=True
            while((len(self.jobs)<self.config_data.max_threads.get()) and
                  (len(self.jobs)<self.jobs_total.get())):
                self.jobs.append(Thread(target=self.__t_job_worker))
                self.jobs[-1].start()
            self.job_timer = Thread(target=self.__t_job_watch)
            self.job_timer.start()
            self.job_join = Thread(target=self.__t_job_join)
            self.job_join.start()

        except: raise

    def __end_jobs(self):
        self.__calc_status()
        pass
    def __calc_status(self):
        try:
            unfinished=self.job_queue.unfinished_tasks
            open      =len(self.job_queue.queue)
            running   =unfinished-open
            finished  =self.jobs_total.get()-(open+running)
            self.jobs_open.set(open)
            active_workers=0
            for job in self.jobs:
                if(job._is_stopped==False):
                    active_workers = active_workers+1
            self.jobs_running.set(running)
            self.jobs_closed.set(finished)
            self.active_workers.set(active_workers)  
        except: raise
        
    def __t_job_watch(self):
        try:
            while(self.job_active==True):
                self.__calc_status()
                time.sleep(1)
            self.__calc_status()
            self.__end_jobs()
        except: raise
    
    def __t_job_join(self):
        for job in self.jobs:
			time.sleep(1)
            job.join()
        self.job_active=False

    def __t_job_worker(self):
        while(self.job_queue.empty()==False):
            try:
                item = self.job_queue.get(timeout=0.2)
                self.__exec_job(item)
                self.job_queue.task_done()
                time.sleep(1)
            except: pass
            
    def __exec_job(self,item):
        try:
            jobtitle = self.job_title.get()
            if(jobtitle == "auto_rework"):      item.cmd_auto_rework()
            elif(jobtitle == "transfer"):       item.cmd_transfer()
            elif(jobtitle == "create_mapping"): item.cmd_create_mapping()
            elif(jobtitle == "scan_for_files"): item.cmd_scan_for_files()
            elif(jobtitle == "read_rif_id"):    item.cmd_read_rif_id()
            elif(jobtitle == "prepare_files"):
                item.cmd_read_rif_id()
                item.cmd_auto_rework()
                item.cmd_create_mapping()
            elif(jobtitle=="validate_items"):   
                item.cmd_validate()
                item.cmd_finalize()
            elif(jobtitle=="finalize"):         item.cmd_finalize()
        except: raise