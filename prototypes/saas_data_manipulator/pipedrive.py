from pylabs.InitBase import *    

import sys

q.application.appname = "pipedrive"
q.application.start()

q.jshellconfig.interactive=True

try:
    import ujson as json
except:
    import json
    
import requests

API_KEY="07a450c0ef7c498b00d2a4a482278f86dd063972"

for item,item2 in [("people","people"),("org","organizations"),("deal","deals")]:

    url="https://api.pipedrive.com/1.0/%s/index?api_token=%s"%(item,API_KEY)

    data = requests.get(url).json()


    s=str(json.dumps(data[item2],indent=4))

    q.system.fs.writeFile("data/%s.json"%item2,s)



url="https://api.pipedrive.com/1.0/activity/my_activities?api_token=%s"%(API_KEY)
data = requests.get(url).json()

s=str(json.dumps(data["activities"],indent=4))
q.system.fs.writeFile("data/%s.json"%"my_activities",s)





q.application.stop()
