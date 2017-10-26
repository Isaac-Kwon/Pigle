import sys, os, subprocess
from multiprocessing import Process, Pipe, current_process
import time
import json
from datetime import datetime
import csv

import gspread
from oauth2client.service_account import ServiceAccountCredentials

import timeout_decorator

import limiter
from triplet import Triplet
from sendmail import Mail

json_key = 'credentialKey.json'
scope = ['https://spreadsheets.google.com/feeds']

transfercsv = 'tempD.csv'
savingcsv = 'tempsaving.csv'


def monitoringSeq():
    subprocess.call(["sudo", "./measuring"])

def GetSpreadsheet(verbose=False):
    if verbose:
        print('UploadProcess::GoogleCredential::Start')
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_key, scope)
    #get Credential
    gc = gspread.authorize(credentials)
    #get google autorize
    if verbose:
        print('UploadProcess::GoogleCredential::Google Authorized')
    #open configuration file
    with open('cfg.json','r') as infile:
        fname = json.load(infile)
    #spreadsheetfile open
    kk = gc.open(fname['Filename']).worksheet(fname['Sheetname'])
    if verbose:
        print('UploadProcess::GoogleCredential::Open Spreadsheet')
    return kk

def UploadSeq1(verbose=False): #general uploading (only one data-line)
    kk = GetSpreadsheet()
    #get data from temporary file
    imdata = [None]*5
    with open(transfercsv, 'rb') as f:
        reader = csv.reader(f)
        totalD = list(reader)
        imdata = totalD[len(totalD)-1]
    datenormal = datetime.strptime(imdata[0],'%Y-%M-%d %H:%S')
    imdata[0] = datenormal.strftime('%Y-%M-%d %H:%S')
    kk.append_row(imdata)
    print('data upload completed')

def highdeleter(filename):
    i = 0
    tempfilename = filename
    while os.path.exists(tempfilename):
        tempfilename = filename + '_' + str(i)
        i = i+1
    with open(filename,'r') as originfile:
        a = originfile.readlines()
    del(a[0])
    with open(tempfilename,'w') as tempfile:
        for line in a:
            tempfile.write(line)
    os.rename(tempfilename,filename)

def unifier(originname, offsetname, deleting=False,verbose=False):
    if verbose==True:
        print('UploadProcess::DataUnifier::Tranfer Data Detected')
    offsetlines =  open(offsetname,'rb').readlines()
    with open(originname,'ab') as originalfile:
        if verbose==True:
            print('Data lines: %d' %(len(offsetlines)))
        for line in offsetlines:
            #print(line)
            originalfile.write(line)
    print('UploadProcess::DataUnifier::Data Transferred to save data')
    if deleting:
        os.remove(offsetname)
        if verbose==True:
            print('UploadProcess::DataUnifier::Tranfer file deleted')

def UploadSeq2(outpipe=None , verbose=False): #delayed uploading (one by one dataline)
    sheet = GetSpreadsheet(datapipe=None, verbose=verbose)
    #get data from temporary file
    imdata = [None]*5
    with open(savingcsv, 'rt', encoding='utf-8') as f:
        reader = csv.reader(f)
        totalD = list(reader)
        if not outpipe is None:
            outpipe.send(totalD)
    if verbose:
        print('UploadProcess::UploadSequence::Found %d lines saved, ' %(len(totalD)),end='')
    if not len(totalD)==0:
        imdata = totalD[0]
        if verbose:
            print('Sending to google...')
        datenormal = datetime.strptime(imdata[0],'%Y-%M-%d %H:%S')
        imdata[0] = datenormal.strftime('%Y-%M-%d %H:%S')
        sheet.append_row(imdata)
        if verbose:
            print('UploadProcess::UploadSequence::Completed Uploading 1 dataline')
        return True
    else:
        print('Skip upload sequence')
        if verbose:
            print('UploadProcess::UploadSequence::Sleep 20sec.')
        time.sleep(20)
        return False

