import csv
import json

#===================================================#

#data input of present data
with open('tempD.csv', 'rb') as csvfile:
    spamreader  = csv.reader(csvfile,delimiter=',')
    totalD = list(spamreader)

nowdata = totalD[len(totalD)-1]

#===================================================#

#data input of logged data
with open('monitoring_status.json') as statusfile:
    data = json.load(statusfile)

recorddata = [data["current"]["time"], data["current"]["temperature"], data["current"]["humidity"]]

#===================================================#

#variable definition of nowdata (for inspection values into region)
def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)


nowtime = nowdata[1]
nowtemp = num(nowdata[2])
nowhum = num(nowdata[3])

