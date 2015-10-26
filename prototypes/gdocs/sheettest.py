
from JumpScale import j

#pip install PyDrive
#pip install --upgrade oauth2client
#pip install gspread

import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

path="/Users/despiegk/.google/despiegktest.json"
json_key = json.load(open(path))
scope = ['https://spreadsheets.google.com/feeds']

credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)

gc = gspread.authorize(credentials)

wks = gc.open("Gener8_modules").sheet1

from IPython import embed
print "DEBUG NOW 00088"
embed()