def CheckLastRow(rowcnt=0):
    sheet = GetSpreadsheet()
    lastrownum = sheet.row_count
    anslist = sheet.row_values(lastrownum-rowcnt)
    ans = not ('' in anslist) or (None in anslist)
    return ans

def SetLastRow(verbose=False):
    if verbose:
        print('UploadProcess::LastRowSetting::Start')
    sheet = GetSpreadsheet()
    while not CheckLastRow():
        sheet.delete_row(sheet.row_count)
        if verbose:
            print('UploadProcess::LastRowSetting::One Blank line deleted')

def monitoringProcess(verbose=False): #monitoring sequence for multiprocessing
    if verbose:
        print('MonitoringProcess::Start::PID %d' %(os.getpid()))
    while True:
        if verbose:
            print('MonitoringProcess::Start Loop')
            print(datetime.now().strftime('TIME: %Y/%m/%d-%H:%M:%S'))
        monitoringSeq()
        time.sleep(60)

@timeout_decorator.timeout(40)
def uploadingProcess(inpipe=None, verbose=False): #process of ((Uploading + Data Transfer)) for multiprocessing
    if verbose:
        print('UploadProcess::Start Uploading Sequence')
    try:
        if os.path.exists(transfercsv):
            unifier(savingcsv,transfercsv,deleting=True,verbose=verbose)
        upstate = UploadSeq2(outpipe=inpipe, verbose=verbose)
        if upstate:
            highdeleter(savingcsv)
            if verbose:
                print('UploadProcess::Delete head of saved data')
    except gspread.exceptions.RequestError:
        if verbose:
            print('UploadProcess::Upload Failed, Re-Try')
        SetLastRow()
    except:
        raise
                    
def alarmProcess(outpipe, verbose=False):
    while True:
        checker = Limiter(thHi=25, thLo=23)
        msg = outpipe.recv()
        to = None
        status = checker.alertcheck(float(msg[1]))
        if a==Triplet.Up:
            par = "temperature is too high. \n condition of atmosphere is %s *C, %s \% \n measure at %s  \n\n best regards\nCIMS" %(msg[1], msg[2], msg[0])
        elif a==Triplet.Down:
            par = "temperature is recovered. \n condition of atmosphere is %s *C, %s \% \n measure at %s  \n\n best regards\nCIMS" %(msg[1], msg[2], msg[0])
        elif a==Triplet.Mid:
            pass
        else:
            raise TypeError
        if a==Triplet.Up or a==Triplet.Down:
            mail = Mail(To=to, Sub="Mailling Alert for CIMS", From="sendmailtest@cims.kr", Par=par, verbose=True)
            mail.writeMail()
            mail.sendMail()


def ClockProcess(verbose=False):
    time.sleep(10)
    if verbose:
        print('ClockProcess::Start::PID %d' %(os.getpid()))
    while True:
        if verbose:
            print(datetime.now().strftime('TIME: %Y/%m/%d-%H:%M:%S'))
            time.sleep(20)

def main(verbose=False):
    try:
        mproc = Process(target=monitoringProcess, args=(True,))
        mproc.start()
        tproc = Process(target=ClockProcess, args=(True,))
        tproc.start()
        input_p, output_p = Pipe()
        rproc = Process(target=alarmProcess, args=(output_p, True))
        SetLastRow(verbose=True)
        #mailling process pipe setting
        mailOutPipe, mailInPipe = Pipe()
        while True:
            try:
                uploadingProcess(input_p, True)
            except imeout_decorator.timeout_decorator.TimeoutError:
                if verbose:
                    print('UploadProcess::Uploading Timeout. Kill and Reload.')
                pass
    except KeyboardInterrupt:
        mproc.terminate()
        tproc.terminate()
        if verbose:
            print('MonitoringProcess::Terminated')
        uproc.join()
        tproc.join()
        mailOutPipe.close()
        mailInPipe.close()
        rproc.join()
        if verbose:
            print('UploadProcess::Exit')
    except:
        pass

if __name__=="__main__":
    main()
