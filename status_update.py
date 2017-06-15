# -*-coding: utf-8 -*-

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

data_store = data
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

# : duplicate hystereses and configuring regions

lowest = 0
highest = 100

inspect_temp = [lowest,data["hysteresis"]["low"]["send"]["temperature"], data["hysteresis"]["low"]["reset"]["temperature"], data["hysteresis"]["high"]["reset"]["temperature"], data["hysteresis"]["low"]["send"]["temperature"] ,highest]
inspect_hum = [lowest,data["hysteresis"]["low"]["send"]["humidity"], data["hysteresis"]["low"]["reset"]["humidity"], data["hysteresis"]["high"]["reset"]["humidity"], data["hysteresis"]["low"]["send"]["humidity"],highest]


instemp = 6 #initialize region value

for i in range(5):
    ins_low = inspect_temp[i]
    ins_high = inspect_temp[i+1]
    #
    if ins_low<nowtemp and ins_high>nowtemp:
        instemp = i

inshum = 6 #initialize region value

i = 6

for i in range(5):
    ins_low = inspect_hum[i]
    ins_high = inspect_hum[i+1]
    #
    if ins_low<nowhum and ins_high>nowhum:
        inshum = i

#===================================================#
#data comparision (nowdata, loggeddata)

##temperature

templog_status = [0,0,0,0,0,0] #High Low 시작, 종료, 지속, Low Log 시작, 종료, 지속

if data["log"]["status"]["temperature"] == "high" and (instemp in [1]):
    # 이전 상태가 HIGH LOGGING 상태이면서, 현태 상태가 LOW 인 경우
    # HIGH LOGGING 을 중단하고, LOW LOGGING 을 시작함
    templog_status = [0,1,0,1,0,0]
elif data["log"]["status"]["temperature"] == "high" and (instemp in [2,3]):
    # 이전 상태가 HIGH LOGGING 상태이면서, 현태 상태가 Normal 인 경우
    # HIGH LOGGING 을 중단함.
    templog_status = [0,1,0,0,0,0]
elif data["log"]["status"]["temperature"] == "high" and (instemp in [4,5]):
    # 이전 상태가 HIGH LOGGING 상태이면서, 현태 상태가 High Hyst 또는 High 인 경우
    # HIGH LOGGING 을 계속함.
    templog_status = [0,0,1,0,0,0]
elif data["log"]["status"]["temperature"] == "normal" and (instemp in [1]):
    # 이전 상태가 normal_unlogging 상태이면서, 현태 상태가 Low 인 경우
    # LOGGING을 시작함 (Low)
    templog_status = [0,0,0,1,0,0]
elif data["log"]["status"]["temperature"] == "normal" and (instemp in [2,3,4]):
    # 이전 상태가 normal_unlogging 상태이면서, 현태 상태가 Normal, High Hyst, Low Hyst 인 경우
    # LOGGING 을 안하고 있는 것을 지속함.
    templog_status = [0,0,0,0,0,0]
elif data["log"]["status"]["temperature"] == "normal" and (instemp in [5]):
    # 이전 상태가  normal_unlogging 상태이면서, 현태 상태가 High 인 경우
    # HIGH LOGGING 을 시작함 (High)
    templog_status = [1,0,0,0,0,0]
elif data["log"]["status"]["temperature"] == "low" and (instemp in [1,2]):
    # 이전 상태가 LOW LOGGING 상태이면서, 현태 상태가 Low, Low Hyst 인 경우
    # LOW LOGGING 을 계속함.
    templog_status = [0,0,0,0,0,1]
elif data["log"]["status"]["temperature"] == "low" and (instemp in [3,4]):
    # 이전 상태가 LOW LOGGING 상태이면서, 현태 상태가 Normal, High Hyst 인 경우
    # LOW LOGGING 을 중단함.
    templog_status = [0,0,0,0,0,0]
elif data["log"]["status"]["temperature"] == "low" and (instemp in [5]):
    # 이전 상태가 LOW LOGGING 상태이면서, 현태 상태가 High 인 경우
    # LOW LOGGING 을 중단하고, HIGH LOGGING 을 시작함.
    templog_status = [1,0,0,0,1,0]

##humidity

humlog_status = [0,0,0,0,0,0] #High log 시작, 종료, 지속, Low log 시작, 종료, 지속

