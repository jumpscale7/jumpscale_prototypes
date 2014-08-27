#!/usr/bin/env python


from JumpScale import j

j.application.start("jsexamples:xlrd")




from xlrd import open_workbook
import xlwt
from datetime import datetime

class XLSSheetFactory():
    def getXLSReader(self,name,excelpath):
        return XLSSheetReader(name,excelpath)
    def getXLSWriter(self,name,excelpath):
        return XLSSheetWriter(name,excelpath)
    
    def getXLSWriterGroup(self,name,format="MYQ",outpath=None):
            return XLSSheetWriterGroup(name,format,outpath)    
    
    

class XLSSheetReader():

    def __init__(self,name,excelpath):
        
        self.name=name
        
        self.workbook = open_workbook(excelpath)
                
        self.dataPath=q.system.fs.joinPaths(q.dirs.varDir,"bizplanner",name)
        self.sheetdef={}
        self.sheetnames=[]
        self.sheets={}

        self.init()   

        

    def init(self):
        for worksheet in self.workbook.sheets():

            wstitle=worksheet.name
            from IPython import embed
            print "DEBUG NOW ooooo"
            embed()
            


path="/root/Desktop/bd/taxaudit-on-2013.xlsx"
xls=XLSSheetReader("test",path)


j.application.stop()