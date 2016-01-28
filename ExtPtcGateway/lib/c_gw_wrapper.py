import os
import subprocess
import datetime

from tkinter import messagebox
from lib.d_global import *


class c_gw_wrapper(object):
    filename = "custom_rif.bat"
    def __init__(self):
        pass

    def __create_rifbat(self,config_data):
        try:
            clientdir  = config_data.ptc_client_dir.get().replace('/','\\')
            rifdir     = os.path.dirname(config_data.rif_bat.get()).replace('/','\\')
            configdir  = config_data.input_dir.get().replace('/','\\')

            rifbat = open(config_data.rif_bat.get(),mode='r')
            new_rifbat = rifbat.read()
            rifbat.close()

            lines = new_rifbat.splitlines()
            new_rifbat=""
            for line in lines:
                pos = line.find("MKS_INTEGRITY_CLIENT_DIRECTORY=")
                if(pos>=0):
                    line = line[:pos+len("MKS_INTEGRITY_CLIENT_DIRECTORY=")] + clientdir
                pos = line.find("RIF_DIRECTORY=")
                if(pos>=0):
                    line = line[:pos+len("RIF_DIRECTORY=")] + rifdir
                pos = line.find("ITEM_MAPPER_CONFIGURATION_DIRECTORY=")
                if(pos>=0):
                    line = line[:pos+len("ITEM_MAPPER_CONFIGURATION_DIRECTORY=")] + configdir
                pos = line.find("JAVA_LIBRARY_PATH=")
                if(pos>=0):
                    line =  line[:pos+len("JAVA_LIBRARY_PATH=")] + '"%RIF_DIRECTORY%;' + line[pos+len("JAVA_LIBRARY_PATH="):] + '"'
                pos = line.find('"%JAVA_LIBRARY_PATH%"')
                if(pos>=0):
                    line =  line[:pos] + '%JAVA_LIBRARY_PATH%' + line[pos+len('"%JAVA_LIBRARY_PATH%"'):]
                new_rifbat = new_rifbat+line+"\n"

            file = open(config_data.input_dir.get()+"/"+self.filename,mode='w')
            file.write(new_rifbat)
            file.close()
        except: raise

    def __run_cmd(self,config_data,command,item):
        try:
            folder  = config_data.input_dir.get()
            if(os.path.exists(folder+"/"+self.filename)==False):
                self.__create_rifbat(config_data)
            command = folder+"/"+self.filename+" "+command
            p = subprocess.Popen(command, stdout=subprocess.PIPE,shell=True)
            (out,err) = p.communicate()
            p.wait()
            print("\n****************************\n")
            print(out)
        except: raise
        return (out,err)

    def edit_mapping(self,config_data,item):
        command = "configure"
        folder  = config_data.input_dir.get()
        folder = folder.replace('/','\\')
        
        if (item.file_rw1.get()!=""):   file = item.file_rw1.get()
        else:                           file = item.file.get()
        file    = ' --rifFile="'+folder+"\\"+file+'"'
        mapping = ' --config="'+folder+"\\"+item.mapping.get()+'"'
        command = command+file+mapping
        return self.__run_cmd(config_data,command,item)

    def transfer(self,config_data,item):
        try:
            item.transfered.set(datetime.datetime.now().__str__())
            out=""
            err=""
            command = "import"
            folder  = config_data.input_dir.get()
            folder  = folder.replace('/','\\')
            file_rw1=item.file_rw1.get()
            file    = ' --rifFile="'+folder+"\\"
            file=file+file_rw1+'"'
            mapping = item.mapping.get()
            mapping = ' --config="'+mapping[:-len(MAPPINGFILE_ENDING)]+'"'
            document= ' --rifDocument="'+item.rif_id.get()+'"'
            project = ' --project="'+config_data.ptc_project.get()+'"'
            gui     = ''
            if(config_data.gw_gui.get() !=True):      
                gui = ' --nogui'
            allyes  = ''
            if(config_data.gw_all_yes.get() ==True):   
                allyes = ' --yesToAll'
            command = command + document + file  + mapping + project + gui + allyes
            (out,err) = self.__run_cmd(config_data,command,item)
            return (out,err)
        except: raise