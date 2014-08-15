#!/usr/bin/env python

import cmd
import locale
import os
import pprint
import shlex
import sys

from dropbox import client, rest, session

from JumpScale import j

import JumpScale.lib.sandboxer

j.application.start("jsexamples:dropbox")



# XXX Fill in your consumer key and secret below
# You can find these at http://www.dropbox.com/developers/apps
app_key = 'zeixgn5rsvu7jxp'
app_secret = '8tfjjnebamea9dh'


import dropbox

# Get your app key and secret from the Dropbox developer website

flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)


access_token_path="/opt/dropbox_token_store.txt"

if not j.system.fs.exists(path=access_token_path):
    authorize_url = flow.start()

    print '1. Go to: ' + authorize_url
    print '2. Click "Allow" (you might have to log in first)'
    print '3. Copy the authorization code.'
    code = raw_input("Enter the authorization code here: ").strip()
    access_token, user_id = flow.finish(code)
    j.system.fs.writeFile(filename=access_token_path,contents=access_token)
else:    
    access_token=j.system.fs.fileGetContents(access_token_path)
    
client = dropbox.client.DropboxClient(access_token)
print 'linked account: ', client.account_info()




months=["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]

import time
import ujson
import leveldb

ago=j.base.time.getEpochAgo("-3m")
db=leveldb.DB("/opt/dropbox.db",create_if_missing=True)

def download():
    has_more=True
    cursor=None
    while has_more:
        result=client.delta(cursor=cursor)
        entries=result["entries"]
        reset=result["reset"]
        cursor=result["cursor"]    
        has_more=result["has_more"]
        print "found:%s"%len(entries)
        for item in entries:
            path=item[0]
            print path
            db.put(path,ujson.dumps(item))
        # dat=item[1]["modified"]
        print item
        print cursor
        print reset
        print has_more

download()

def findnew():
    for item in db.keys(prefix=""):
        from IPython import embed
        print "DEBUG NOW ooo"
        embed()
        p
    

        # dat=item[1]["modified"]
        # month,year=dat.split(",")[1].split(":")[0].strip().split(" ")[1:3]
        # month=month.lower()
        # if month not in months:
        #     from IPython import embed
        #     print "DEBUG NOW months"
        #     embed()
        # month=months.index(month)
        # t = (int(year), month, 0, 0, 0, 0, 0, 0, 0)
        # epoch=time.mktime(t)
        # if epoch>ago:
        #     from IPython import embed
        #     print "DEBUG NOW found"
        #     embed()

from IPython import embed
print "DEBUG NOW ooo"
embed()


findnew()

db.close()

j.application.stop()