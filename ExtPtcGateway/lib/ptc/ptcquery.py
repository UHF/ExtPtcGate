#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UhlenbrF
#
# Created:     28.01.2015
# Copyright:   (c) UhlenbrF 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#global imports

#module imports
if __name__ == '__main__':
    from ptcifc import ptcifc
else:
    from lib.ptc.ptcifc import ptcifc

PTCIFCQUERY_ERR_ = 1

class ptcquery:
    def __init__(self):
        try:
            self.ifc = ptcifc()
            self.user = self.ifc.user
        except:
            raise

    def __msg_status__(self,message,globalpercent,subpercent):
        """Output for status information"""
        if __name__ == '__main__':
            print(message,"\n"," Global: ",globalpercent, " Sub: ",subpercent)

    def SetDefiniton(self,definiton):
        try:
            self.__msg_status__("Set Query definition ",0,0)
            self.definiton = definiton
        except:
            self.__msg_status__("Set Query definition fail",0,0)
            raise
        else:
            self.__msg_status__("Set Query definition pass",0,0)

    def SetFields(self,fields):
        try:
            self.__msg_status__("Set Query Fields ",0,0)
            self.field = fields
            fieldcmd=''
            for field in fields:
                fieldcmd = fieldcmd+'"'+field+'",'
            self.fieldcmd = fieldcmd[0:-1]
        except:
            self.__msg_status__("Set Query Fields  fail",0,0)
            raise
        else:
            self.__msg_status__("Set Query Fields  pass",0,0)

    def Run(self):
        try:
            self.__msg_status__("Run Query ",0,0)
            self.ifc.Send('im issues --queryDefinition='+self.definiton+' --fields='+self.fieldcmd)
        except:
            self.__msg_status__("Run Query fail",0,0)
            raise
        else:
            self.__msg_status__("Run Query pass",0,0)
            return self.ifc.out

def main():
    try:
        qr = ptcquery()
        qr.SetDefiniton('(field[RIF_Identifier]contains"LIKE _d37b4db7-eb03-4c3b-8ebe-c0144b99b86a")')
        qr.SetFields(["ID","RIF_Identifier"])
        print(qr.Run())
    except:
        raise

if __name__ == '__main__':
    main()