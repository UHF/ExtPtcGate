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
import re
import xml.etree.ElementTree as etree

#global defines
RIFDOC_ERROR_NO_RIF_FILE        = 1
RIFDOC_ERROR_NO_VERSION         = 1
RIFDOC_ERROR_UNVALID_VERSION    = 1
RIFDOC_ERROR_NO_LINKS           = 1
RIFDOC_ERROR_NO_LINK_SOURCE     = 1
RIFDOC_ERROR_NO_LINK_TARGET     = 1

RIFDOC_ERROR            = True
RIFDOC_NOERROR          = False

RIFDOC_TAG_RIF              = "RIF"
RIFDOC_TAG_VERSION          = "VERSION"
RIFDOC_TAG_LINKS            = "SPEC-RELATIONS"
RIFDOC_TAG_LINK             = "SPEC-RELATION"
RIFDOC_TAG_Source           = "SOURCE"
RIFDOC_TAG_Target           = "TARGET"
RIFDOC_TAG_Objects          = "SPEC-OBJECTS"
RIFDOC_TAG_Object           = "SPEC-OBJECT"
RIFDOC_TAG_Object_Ref   	= "SPEC-OBJECT-REF"
RIFDOC_TAG_Datatypes        = "DATATYPES"
RIFDOC_TAG_Types            = "SPEC-TYPES"
RIFDOC_TAG_Type             = "SPEC-TYPE"
RIFDOC_TAG_Type_Reference   = "SPEC-TYPE-REF"
RIFDOC_TAG_Groups           = "SPEC-GROUPS"
RIFDOC_TAG_Group            = "SPEC-GROUP"
RIFDOC_TAG_Documents        = "SPEC-HIERARCHY-ROOTS"
RIFDOC_TAG_Document         = "SPEC-HIERARCHY-ROOT"
RIFDOC_TAG_NAME             = "LONG-NAME"
RIFDOC_TAG_ID               = "IDENTIFIER"
RIFDOC_TAG_Description      = "DESC"
RIFDOC_TAD_DOCUMENT_ATTRIBUTES  = "ATTRIBUTE-VALUE-EMBEDDED-DOCUMENT"

RIFDOC_SUPPORTED_VERSION    = ["1.1a"]

class c_rif_doc(object):
    def __init__(self,filename=None):
        try:
            if(filename):
                if(filename!=""):
                    self.Open(filename)
        except: raise

    def __unpack_item(self,element):
        try:
            unpacked={}
            for item in element:
                if len(item) > 1:
                    unpacked[item.tag[len(self.namespace):]]=self.__unpack_item_list(item)
                elif (item.tag[len(self.namespace):] == "XHTML-CONTENT"):
                    unpacked[item.tag[len(self.namespace):]]=item.text
                elif len(item.text.strip()) > 0:
                    unpacked[item.tag[len(self.namespace):]]=item.text
                else:
                    unpacked[item.tag[len(self.namespace):]]=self.__unpack_item(item)
        except:
            raise
        else:
            return unpacked

    def __unpack_item_list(self,element):
        try:
            unpacked=[]
            for item in element:
                unpacked.append(self.__unpack_item(item))
            return unpacked
        except:
            raise
        else:
            return unpacked

    def __check_format(self):
        root = etree.Element
        try:
            root = self.tree.getroot()
            if None == re.search(RIFDOC_TAG_RIF,str.upper(root.tag)):
                 raise Exception(RIFDOC_ERROR_NO_RIF_FILE)
            self.namespace = root.tag[0:root.tag.find(RIFDOC_TAG_RIF)]
        except:     raise
        else:       pass


    def __check_version(self):
        """Checks the RIF Version of a open Document"""
        root = etree.Element
        version = None
        try:
            root = self.tree.getroot()
            tag = self.namespace+RIFDOC_TAG_VERSION
            self.version = root.find(tag)
            if None == self.version:
                raise Exception(RIFDOC_ERROR_NO_VERSION)
        except: raise
        else:   pass

    def Open(self,filename):
        """Open a file and validate if its a RIF file"""
        try:
            self.filename = filename
            self.tree = etree.parse(filename)

            self.__check_format()
            self.__check_version()
        except: raise
        else:   pass

    def Write(self,filename):
        try:    self.tree.write(filename)
        except:raise

    def cmd_create_doc_info(self):
        root = etree.Element
        docimfo = []
        doc = []
        try:
            root = self.tree.getroot()
            docs = list(root.iter(self.namespace+RIFDOC_TAG_Document))
            if 1 > len(docs):
                raise Exception("to many document roots")
            else:
                docinfo = self.__unpack_item(docs[0])
            pass
        except:
            raise
        else:
            return docinfo

    def cmd_read_types_list(self):
        root  = self.tree.getroot()
        types = list(root.iter(self.namespace+RIFDOC_TAG_Type))
        types_list=[]
        for type in types:
            types_list.append(self.__unpack_item(type))
        pass
        return types_list

    def cmd_read_document_attributes(self):
        root  = self.tree.getroot()
        specs = list(root.iter(self.namespace+RIFDOC_TAG_Group))
        if(len(specs)>1): raise Exception("to many documents")
        spec = specs[0]
        attributes = list(spec.iter(self.namespace+RIFDOC_TAD_DOCUMENT_ATTRIBUTES))
        attr_list = []
        for attribute in attributes:
            attr_list.append(self.__unpack_item(attribute))
        pass
        return attr_list
    
if __name__ == "__main__":
    def main():
        doc = c_rif_doc(filename="g:/py_prj/rif_doc/wrk/System_Requirement_Specification_00072f43_rw1.xml")
        doc.cmd_combine_link_types("DOORS-LINKS-TYPE")
        pass

    main()