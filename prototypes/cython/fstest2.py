# from pylabs.InitBase import *

# q.application.appname = "owfs"
# q.application.start()


import os
import os.path
import sys
# sys.path=['lib2','/usr/lib/python2.7','/usr/lib/pymodules/python2.7','/usr/lib/python2.7/lib-dynload/','/opt/qbase6/lib/pylabs/','/opt/qbase6/lib/pylabsextensions/']
# sys.path=["core.egg","compr.egg","owlib"]
sys.path.append('jslib')
import regex  # easy_install regex
import traceback
import time
import hashlib
import blosc


# cStringIO

from ext.core.installtools.InstallTools import InstallTools


class TIMER:

    @staticmethod
    def start():
        TIMER.clean()
        TIMER._start = time.time()

    @staticmethod
    def stop(nritems=0, log=True):
        TIMER._stop = time.time()
        TIMER.duration = TIMER._stop - TIMER._start
        if nritems > 0:
            TIMER.nritems = float(nritems)
            if TIMER.duration > 0:
                TIMER.performance = float(nritems) / float(TIMER.duration)
        if log:
            TIMER.result()

    @staticmethod
    def clean():
        TIMER._stop = 0.0
        TIMER._start = 0.0
        TIMER.duration = 0.0
        TIMER.performance = 0.0
        TIMER.nritems = 0.0

    @staticmethod
    def result():
        print "duration:%s" % TIMER.duration
        print "nritems:%s" % TIMER.nritems
        print "performance:%s" % TIMER.performance


class ERRORHANDLER:

    @staticmethod
    def log(msg):
        print msg

    @staticmethod
    def setExceptHook():
        sys.excepthook = ERRORHANDLER.exceptHook

    @staticmethod
    def exceptHook(ttype, pythonExceptionObject, tb):
        """ 
        every fatal error in pylabs or by python itself will result in an exception
        in this function the exception is caught.
        This routine will create an errorobject & escalate to the infoserver
        @ttype : is the description of the error
        @tb : can be a python data object or a Event
        """

        print "EXCEPTIONHOOK"

        ERRORHANDLER.inException = True

        # errorobject=self.parsePythonErrorObject(pythonExceptionObject,ttype=ttype,tb=tb)

        # ERRORHANDLER.processErrorConditionObject(errorobject)

        print "**ERROR**"
        print pythonExceptionObject
        print "\n".join(traceback.format_tb(tb))

        # trace=ERRORHANDLER.getTraceback()

        ERRORHANDLER.inException = False

    @staticmethod
    def getTraceback():
        backtrace = ""
        stack = ""
        for x in traceback.format_stack():
            ignore = False
            # if x.find("IPython")<>-1 or x.find("MessageHandler")<>-1 \
            #   or x.find("EventHandler")<>-1 or x.find("ErrorconditionObject")<>-1 \
            #   or x.find("traceback.format")<>-1 or x.find("ipython console")<>-1:
            #    ignore=True
            stack = "%s" % (stack + x if not ignore else stack)
            if len(stack) > 50:
                backtrace = stack
                return
        return backtrace


class FS:

    @staticmethod
    def log(msg):
        print msg

    @staticmethod
    def fileGetContents(filename):
        """Read a file and get contents of that file
        @param filename: string (filename to open for reading )
        @rtype: string representing the file contents
        """
        with open(filename) as fp:
            data = fp.read()
        return data

    @staticmethod
    def isDir(path, followSoftlink=False):
        """Check if the specified Directory path exists
        @param path: string
        @param followSoftlink: boolean
        @rtype: boolean (True if directory exists)
        """
        if FS.isLink(path):
            if not followSoftlink:
                return False
            else:
                link = FS.readLink(path)
                return FS.isDir(link)
        else:
            return os.path.isdir(path)

    @staticmethod
    def isLink(path):
        return os.path.islink(path)

    @staticmethod
    def readLink(path):
        """Works only for unix
        Return a string representing the path to which the symbolic link points.
        """
        while path[-1] == "/" or path[-1] == "\\":
            path = path[:-1]
        return os.readlink(path)

    @staticmethod
    def isFile(path, followSoftlink=False):
        """Check if the specified file exists for the given path
        @param path: string
        @param followSoftlink: boolean
        @rtype: boolean (True if file exists for the given path)
        """
        if FS.isLink(path):
            if not followSoftlink:
                return False
            else:
                link = FS.readLink(path)
                return FS.isFile(link)
        else:
            return os.path.isfile(path)

    @staticmethod
    def list(path):
        # FS.log("list:%s"%path)
        if(FS.isDir(path)):
            s = sorted(["%s/%s" % (path, item) for item in os.listdir(path)])
            return s
        elif(FS.isLink(path)):
            link = FS.readLink(path)
            return FS.list(link)
        else:
            raise ValueError("Specified path: %s is not a Directory in FS.listDir" % path)

    installtools = InstallTools()

    @staticmethod
    def exists(path):
        return os.path.exists(path)

    @staticmethod
    def findDependencies(path, deps={}):
        excl = ["libc.so", "libpthread.so", "libutil.so"]
        out = FS.installtools.execute("ldd %s" % path)
        result = []
        for item in [item.strip() for item in out.split("\n") if item.strip() != ""]:
            if item.find("=>") != -1:
                link = item.split("=>")[1].strip()
                link = link.split("(")[0].strip()
                if FS.exists(link):
                    name = os.path.basename(link)
                    if name not in deps:
                        print link
                        deps[name] = link
                        deps = FS.findDependencies(link)
        return deps

    @staticmethod
    def copyDependencies(path, dest):
        FS.installtools.createdir(dest)
        deps = FS.findDependencies(path)
        for name in deps.keys():
            path = deps[name]
            FS.installtools.copydeletefirst(path, "%s/%s" % (dest, name))