if data["log"]["status"]["humidity"] == "high" and (inshum in [1]):
    # 이전 상태가 HIGH LOGGING 상태이면서, 현태 상태가 LOW 인 경우
    # HIGH LOGGING 을 중단하고, LOW LOGGING 을 시작함
    humlog_status = [0,1,0,1,0,0]
elif data["log"]["status"]["humidity"] == "high" and (inshum in [2,3]):
    # 이전 상태가 HIGH LOGGING 상태이면서, 현태 상태가 Normal 인 경우
    # HIGH LOGGING 을 중단함.
    humlog_status = [0,1,0,0,0,0]
elif data["log"]["status"]["humidity"] == "high" and (inshum in [4,5]):
    # 이전 상태가 HIGH LOGGING 상태이면서, 현태 상태가 High Hyst 또는 High 인 경우
    # HIGH LOGGING 을 계속함.
    humlog_status = [0,0,1,0,0,0]
elif data["log"]["status"]["humidity"] == "normal" and (inshum in [1]):
    # 이전 상태가 normal_unlogging 상태이면서, 현태 상태가 Low 인 경우
    # LOGGING을 시작함 (Low)
    humlog_status = [0,0,0,1,0,0]
elif data["log"]["status"]["humidity"] == "normal" and (inshum in [2,3,4]):
    # 이전 상태가 normal_unlogging 상태이면서, 현태 상태가 Normal, High Hyst, Low Hyst 인 경우
    # LOGGING 을 안하고 있는 것을 지속함.
    humlog_status = [0,0,0,0,0,0]
elif data["log"]["status"]["humidity"] == "normal" and (inshum in [5]):
    # 이전 상태가  normal_unlogging 상태이면서, 현태 상태가 High 인 경우
    # HIGH LOGGING 을 시작함 (High)
    humlog_status = [1,0,0,0,0,0]
elif data["log"]["status"]["humidity"] == "low" and (inshum in [1,2]):
    # 이전 상태가 LOW LOGGING 상태이면서, 현태 상태가 Low, Low Hyst 인 경우
    # LOW LOGGING 을 계속함.
    humlog_status = [0,0,0,0,0,1]
elif data["log"]["status"]["humidity"] == "low" and (inshum in [3,4]):
    # 이전 상태가 LOW LOGGING 상태이면서, 현태 상태가 Normal, High Hyst 인 경우
    # LOW LOGGING 을 중단함.
    humlog_status = [0,0,0,0,0,0]
elif data["log"]["status"]["humidity"] == "low" and (inshum in [5]):
    # 이전 상태가 LOW LOGGING 상태이면서, 현태 상태가 High 인 경우
    # LOW LOGGING 을 중단하고, HIGH LOGGING 을 시작함.
    humlog_status = [1,0,0,0,1,0]

#===================================================#
#logging dictionary data

#when stop logging
if templog_status[1] == 1 or templog_status[4] == 1:
    data["log"]["status"]["temperature"] = "normal"

if humlog_status[1] == 1 or humlog_status[4] == 1:
    data["log"]["status"]["humidity"] = "normal"

#when start high logging
if templog_status[0] == 1:
    data["log"]["start"]["temperature"] = nowtime
    data["log"]["status"]["temperature"] = "high"
    data["log"]["count"]["temperature"] = 0

if humlog_status[0] == 1:
    data["log"]["start"]["humidity"] = nowtime
    data["log"]["status"]["humidity"] = "high"
    data["log"]["count"]["humidity"] = 0

#when start low logging
if templog_status[3] == 1:
    data["log"]["start"]["temperature"] = nowtime
    data["log"]["status"]["temperature"] = "low"
    data["log"]["count"]["temperature"] = 0

if humlog_status[3] == 1:
    data["log"]["start"]["humidity"] = nowtime
    data["log"]["status"]["humidity"] = "low"
    data["log"]["count"]["humidity"] = 0


# when continue log

if templog_status[2] == 1 or templog_status[5] == 1:
    data["log"]["count"]["temperature"] = data["log"]["count"]["temperature"] + 1

if humlog_status[2] == 1 or humlog_status[5] == 1:
    data["log"]["count"]["humidity"] = data["log"]["count"]["humidity"] + 1

data["current"]["time"] = nowtime
data["current"]["humidity"] = nowhum
data["current"]["temperature"] = nowtemp

with open('monitoring_status.json','w') as statusfile:
    json.dump(data,statusfile)



    #



