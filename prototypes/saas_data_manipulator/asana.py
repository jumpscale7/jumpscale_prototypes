from pylabs.InitBase import *    
import sys

q.application.appname = "asana"
q.application.start()

q.jshellconfig.interactive=True

from asana import asana

asana_api = asana.AsanaAPI('16292ivi.YZCO5tfu0S16OimpyunknzJ', debug=True)

myspaces = asana_api.list_workspaces()

incubaidid=3864381820193L
awinguid=5244288044012L
incubaid_despiegk=3864381820188L

users_incubaid=asana_api.list_users(incubaidid)
users_awingu=asana_api.list_users(awinguid)

out="tasks"
outtxt=""
for task in asana_api.list_tasks(incubaidid,incubaid_despiegk):
    task_id=task["id"]
    task=asana_api.get_task(task_id)
    print task

    if task["completed"]==False:
        status=task["assignee_status"].encode("ascii")
        notes=task["notes"]
        # notes=task["notes"].replace("\n","|")
        # if len(notes)>200:
        #   notes=notes[0:200]
        try:
            notes=notes.encode("ascii")
        except:
            notes=""
        if len(notes)>50:
            outtxt+="%s : %s\n"%(status,task["name"])
            q.system.fs.writeFile("tasks/%s_%s.txt"%(status,task["name"]),notes)
        else:
            outtxt+="%s : %s : %s\n"%(status,task["name"],notes)


q.system.fs.writeFile("tasks.txt",outtxt)



from IPython.Shell import IPShellEmbed
IPShellEmbed(argv=[], banner="Welcome to IPython", exit_msg="Bye")()



q.application.stop()