class DispersedBlock:

    def __init__(self):
        self.subblocks = []

    def create(self, s, nrblocks, extrablocks, compress=True):
        pass


class ByteProcessor:

    @staticmethod
    def md5str(s):
        if isinstance(s, unicode):
            s = s.encode('utf-8')
        impl = hashlib.new(s)
        return impl.hexdigest()

    @staticmethod
    def compress(s):
        return blosc.compress(s, typesize=8)

    @staticmethod
    def decompress(s):
        return blosc.decompress(s)

    @staticmethod
    def disperse(s, nrblocks, extrablocks, compress=True):
        """
        returns DispersedBlock object
        """
        db = DispersedBlock()
        db.create(s, nrblocks, extrablocks, compress)
        return db

    @staticmethod
    def getDispersedBlockObject():
        return DispersedBlock

    @staticmethod
    def undisperse(dispersedBlockObject, uncompress=True):
        dispersedBlockObject.restore

    @staticmethod
    def decompress(s):
        return blosc.decompress(s, typesize=8)


class JSFile:

    def __init__(self, fullpath, name):
        self.name = name


class JSLink:

    def __init__(self, fullpath, name, dest):
        self.name = name
        self.dest = dest


class JSDirObject:

    def __init__(self, path, parent):
        name = os.path.basename(path)
        self.key = ""
        self.nsid = 0
        self.name = name
        self.parent = parent
        self.files = {}
        self.dirs = {}
        self.links = {}
        self.changed = False

    def registerFile(self, path):
        name = os.path.basename(path)
        if name not in self.files:
            FSWalker.registerChange(self, "F", "N", name)  # L:link, D:dir, F:File    N:new, M:modified, D:deleted
            self.changed = True
            self.files[name] = JSFile(path, name)
            self.files[name].stat = os.stat(path)
        else:
            pass
            self.changed = True

    def registerDir(self, path):
        name = os.path.basename(path)
        if name not in self.dirs:
            FSWalker.registerChange(self, "D", "N", name)  # L:link, D:dir, F:File    N:new, M:modified, D:deleted
            self.changed = True
            self.files["name"] = None

    def registerLink(self, path):
        name = os.path.basename(path)
        dest = FS.readLink(path)
        if name not in self.links:
            FSWalker.registerChange(self, "L", "N", name)  # L:link, D:dir, F:File    N:new, M:modified, D:deleted
            self.changed = True
            self.links[name] = JSLink(path, name, dest)
        else:
            link = self.links[name]
            if link.dest != dest:
                FSWalker.registerChange(self, "L", "M", name)
                link.dest = dest
                self.changed = True


