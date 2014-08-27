#!/usr/bin/env python


from JumpScale import j

j.application.start("jsexamples:datamine")

import pymongo
from pymongo import *
from datetime import datetime
import time
   
    

class Reader():

    def __init__(self,path):        
        self.path=path
        self._db = MongoClient('localhost', 27017)
        self.db = self._db.test_database

    def getdb(self):
        return self.db.test

    def query(self,query):
        db=self.getdb()
        res=db.aggregate([                     
                    {  "$group" :
                        { "_id" : ["$stcity"],
                           "total" : { "$sum" : "$price" }
                        }
                    },                
                    {   "$sort" : { "_id" : 1}},
                    
                ])   
        return res     

    def dump2db(self):
        db=self.db.test
        f = open(self.path, 'r')
        first=f.readline()

        headers=[]
        for item in first.split("|"):
            if item.strip()=="":
                item="id"
            item=item.strip().lower().replace(" ","")
            headers.append(item)

        counter=0
        process=0
        tosend=[]
        for line in f:

            cols=line.split("|")
            ddict={}
            for i in range(len(cols)):
                ret=None
                try:
                    ret=int(cols[i])
                except:
                    pass
                if ret==None and cols[i].find("/")<>-1:
                    if len(cols[i].split("/"))==3:
                        try:
                            ret=int(time.mktime(time.strptime(cols[i], "%m/%d/%Y")))
                        except:                    
                            pass
                if ret==None and cols[i].find("$")<>-1:
                    try:
                        ret=float(cols[i].replace("$","").replace("(","").replace(")","").replace(",",""))
                    except:
                        pass
                try:
                    ret=float(cols[i])
                except:
                    pass

                if ret==None:
                    ret=cols[i].strip()

                ddict[headers[i]]=ret
            tosend.append(ddict)
            counter+=1
            if counter>100:
                process+=1
                counter=0
                print process*100

                db.insert(tosend)
                
                tosend=[]


path="/root/Desktop/bd/taxaudit-on-2013.csv"
reader=Reader(path)
# reader.dump2db()

res=reader.query("group:tax_level ")

from IPython import embed
print "DEBUG NOW ooo"
embed()




j.application.stop()