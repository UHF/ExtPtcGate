'''
Created on 16.02.2015

@author: f.uhlenbruck
'''
import platform

from tkinter import Tk, Tcl , ttk , filedialog, PhotoImage, Image, Menu
from tkinter.constants import *
from cgitb import text
import pickle

from lib.d_global import *
from img.d_images import d_images
from gui.c_clientFrame import c_clientFrame

class c_mainFrame(Tk):
    '''
    classdocs
    '''
    def __init__(self,**paras):
        '''
        Constructor
        '''
        try:
            super().__init__(**paras)
            
            self.__check_enviroment()
            self.system = self.tk.call('tk','windowingsystem')
            
            self.__mystyle()
            self.__setup()
            self.__create_children()
            pass
        except: raise
        else: pass

    def __del__(self):
        try: pass
        except: pass
        else: pass

    def __check_enviroment(self):
        try:
            self.py_Version=platform.python_version()
            self.py_Compiler=platform.python_compiler()
            self.py_Build=platform.python_build()

            major,minor,patch = self.py_Version.split(".")
            if (int(major) < MIN_PY_MAJOR_VERSION) or \
               ((int(major) == MIN_PY_MAJOR_VERSION) and \
                (int(minor) < MIN_PY_MINOR_VERSION)):
                raise Exception('Python Version '+MIN_TCL_MAJOR_VERSION+'.'+MIN_TCL_MINOR_VERSION+'.x or higher required')

            self.tcl_Version = Tcl().eval('info patchlevel')
            major,minor,patch = self.tcl_Version.split(".")
            if (int(major) < MIN_TCL_MAJOR_VERSION) or \
               ((int(major) == MIN_TCL_MAJOR_VERSION) and \
                (int(minor) < MIN_TCL_MINOR_VERSION)):
                raise Exception('TCL Version '+MIN_TCL_MAJOR_VERSION+'.'+MIN_TCL_MINOR_VERSION+'.x or higher required')
        except:
            raise

    def __setup(self):
        try:
            self.option_add('*tearOFF',FALSE)
            self.geometry("1024x640+10+10")
            self.configure(title="Extended PTC Gateway")


            pass
        except: pass
        else: pass


    def __create_children(self):
        try:
            self.__create_menue()
            pass
        except: raise
        else: pass

    def __create_menue(self):
        try:
            self.frm_menu=ttk.Frame(self,name="menu")

            ttk.Button(self.frm_menu,name="btn_new_file",text="New",command=self.__on_menu_new_file).pack(side=LEFT)
            ttk.Button(self.frm_menu,name="btn_open_file",text="Open",command=self.__on_menu_open_file).pack(side=LEFT)
            ttk.Button(self.frm_menu,name="btn_save_file",text="Save",state='disabled',command=self.__on_menu_save_file).pack(side=LEFT)
            ttk.Button(self.frm_menu,name="btn_save_as_file",text="SaveAs",state='disabled',command=self.__on_menu_save_as_file).pack(side=LEFT)

            self.frm_menu.pack(side=TOP,fill=X)
            pass
        except: raise
        else: pass

    def __create_client(self,savedata=None):
        try:
            try:
                self.frm_client.destroy()
            except: pass
            self.frm_client = c_clientFrame(self,savedata=savedata,name="client")
            self.frm_client.pack(side=TOP,fill=BOTH,expand=True)
            self.__save_enable()
            pass
        except: raise

    def __on_menu_open_file(self):
        try:
            filename = filedialog.askopenfilename(filetypes=[('ExtGatewayConfig', SAVE_FILE_ENDING)],title="Select Configuration File")
            if(filename):
                self.__load(filename)
            pass
        except: raise

    def __on_menu_new_file(self):
        try:
            self.__create_client()
            pass
        except: raise

    def __on_menu_save_file(self):
        try:
            self.__save(self.filename)
            pass
        except: self.__on_menu_save_as_file()


    def __on_menu_save_as_file(self):
        try:
            filename = filedialog.asksaveasfilename(filetypes=[('ExtGatewayConfig', SAVE_FILE_ENDING)],title="Select Configuration File")
            if(filename):
                if(filename[-len(SAVE_FILE_ENDING):] != SAVE_FILE_ENDING):
                    filename+=SAVE_FILE_ENDING
                self.__save(filename)
            pass
        except: raise

    def cbk_menue_disable(self):
        try:
            self.children["menu"].children["btn_save_file"].config(state='disabled')
            self.children["menu"].children["btn_save_as_file"].config(state='disabled')
            self.children["menu"].children["btn_new_file"].config(state='disabled')
            self.children["menu"].children["btn_open_file"].config(state='disabled')
            pass
        except: raise

    def cbk_menue_enable(self):
        try:
            self.children["menu"].children["btn_save_file"].config(state='normal')
            self.children["menu"].children["btn_save_as_file"].config(state='normal')
            self.children["menu"].children["btn_new_file"].config(state='normal')
            self.children["menu"].children["btn_open_file"].config(state='normal')
            pass
        except: raise

    def __save_enable(self):
        self.children["menu"].children["btn_save_file"].config(state='normal')
        self.children["menu"].children["btn_save_as_file"].config(state='normal')

    def __get_save_data(self):
        return self.frm_client.get_save_data()

    def __restore_data(self,savedata):
        self.__create_client(savedata)
        pass

    def __save(self,filename):
        try:
            savedata = self.__get_save_data()
            self.filename=filename
            f = open(filename,mode="wb")
            s=pickle.dumps(savedata)
            f.write(s)
            f.close()
            pass
        except: raise

    def __load(self,filename):
        try:
            self.filename=filename
            f = open(filename,mode="rb")
            s=f.read()
            f.close()
            savedata = pickle.loads(s)
            self.__restore_data(savedata)
            pass
        except: raise

    def __mystyle(self):
        self.style = ttk.Style()
        
        self.style.configure("TFrame",padding=5,relief=RIDGE)
        self.style.configure("TButton",padding=3,relief=FLAT,padx=2,pady=2)
        self.style.configure("TLable",padding=2,relief=FLAT,padx=2,pady=2)
        
        self.style.configure("TEntry",padding=2,relief=RIDGE,padx=2,pady=2)
        self.style.configure("TCheckbutton",padding=2,relief=RIDGE,padx=2,pady=2)
        
        self.style.configure("ok.TEntry",foreground="green",background="green",padding=3,relief=RIDGE,padx=2,pady=2)
        self.style.configure("err.TEntry",foreground="red",background="red",padding=3,relief=RIDGE,padx=2,pady=2)
        self.style.configure("tbd.TButton", foreground="gray",background="gray",padding=3,relief=FLAT,padx=2,pady=2)
        self.style.configure("warn.TButton", foreground="yellow",background="yellow",padding=3,relief=FLAT,padx=2,pady=2)
        self.style.configure("ok.TButton", foreground="green",background="green",padding=3,relief=FLAT,padx=2,pady=2)
        self.style.configure("err.TButton", foreground="red",background="red",padding=3,relief=FLAT,padx=2,pady=2)
        self.style.configure("option.TButton", foreground="blue",background="blue",padding=3,relief=FLAT,padx=2,pady=2)
        
if __name__ == '__main__':
    import tkinter

    def main():
        app = c_main()
        app.mainloop()
        try:
            app.destroy()
            app.quit()
        except:
            pass
        pass

    main()