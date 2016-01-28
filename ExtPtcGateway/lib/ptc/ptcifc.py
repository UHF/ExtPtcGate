#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      f.uhlenbruck
#
# Created:     28.01.2015
# Copyright:   (c) f.uhlenbruck 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#global imports
import subprocess

#project imports


#module imports

#module defines
PTCIFC_ERR_COM = 1

class ptcifc:
    def __init__(self):
        try:
            self.__create()
        except:
            raise

    def __msg_status__(self,message,globalpercent,subpercent):
        """Output for status information"""
        if __name__ == '__main__':
            print(message,"\n"," Global: ",globalpercent, " Sub: ",subpercent)

    def __create(self):
        self.__msg_status__("Check PTC connection",0,0)
        try:
            self.Send('im servers --showVersion')
            if 0==len(self.out):
                raise Exception(PTCIFC_ERR_COM)
            self.user = self.out[0:self.out.find("@")]
        except:
            self.__msg_status__("No PTC connection",0,0)
            raise
        else:
            self.__msg_status__("PTC connection valid",0,0)


    def Send(self,command):
        try:
            self.cmd = command
            print (command)
            p = subprocess.Popen(command, stdout=subprocess.PIPE,shell=True)
            (out,err) = p.communicate()
            p.wait()
            if None == err:
                self.err = None
            else:
                self.err = err.decode("iso-8859-1")
            if None == out:
                self.out = None
                self.outitems = None
            else:
                self.out = out.decode("iso-8859-1")
                self.outitems = self.out.splitlines()
        except:
            raise
        else:
            return self.out.strip()



def main():
    try:
        PtcIfc = ptcifc()
        """ #load all Querys
        PtcIfc.Send('im queries --fields=id,name,queryDefinition')
        #view a query
        #PtcIfc.cmd.Send('im viewquery "[FUH] Test"')
        #create a query... create have no reply
        PtcIfc.Send('im viewquery "tempquery" --queryDefinition ')
        if(0==len(PtcIfc.out)):
            PtcIfc.Send('im createquery --name="tempquery"')
        PtcIfc.Send('im editquery --queryDefinition=(field[ID]=30900) "tempquery"')
        PtcIfc.Send('im viewquery "tempquery" --queryDefinition')
        print(PtcIfc.outitems[10])
        print(PtcIfc.out)"""
        PtcIfc.Send("im viewitem 30844")
        print(PtcIfc.out)

    except:
        raise
    pass

if __name__ == '__main__':
    main()