class REGEXTOOL():

    @staticmethod
    def match(pattern, text):
        m = regex.match(pattern, text)
        if m != None:
            print "%s %s" % (pattern, text)
            return True
        else:
            return False

    @staticmethod
    def matchContent(path, contentRegexIncludes=[], contentRegexExcludes=[]):
        content = FS.fileGetContents(path)
        if REGEXTOOL.matchMultiple(patterns=contentRegexIncludes, text=content) and not REGEXTOOL.matchMultiple(patterns=contentRegexExcludes, text=content):
            return True
        return False

    @staticmethod
    def matchMultiple(patterns, text):
        """
        see if any patterns matched
        if patterns=[] then will return False
        """
        if type(patterns).__name__ != 'list':
            raise RuntimeError("patterns has to be of type list []")
        if patterns == []:
            return True
        for pattern in patterns:
            pattern = REGEXTOOL._patternFix(pattern)
            if REGEXTOOL.match(pattern, text):
                return True
        return False

    @staticmethod
    def matchPath(path, regexIncludes=[], regexExcludes=[]):
        if REGEXTOOL.matchMultiple(patterns=regexIncludes, text=path) and not REGEXTOOL.matchMultiple(patterns=regexExcludes, text=path):
            return True
        return False

    @staticmethod
    def _patternFix(pattern):
        if pattern.find("(?m)") == -1:
            pattern = "%s%s" % ("(?m)", pattern)
        return pattern


class FSWalker():

    # def _checkDepth(path,depths,root=""):
    #     if depths==[]:
    #         return True
    # path=q.system.fs.pathclean(path)
    #     path=FSWalker.pathRemoveDirPart(path,root)
    #     for depth in depths:
    #         dname=os.path.dirname(path)
    #         split=dname.split(os.sep)
    #         split = [ item for item in split if item<>""]
    # print split
    #         if depth==len(split):
    #             return True
    #     else:
    #         return False

    @staticmethod
    def log(msg):
        print msg

    @staticmethod
    def registerChange(do, ttype, status, name):
        # print "CHANGE: %s %s %s" %(name,ttype,status)
        pass

    @staticmethod
    def _findhelper(arg, path):
        arg.append(path)

    @staticmethod
    def find(root, includeFolders=False, includeLinks=False, pathRegexIncludes=[], pathRegexExcludes=[], contentRegexIncludes=[], contentRegexExcludes=[], followlinks=False):
        """
        @return {files:[],dirs:[],links:[]}
        """

        files = []
        dirs = []
        links = []

        def processfile(path):
            files.append(path)

        def processdir(path):
            dirs.append(path)

        def processlink(path):
            links.append(path)

        matchfile = None

        if pathRegexIncludes != [] or pathRegexExcludes != []:
            if contentRegexIncludes == [] and contentRegexExcludes == []:
                def matchfile(path):
                    return REGEXTOOL.matchPath(path, pathRegexIncludes, pathRegexExcludes)
            else:
                def matchfile(path):
                    return REGEXTOOL.matchPath(path, pathRegexIncludes, pathRegexExcludes) and REGEXTOOL.matchContent(path, contentRegexIncludes, contentRegexExcludes)

        matchdir = None
        matchlink = None

        if includeFolders:
            if pathRegexIncludes != [] or pathRegexExcludes != []:
                def matchdir(path):
                    return REGEXTOOL.matchPath(path, pathRegexIncludes, pathRegexExcludes)

        if includeLinks:
            if pathRegexIncludes != [] or pathRegexExcludes != []:
                def matchlink(path):
                    return REGEXTOOL.matchPath(path, pathRegexIncludes, pathRegexExcludes)

        FSWalker.walk(root, callbackFunctionFile=processfile, callbackFunctionDir=processdir, callbackFunctionLink=processlink, args={},
                      callbackForMatchFile=matchfile, callbackForMatchDir=matchdir, callbackForMatchLink=matchlink, matchargs={}, followlinks=followlinks)

        listfiles = {}
        listfiles["files"] = files
        listfiles["dirs"] = dirs
        listfiles["links"] = links

        return listfiles

    @staticmethod
    def walk(root, callbackFunctionFile=None, callbackFunctionDir=None, callbackFunctionLink=None, args={}, callbackForMatchFile=None, callbackForMatchDir=None, callbackForMatchLink=None, matchargs={}, followlinks=False):
        '''Walk through filesystem and execute a method per file and dirname

        Walk through all files and folders starting at C{root}, recursive by
        default, calling a given callback with a provided argument and file
        path for every file & dir we could find.

        To match the function use the callbackForMatch function which are separate for dir or file
        when it returns True the path will be further processed
        when None (function not given match will not be done)

        Examples
        ========
        >>> def my_print(path,arg):
        ...     print arg, path
        ...
        #if return False for callbackFunctionDir then recurse will not happen for that dir

        >>> def matchDirOrFile(path,arg):
        ...     return True #means will match all
        ...

        >>> self.walkFunctional('/foo', my_print,my_print, 'test:',matchDirOrFile,matchDirOrFile)
        test: /foo/file1
        test: /foo/file2
        test: /foo/file3
        test: /foo/bar/file4

        @param root: Filesystem root to crawl (string)
        #@todo complete
        
        '''
        # We want to work with full paths, even if a non-absolute path is provided
        root = os.path.abspath(root)

        if not FS.isDir(root):
            raise ValueError('Root path for walk should be a folder')

        # print "ROOT OF WALKER:%s"%root

        FSWalker._walkFunctional(root, callbackFunctionFile, callbackFunctionDir, callbackFunctionLink, args,
                                 callbackForMatchFile, callbackForMatchDir, callbackForMatchLink, matchargs, followlinks=followlinks)

    @staticmethod
    def getDirObject(path, parent):
        return JSDirObject(path, parent)

    @staticmethod
    def _walkFunctional(
        path, callbackFunctionFile=None, callbackFunctionDir=None, callbackFunctionLink=None, args={}, callbackForMatchFile=None, callbackForMatchDir=None, callbackForMatchLink=None, matchargs={},
            followlinks=False, dirObjectProcess=True):
        if dirObjectProcess:
            do = FSWalker.getDirObject(path, parent="parent")
        else:
            do = None

        paths = FS.list(path)
        for path2 in paths:
            # FSWalker.log("walker path:%s"% path2)
            if FS.isFile(path2, False):
                # FSWalker.log("walker filepath:%s"% path2)
                if callbackForMatchFile == None or callbackForMatchFile(path2, **matchargs):
                    if do != None:
                        do.registerFile(path2)
                    # execute
                    if callbackFunctionFile != None:
                        callbackFunctionFile(path2, **args)
                elif callbackForMatchFile == False:
                    continue
            elif FS.isDir(path2, followlinks):
                # FSWalker.log("walker dirpath:%s"% path2)
                if callbackForMatchDir == None or callbackForMatchDir(path2, **matchargs):
                    if do != None:
                        do.registerDir(path2)
                    # recurse
                    # print "walker matchdir:%s"% path2
                    if callbackFunctionDir != None:
                        callbackFunctionDir(path2, **args)
                elif callbackForMatchDir == False:
                    continue
                FSWalker._walkFunctional(path2, callbackFunctionFile, callbackFunctionDir,
                                         callbackFunctionLink, args, callbackForMatchFile, callbackForMatchDir, callbackForMatchLink)
            elif FS.isLink(path2):
                # FSWalker.log( "walker link:%s"% path2)
                if callbackForMatchLink == None or callbackForMatchLink(path2, **matchargs):
                    if do != None:
                        do.registerLink(path2)
                if callbackFunctionLink != None:
                    # execute
                    callbackFunctionLink(path2, **args)
                elif callbackFunctionLink == False:
                    continue

