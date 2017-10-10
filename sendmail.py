import sys, os
import subprocess
import random

class Mail:
    templateHead = ["To: ", "Subject: ", "From: "]
    def __init__(self, To=None, Sub=None, From=None, Par=None, Cc=None, Bcc=None, verbose=False):
        self.To = To
        self.Sub = Sub
        self.From = From
        self.Par = Par
        self.Cc = Cc
        self.Bcc = Bcc
        self.verbose=verbose
    def sendMail(self, textfilename='MailTemp.temp'):
        mailtext = open(textfilename,"r")
        subprocess.Popen("sendmail","-vt", stdin=mailtext)
    def writeMail(self, textfilename='MailTemp.temp'):
        if None in [self.To, self.From]:
            if self.verbose:
                print("Sendmail::No TO or FROM e-mail address. abort")
            return
        with open(textfilename,'w') as mailFile:
            mailFile.writelines(self.templateHead[0] + self.To + "\n")
            if not self.Sub is None:
                mailFile.writelines(self.templateHead[1] + self.Sub + "\n")
            mailFile.writelines(self.templateHead[2] + self.From + "\n")
            if not self.Cc is None:
                mailFile.writelines(self.templateHead[3] + self.Cc + "\n")
            if not self.Bcc is None:
                mailFile.writelines(self.templateHead[4] + self.Bcc + "\n")
            if not self.Par is None:
                mailFile.writelines("\n"+self.Par+"\n")
            pass
        

#test script for mailling
if __name__ == "__main__":
    print("")
    print("====================================================================")
    print("Mailing Software with using \'sendmail\' command of Linux")
    print("This will run to test your device whether yours works or don\'t. ")
    print("please input your e-mail address.\n")
    testmailto = input("your email address: ")
    print("please input email to show at the top of test email address.")
    print("If keeping input to blank, it will send with \"sendmailtest@raspberry.pi\"")
    testmailfrom = input("from email adress: ")
    if testmailfrom=='':
        testmailfrom = "sendmailtest@raspberry.pi"
    configInt = random.randint(0,100000)
    testmail = Mail(To=testmailto, Sub="Sendmail Software Test", From=testmailfrom)
    testmail.Par = "Mail for test Sendmail software with Python script. \n if you didn\'t do test, just ignore. \n the configuration number is " + str(configInt) + " \n\n Best Regards. \n Sendmail Test Software." 
    testmail.writeMail()
    print("E-mail is written, will be sent.\nIf it went by too long (over 2 min.), Do KeyboardInterrupt (Ctrl+C) and check your sendmail software")
    print("Sending Sequence Start.")
    testmail.sendMail()
    print("E-mail to test Sendmail software is sent")
    print("Subject: Sendmail Software Test")
    print("Sent to " + testmailto)
    print("Sent from " + testmailfrom)
    print("Please confirm number :: " + str(configInt))

