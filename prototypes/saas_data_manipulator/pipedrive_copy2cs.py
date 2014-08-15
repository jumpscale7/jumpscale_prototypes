import unicodedata
import sys


from JumpScale import j

j.application.appname = "pipedrive"
j.application.start()

j.config.interactive=True

import json
import requests
import pickle


class PipeDrive():
    def __init__(self,name="unknown",reset=False):
        self.name=name
        self._loadConfig()            
        self.destination=None
        self.persons={}
        self.personsId={}
        self.orgs={}
        self.orgsId={}
        self.pipelines={}
        self.stages={}
        self.deals={}
        self.loadDeals=False
        self.loadOrgs=False
        self.loadPersons=False
        self.loadPipelines=False
        self.loadStages=False
        if reset:
            self.loadDeals=True 
            self.loadOrgs=True
            self.loadPersons=True
            self.loadPipelines=True
            self.loadStages=True
            self.quit()

    def _loadConfig(self):
        cpath=j.system.fs.joinPaths(j.dirs.hrdDir,"pipedrive")
        j.system.fs.createDir(cpath)
        hrd=j.core.hrd.getHRD(cpath)
        
        if not hrd.exists("pipedrive.datapath"):
            j.system.fs.writeFile(j.system.fs.joinPaths(cpath,"main.hrd"),"pipedrive.datapath=%s\n"%j.system.fs.joinPaths(j.dirs.varDir,"pipedrive"))
            hrd=j.core.hrd.getHRD(cpath)
        if not hrd.exists("pipedrive.%s.key"%self.name):
            key=j.console.askString("api key to pipedrive with name:%s\nCan be found at:https://app.pipedrive.com/settings#api\n"%self.name)
            j.system.fs.writeFile(j.system.fs.joinPaths(cpath,"%s.hrd"%self.name),"pipedrive.%s.key=%s\n"%(self.name,key))
            hrd=j.core.hrd.getHRD(cpath)
        
        self.key=hrd.get("pipedrive.%s.key"%self.name)
        self.datapath=hrd.get("pipedrive.datapath")
        j.system.fs.createDir(self.datapath)

    def _getAscii(self,s):
        s=unicode(s)
        return unicodedata.normalize('NFKD', s).encode('ascii','ignore') 

    def _strNormalise(self,s):
        s=self._getAscii(s).strip()
        s=s.replace("mr. ","")
        s=s.replace("  "," ")
        s=s.replace("\n","")
        s=s.replace("-","-")
        s=s.replace("_","-")
        s=s.replace(":","")
        return s

    def _name2key(self,s):
        s=self._strNormalise(s)
        s=s.replace("'","")
        s=s.replace("-","")
        s=s.lower()
        return s

    def _getBaseUrl(self,url):
        return "https://api.pipedrive.com/%s?api_token=%s"%(url,self.key)

    def dealsGet(self,refresh=False):
        if self.deals=={} or refresh==True or self.loadDeals:
            datapath="%s/%s_deals.data"%(self.datapath,self.name)
            if j.system.fs.exists(datapath) and not(refresh==True or self.loadDeals):
                self.deals=pickle.loads(j.system.fs.fileGetContents(datapath))
            else:
                print "refreshdeals"
                data = self._get("v1/deals/",getstatement="start=0&limit=10000&sort_by=title&sort_mode=asc")
                for item in data:
                    # name=self._name2key(item["name"])
                    self.deals[item["id"]]=item
                data=pickle.dumps(self.deals)
                j.system.fs.writeFile(datapath,data)
                self.loadDeals=False

    def personsGet(self,refresh=False):
        if self.persons=={} or refresh==True or self.loadPersons:
            datapath="%s/%s_persons.data"%(self.datapath,self.name)
            if j.system.fs.exists(datapath) and not (refresh==True or self.loadPersons):
                self.persons=pickle.loads(j.system.fs.fileGetContents(datapath))
                for key in self.persons.keys():
                    items=self.persons[key]
                    for item in items:
                        self.personsId[int(item["id"])]=item                        
            else:
                print "refreshpersons"
                data = self._get("v1/persons/",getstatement="start=0&limit=10000&sort_by=name&sort_mode=asc")
                for item in data:
                    name=self._name2key(item["name"])
                    if not self.persons.has_key(name):
                        self.persons[name]=[]
                    self.persons[name].append(item)
                    self.personsId[item["id"]]=item
                data=pickle.dumps(self.persons)
                j.system.fs.writeFile(datapath,data)
                self.loadPersons=False

    def organizationsGet(self,refresh=False):
        if self.orgs=={} or refresh==True or self.loadOrgs:
            datapath="%s/%s_orgs.data"%(self.datapath,self.name)
            if j.system.fs.exists(datapath) and not (refresh==True or self.loadOrgs):
                self.orgs=pickle.loads(j.system.fs.fileGetContents(datapath))
                for key in self.orgs.keys():
                    item=self.orgs[key]
                    self.orgsId[item["id"]]=item                
            else:
                print "refreshorgs"
                data = self._get("v1/organizations/",getstatement="start=0&limit=10000&sort_by=name&sort_mode=asc")
                for item in data:
                    name=self._name2key(item["name"])
                    self.orgs[name]=item
                    self.orgsId[item["id"]]=item
                data=pickle.dumps(self.orgs)
                j.system.fs.writeFile(datapath,data)
                self.loadOrgs=False

    def pipelinesGet(self,refresh=False):
        if self.pipelines=={} or refresh==True or self.loadPipelines:
            datapath="%s/%s_pipelines.data"%(self.datapath,self.name)
            if j.system.fs.exists(datapath) and not (refresh==True or self.loadPipelines):
                self.pipelines=pickle.loads(j.system.fs.fileGetContents(datapath))
            else:
                print "refreshpipelines"
                data = self._get("v1/pipelines/")
                for item in data:
                    name=self._name2key(item["name"])
                    self.pipelines[name]=item
                data=pickle.dumps(self.pipelines)
                j.system.fs.writeFile(datapath,data)
                self.loadPipelines=False                

    def stagesGet(self,refresh=False):
        if self.stages=={} or refresh==True or self.loadStages:
            datapath="%s/%s_stages.data"%(self.datapath,self.name)
            if j.system.fs.exists(datapath) and not (refresh==True or self.loadStages):
                self.stages=pickle.loads(j.system.fs.fileGetContents(datapath))
            else:
                print "refreshpipelines"
                data = self._get("v1/stages/")
                for item in data:
                    # name=self._name2key(item["name"])
                    self.stages[item["id"]]=item
                data=pickle.dumps(self.stages)
                j.system.fs.writeFile(datapath,data)
                self.loadStages=False 

    def _getNamesFromList(self,name,llist):
        name=self._name2key(name)
        if llist.has_key(name):
            return llist[name]
        if name.find(" ")==1:
            items=name.split(" ")
            if llist.has_key("%s %s"%(items[0],items[1])):
                return llist[name]
            if llist.has_key("%s %s"%(items[1],items[0])):
                return llist[name]
        if name.find(" ")==2:
            items=name.split(" ")
            if llist.has_key("%s %s %s"%(items[0],items[1],items[2])):
                return llist[name]
            if llist.has_key("%s %s %s"%(items[0],items[2],items[1])):
                return llist[name]
            if llist.has_key("%s %s %s"%(items[1],items[0],items[2])):
                return llist[name]
            if llist.has_key("%s %s %s"%(items[1],items[2],items[0])):
                return llist[name]
            if llist.has_key("%s %s %s"%(items[2],items[1],items[0])):
                return llist[name]
            if llist.has_key("%s %s %s"%(items[2],items[0],items[1])):
                return llist[name]

    def personGetFromName(self,orgname,name):
        self.personsGet()
        orgname=self._strNormalise(orgname)
        persons=self._getNamesFromList(name,self.persons)
                        
        if persons==None:
            return None
        for person in persons:
            orgname2=self._strNormalise(person["org_name"])
            if orgname==orgname2:
                return person        
        return None        

    def pipelineGetFromName(self,name):
        self.pipelinesGet()
        return self._getNamesFromList(name,self.pipelines)
        
    def organizationGetFromName(self,name):
        self.organizationsGet()
        return self._getNamesFromList(name,self.orgs)        

    def dealGet(self,id):
        self.dealsGet()
        if self.deals.has_key(id):
            return self.deals[id]
        raise RuntimeError("Could not find deal with id:%s in %s"%(id,self.name))

    def personGet(self,id):
        self.personsGet()
        if self.personsId.has_key(id):
            return self.personsId[id]
        raise RuntimeError("Could not find person with id:%s in %s"%(id,self.name))

    def organizationGet(self,id):
        self.organizationsGet()
        if self.orgsId.has_key(id):
            return self.orgsId[id]
        raise RuntimeError("Could not find organization with id:%s in %s"%(id,self.name))

    def personCopy2Destination(self,id):
        person=self.personGet(id)
        personName=person["name"]
        orgName=person["org_name"]
        #get emails
        emails=",".join([item["value"].encode("ascii") for item in person["email"] if item["value"] <>""])
        phones=",".join([item["value"].encode("ascii") for item in person["phone"] if item["value"] <>""])
        self.destination.personAdd(personName,orgName,emails,phones)

    def organizationCopy2Destination(self,id):
        org=self.organizationGet(id)
        orgName=org["name"]
        self.destination.organizationAdd(orgName)

    def dealCopy2Destination(self,id,pipeline=None):
        deal=self.dealGet(id)
        if deal["person_id"]<>0:
            personName=deal["person_id"]["name"]
            personOrg=self.personGet(deal["person_id"]["value"])["org_name"]
        else:
            personName=None
            personOrg=None
        orgName=deal["org_id"]["name"]
        title=deal["title"].strip()
        value=int(deal["value"])

        #check organization exists on dest
        organization2=self.destination.organizationGetFromName(orgName)
        if organization2==None:
            #need to copy org from source to dest
            self.organizationAdd(orgName)
        if personName<>None:
            person2=self.destination.personGetFromName(personOrg,personName)
            if person2==None:
                person2=self.personGetFromName(personOrg,personName)
                if person2==None:
                    raise RuntimeError("Could not find person:%s on source"%personName)
                personid=person2["id"]
                self.personCopy2Destination(personid)

        self.destination.dealAdd(title,value,personName,orgName,pipeline=pipeline)

    def dealMove2Destination(self,id,pipeline=None):
        self.dealCopy2Destination(id,pipeline=pipeline)
        self.dealDelete(id)


    def dealDelete(self,id):
        self._delete("v1/deals/%s"%id)        

    def _delete(self,urlpart):
        url=self._getBaseUrl(urlpart)
        data=requests.request(method="DELETE",url=url)

    def _post(self,urlpart,payload,put=False):
        url=self._getBaseUrl(urlpart)
        headers = {'content-type': 'application/json'}
        if put:
            print "put:%s"%url
            data=requests.request(method="PUT",url=url, data=json.dumps(payload), headers=headers)
        else:
            #post
            print "post:%s"%url
            data=requests.post(url, data=json.dumps(payload), headers=headers)
        data=data.json()
        if data.has_key("error"):
            raise RuntimeError("Error in post:%s"%data["error"])        

        if data.has_key("data"):
            data=data["data"]

        return data

    def _get(self,urlpart,payload=None,getstatement=""):
        url=self._getBaseUrl(urlpart)
        if getstatement<>"":
            url+="&%s"%(getstatement)
        headers = {'content-type': 'application/json'}
        print url
        if payload<>None:
            data=requests.get(url, data=json.dumps(payload), headers=headers)
        else:
            data=requests.get(url)
        data=data.json()
        if data.has_key("error"):
            print "error in get:"
            print "payload:%s"%payload
            print "getstatement:%s"%getstatement
            raise RuntimeError("Error in get:%s"%data["error"])
        return data["data"]

    def organizationAdd(self,name):
        """
        """
        print "organization add in %s: %s"%(self.name,name)

        orgExists=self.organizationGetFromName(name)

        if orgExists==None:
            payload={}
            payload["name"]=name
            r=self._post("v1/organizations/",payload)
            id=r["id"]
        else:
            id=orgExists["id"]

        self.loadOrgs=True
        return id

    def personAdd(self,personName,orgName,emails,phones):
        """
        @param phones is comma separated list of phones
        @param emails is comma separated list of emails
        """
        print "person add in %s: %s"%(self.name,personName)

        if personName==None:
            raise RuntimeError("personname cannot be None")

        personExists=self.personGetFromName(orgName,personName)
        if personExists==None:
            print "person new"

        org=self.organizationGetFromName(orgName)
        if org<>None:
            orgid=org["id"]
        else:
            orgid=self.organizationAdd(orgName)

        put=False
        if personExists<>None:
            emailsexist=[item["value"].lower().strip().encode("ascii") for item in personExists["email"] if item["value"] <>""]
            phonesexist=[item["value"].lower().strip().encode("ascii") for item in personExists["phone"] if item["value"] <>""]

            emails=emails.split(",")
            for email in emails:
                email=email.lower().strip().encode("ascii")
                if email not in emailsexist and email<>"":
                    emailsexist.append(email)
                    put=True
            emails=",".join(emailsexist)            
                
            phones=phones.split(",")
            for phone in phones:
                phone=phone.lower().strip().encode("ascii")
                if phone not in phonesexist and phone<>"":
                    phonesexist.append(phone)
                    put=True
            phones=",".join(phonesexist)

            orgid=int(personExists["org_id"]["value"])

        emailsOut=[]
        primary=True
        for email in emails.split(","):
            item={}
            item["value"]=email.encode("ascii").lower().strip()
            item["primary"]=primary
            primary=False
            emailsOut.append(item)

        phonesOut=[]
        primary=True
        for phone in phones.split(","):
            item={}
            item[u"value"]=u"%s"%phone.lower().strip()
            item[u"primary"]=primary
            primary=False
            phonesOut.append(item)

        payload={u'name':personName}
        if phonesOut<>[]:
            payload[u"phone"]=phonesOut
        if emailsOut<>[]:
            payload[u"email"]=emailsOut

        if orgid<>None:
            payload[u"org_id"]=orgid

        if personExists<>None and put:
            payload["owner_id"]=personExists["owner_id"]["value"]
            payload["id"]=personExists["id"]
            r=self._post("v1/persons/%s"%payload["id"],payload,put=True)
            personid=r["id"]
        elif personExists==None:
            r=self._post("v1/persons/",payload)
            personid=r["id"]
        else:
            personid=personExists["id"]

        self.loadPersons=True
        return personid

    def dealAdd(self,title,value,person,organization,personEmails="",personPhones="",pipeline=None):
        print "deal add in %s: %s"%(self.name,title)
        personKey=self._name2key(person)
        organizationKey=self._name2key(organization)        
        payload={'title':title,'value': value}

        #check organization exists
        organization2=self.organizationGetFromName(organizationKey)
        if organization2<>None:
            payload["org_id"]=organization2["id"]
        else:
            #does not exist create
            orgid=self.organizationAdd(organization)
            payload["org_id"]=orgid

        if person<>None:
            person2=self.personGetFromName(organization,personKey)
            if person2<>None:
                payload["person_id"]=person2["id"]
            else:
                #does not exist create
                persid=self.personAdd(person,organization,emails=personEmails,phones=personPhones)
                payload["person_id"]=persid

        self.loadDeals=True

        if pipeline<>None:
            stages=self.stagesGetFromPipeline(pipeline)
            stage=[item for item in stages if item["prob"]==0][0]
            stageid=stage["id"]
            payload["stage_id"]=stageid
            
        r = self._post("v1/deals/", payload=payload)
        return r["id"]
        
    def stagesGetFromPipeline(self,name):
        pipelineobj=self.pipelineGetFromName(name)
        self.stagesGet()
        result=[]
        for key in self.stages.keys():
            stage=self.stages[key]
            if stage["pipeline_id"]==pipelineobj["id"]:
                r={}
                r["name"]=self._strNormalise(stage["name"])
                r["id"]=int(stage["id"])
                r["prob"]=int(stage["deal_probability"])
                result.append(r)
        return result

    def quit(self):
        self.dealsGet()
        self.organizationsGet()
        self.personsGet()
        self.stagesGet()
        self.pipelinesGet()
        if self.destination<>None:
            self.destination.quit()


    # s=str(json.dumps(data[item2],indent=4))

    # j.system.fs.writeFile("data/%s.json"%item2,s)


reset=False

pd=PipeDrive(name="awingu",reset=reset)
pd.loadPersons=True
pd.destination=PipeDrive(name="incubaid",reset=reset)

# pd.personAdd(personName="kristof2",orgName="test3",emails="",phones="")
# pd.organizationAdd(name="test3")
# pd.dealAdd(title="testdeal",value=200,person="kristof2",organization="test")

funding=[109,108,96,95]
deals=[43,53]

for i in funding:
    pd.dealMove2Destination(i,pipeline="FundingAwingu")
    #pd.dealCopy2Destination(i,pipeline="FundingAwingu")

for i in deals:
    pd.dealMove2Destination(i,pipeline="CloudScalers")

pd.quit()

j.application.stop()
