import json
import gspread
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

with open('cfg.json','r') as infile:
    fname = json.load(infile)

kk = gc.open(fname['Filename']).worksheet(fname['Sheetname'])
print('open spreadsheet')

imdata = [None]*5
with open('tempD.csv', 'rb') as f:
        reader = csv.reader(f)
        totalD = list(reader)
	imdata = totalD[len(totalD)-1]

kk.append_row(imdata)

print('data upload completed')
#values_list = kk.col_values(1)

#print(values_list)
