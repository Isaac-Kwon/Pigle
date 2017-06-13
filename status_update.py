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


nowtime = nowdata[0]
nowtemp = num(nowdata[1])
nowhum = num(nowdata[2])

#===================================================#

#data inspection (nowdata)
inspect_temp = [0,num(data["hysteresis"]["low"]["send"]["temperature"]), num(data["hysteresis"]["low"]["reset"]["temperature"]), num(data["hysteresis"]["high"]["reset"]["temperature"]), num(data["hysteresis"]["low"]["send"]["temperature"]) ,100]
inspect_hum = [0,num(data["hysteresis"]["low"]["send"]["humidity"]), num(data["hysteresis"]["low"]["reset"]["humidity"]), num(data["hysteresis"]["high"]["reset"]["humidity"]), num(data["hysteresis"]["low"]["send"]["humidity"]) ,100]

for i in range(5):
    ins_low = inspect_temp[i]
    ins_high = inspect_temp[i+1]
    #
    if ins_low<nowtemp and ins_high>nowtemp:
        instemp = i

for i in range(5):
    ins_low = inspect_hum[i]
    ins_high = inspect_hum[i+1]
    #
    if ins_low<nowhum and ins_high>nowhum:
        inshum = i

