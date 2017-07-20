import json
import gspread
import datetime
#from  oauth2client.client  import SignedJwtAssertionCredentials
from oauth2client.service_account import ServiceAccountCredentials

import csv

print('upload sequence start')

#json_key = json.load(open('hello.json'))
json_key = 'credentialKey.json'
scope = ['https://spreadsheets.google.com/feeds']
#credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_key, scope)

gc = gspread.authorize(credentials)
print('google authorized')

kk = gc.open('THMonitoring').sheet1
print('open spreadsheet')

imdata = [None]*5
with open('tempD.csv', 'rb') as f:
        reader = csv.reader(f)
        totalD = list(reader)
	imdata = totalD[len(totalD)-1]

datenormal = datetime.datetime.strptime(imdata[0],'%Y-%M-%d %H:%S')
imdata[0] = datenormal.strftime('%Y-%M-%d %H:%S')

kk.append_row(imdata)

print('data upload completed')
