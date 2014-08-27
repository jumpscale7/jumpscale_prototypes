
from JumpScale import j


import JumpScale.grid.zdaemon

j.application.start("zdaemon")

j.logger.consoleloglevel = 6

zd = j.core.zdaemon.getZDaemon(port=3399, nrCmdGreenlets=50)

class MyCommands():

    def __init__(self, daemon):
        #TODO
        
        self.repopath=""

    def authenticate(self, user, login, **args):
        return True  # will authenticall all (is std)

    def reposList(self, **args):
        ##TODO
        pass
        
    def repoCreate(self,name):
        """
        create repo on git repo using hrd param docs.gitbaseurl= as basis
        only admin can do this
        repo name= docs_$name
        use agentcontroller
        """
        pass

    def reposUpdate(self,name="*"):
        """
        get all repo's from git repo user account starting with docs_
        update all info
        use agentcontroller
        only admin can do this
        @param name if name used then only relevant repo
        """
        pass

    def reposPush(self,name="*"):
        """
        use agentcontroller to push all repos known to the system
        only admin can do this
        @param name if name used then only relevant repo
        """
        pass

    def docGet(self,reponame,path, **args):
        """
        @path is path of doc inside repo
        @return returns blosc compressed file in binary format        
        """
        ##TODO
        pass

    def docSet(self,reponame,path, bindata,**args):
        """
        @param bindata is blosc format of data of file
        @param path is path of doc inside repo
        user from session is used to commit file
        commit happens by agent controller: jscript and happens async, make sure locking is done that only 1 commit at same time happens on 1 repo
        file is written to temp location first then by jscript moved to right location in repo & then committed 
        (so if 2 users do a set +- at same time they will still be committed one after the other)
        populate the local leveldb with metadata about doc (key reponame__normalizedPath) has e.g. md5
        """
        ##TODO
        pass

    def docList(self,reponame,path):
        """
        @param list docs in path 
        @return [[pathInRepo,size,moddate]]
        """
        pass

    def docGetMetadata(self,reponame,path,history=True,**args):
        """
        @return relevant data about doc e.g. author, ... if history then return all metadata about versions too
        the history is call to git app
        all the other info is cached in a local leveldb
        """
        pass

    def aclReload(self,**args):
        pass


zd.addCMDsInterface(MyCommands,"docsmgmt")  # pass as class not as object !!!
zd.start()

j.application.stop()
