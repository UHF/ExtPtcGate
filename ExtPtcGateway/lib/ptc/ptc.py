#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UhlenbrF
#
# Created:     02.02.2015
# Copyright:   (c) UhlenbrF 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#lobal import

#project import

#module import
if __name__ == '__main__':
    from ptcifc import ptcifc
    from ptcquery import ptcquery
    from lib.rif.rif import rif
else:
    from lib.ptc.ptcifc import ptcifc
    from lib.ptc.ptcquery import ptcquery


class ptc():
    def __init__(self):
        try:
            self.ifc = ptcifc()
        except:
            raise
        else:
            pass

    def __msg_status__(self,message,globalpercent,subpercent):
        """Output for status information"""
        if __name__ == '__main__':
            print(message,"\n"," Global: ",globalpercent, " Sub: ",subpercent)

    def GetDocumentbyRIFID(self,rifid):
        try:
            ptcdoc = {}
            self.__msg_status__("GetDocumentIDbyRIFID"+rifid,0,0)
            out=self.ifc.Send('im issues --fields="ID","RIF_Identifier","Summary","Type" --queryDefinition=(field["RIF_Identifier"]contains"LIKE '+rifid+'")')
            out = out.strip()
            ptcdoc["ID"],ptcdoc["RIF_ID"],ptcdoc["Summary"],ptcdoc["Type"]=out.split('\t')
        except:
            self.__msg_status__("GetDocumentIDbyRIFID fail",0,0)
            raise
        else:
            self.__msg_status__("GetDocumentIDbyRIFID pass",0,0)
        return ptcdoc
    
    def cmd_write_notes(self,ptc_id,text):
        try:
            out= self.ifc.Send("im editissue --richContentField=ALM_Notes='"+text+"' "+ptc_id)
        except:raise
        
    def cmd_update_attachment(self,ptc_id,field,path,file,name,description): 
        try:
            out = self.ifc.Send("im editissue --updateAttachment='field="+field+",path="+path+"/"+file+",name="+name+",summary="+description+"' "+ptc_id)
        except:raise
            
    
def main():
    p=ptc()
    #p.GetDocumentbyRIFID("_d37b4db7-eb03-4c3b-8ebe-c0144b99b86a")
    #p.Create_RifHashListByDocID("30844")
    #_rif = PTC_Gateway()
    #_rif.Open("z:\\2015-01-22_07-03-33-139_export\\Electronics_Requirement_Specification_00072fa6.xml")
    #riflinks = _rif.Create_Link_List()
    #p.Apply_Relationships(riflinks)
    print(p.ifc.Send("im viewissue --showRelationships 32817"))
    print(p.ifc.Send('im editissue --addRelationships="Decomposed From":18808 32817'))
    print(p.ifc.Send("im viewissue --showRelationships 32817"))

    #p.add_relationship("32817","18808","Decomposed From")

    pass

if __name__ == '__main__':
    main()
