
from JumpScale import j

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

items=[(item["id"],item["title"]) for item in drive.ListFile({'q': "'%s' in parents and trashed=false" % parent}).GetList()]


ppt=drive.CreateFile({'id': items[0][0]})
