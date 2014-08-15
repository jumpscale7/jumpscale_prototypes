import time

from pprint import pprint
import cProfile
import pstats

from JumpScale import j

j.application.start("mailfetcheractions")


def process(mailfrom, emailepoch, subject, text, args):

    loghandler = args["loghandler"]
    channel, source = subject.split("_", 1)
    if channel.find("CLOUDACTION:") != -1:
        channel = channel.replace("CLOUDACTION:", "")
        for line in text.split("\n"):
            line = line.strip()
            if line != "":
                splitted = line.split(":")

                if len(splitted) == 6:
                    jobguid, start, stop, action, rootobjectguid, state = splitted
                    if action.find(".") == 0:
                        msg = "could not parse log message, action needs to have actor inside , %s %s\n%s" % (action, subject, text)
                        loghandler.raiseError(msg)
                    else:
                        actor, action = action.split(".", 1)
                        loghandler.log(jobguid, emailepoch, channel, source, actor, rootobjectguid, action, state, start, stop)
                elif len(splitted) == 10:
                    #jobid,epochstart,epochend,actionname,rootobjectid,state, customername, spacename, resourcename, resourceguid
                    jobguid, start, stop, action, rootobjectguid, state, customername, spacename, resourcename, resourceguid = splitted
                    if str(customername).strip() == "None":
                        customername = ""
                    if str(spacename).strip() == "None":
                        spacename = ""
                    if str(resourcename).strip() == "None":
                        resourcename = ""
                    if str(resourceguid).strip() == "None":
                        resourceguid = ""
                    if action.find(".") == 0:
                        msg = "could not parse log message, action needs to have actor inside , %s %s\n%s" % (action, subject, text)
                        loghandler.raiseError(msg)
                    else:
                        actor, action = action.split(".", 1)
                        loghandler.log(jobguid, emailepoch, channel, source, actor, rootobjectguid,
                                       action, state, start, stop, customername, spacename, resourcename, resourceguid)
                else:
                    msg = "could not parse log message, %s\n%s" % (subject, text)

                    loghandler.raiseError(msg)

lhandler = j.apps.acloudops.actionlogger.extensions.loghandler

# j.core.osis.destroy("acloudops") #remove all existing objects & indexes

# lhandler.loadTypes()

# lhandler.readLogs(hoursago=5*24)

# j.application.stop()

while True:
    print "fetch actions"
    robot = j.tools.mailrobot.get("imap.gmail.com", 'action@awingu.com', 'be343483')
    robot.start(process, loghandler=lhandler)

    # check all known actions (active in mem)
    # for key in actionlh.activeActions.keys():
        # action=actionlh.activeActions[key]
        # actionlh.processActionObject(action)

    time.sleep(15)


    # every hour want to save the updated stats
    # j.apps.acloudops.actionhandler.models.actiontype.set(ttype)
    # j.apps.acloudops.actionhandler.models.actiontype.list()

j.application.stop()