if __name__ == '__main__':
    # found=FSWalker.find(,recursive=True, includeFolders=True, pathRegexIncludes=[".*"],pathRegexExcludes=[], contentRegexIncludes=[], contentRegexExcludes=[])

    # deps=FS.copyDependencies("fstest2","lib")
    root = "/usr"

    files = []
    dirs = []
    links = []

    def processfile(path):
        files.append(path)

    def processdir(path):
        dirs.append(path)

    def processlink(path):
        links.append(path)

    def matchfile(path):
        return False

    def matchdir(path):
        return False

    def matchlink(path):
        return False

    ERRORHANDLER.setExceptHook()

    TIMER.start()

    # result=FSWalker.find(root, includeFolders=True,includeLinks=True, pathRegexIncludes=[".*7z.*"],pathRegexExcludes=[".*pngee.*"], contentRegexIncludes=[], contentRegexExcludes=[],followlinks=False)
    result = FSWalker.find(root, includeFolders=True, includeLinks=True, pathRegexIncludes=[], pathRegexExcludes=[
                           ".*\.pyc"], contentRegexIncludes=[], contentRegexExcludes=[], followlinks=False)

    nrfound = (len(result["files"]) + len(result["dirs"]) + len(result["links"]))
    print "found:%s" % nrfound
    nr = 158245

    TIMER.stop(nr)

    # FSWalker.walkFunctional(root,callbackFunctionFile=processfile, callbackFunctionDir=processdir,callbackFunctionLink=processlink,args={}, \
    #     callbackForMatchFile=matchfile,callbackForMatchDir=matchdir,callbackForMatchLink=matchlink,matchargs={},followlinks=False)
