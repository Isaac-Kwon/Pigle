#--*--coding: utf-8--*--

################################################################################
# HIPEx monitoring software :: Limiter.py
# monitoring value (number value :: integer, float, double etc.) 
# 
# value will monitoring with threshold and hysteresis (hysteresis thresholding)
#   
#  with class 'Limiter' 's function, value can input continously and judge the 
# overing of threshold (can monitoring value whether be over the threshold)
#
#  At the mode of HIGH LIMIT MODE (highlimit = true) and with hysteresis,
# input function will return alert JUST ONE TIME when been over threshold (thHi).
# This alert checker will reset when data recovered to 2nd threshold (thLo)
# 
# data flow example
# when using HIGH LIMIT MODE (highlimit = True)
# thHi = 50, thLo = 30
# 
# data | 10 20 30 40 50 60 50 40 60 50 30 20 30 
# alert| --------------a--------------b---------
# a: over alert
# b: recover alert
#
#
# == 
# with class 'DoubleLimiter' can set upper threshold and lower threshold.
# Double Limiter is combine of 2 Limiter Class Variables.
#
################################################################################

import sys, os
import subprocess
from multiprocessing import process

from triplet import Triplet

#alert with hysteresis
#return true when alert.
#through Limiter.inputData(data) can input data, will return alarm. (T of F) 
# highlimit : true >> alert when data is higher than threshold 
# highlimit : false >> alert when data is lower than threshold

class Limiter:
    def __init__(self, thHi=50, thLo=40, highlimit=True, overalert=True, returnalert=True, verbose=False):
        if verbose:
            print("Monitoring::Limiter::monitoring Initialize.")
        self.thHi = thHi
        self.thLo = thLo
        self.highlimit = highlimit
        self.alert = False
        self.verbose=verbose
        self.chkThUD()
    def setTh(self,thTh=50, thLo=40):
        self.thHi = thHi
        self.thLo = thLo
        self.chkThUD()
    def chkThUD(self):
        if (self.thHi < self.thLo):
            if self.verbose:
                print("Monitoring::Limiter::upper threshold is lower than lower threshold. Swap threshold value.")
            k = self.thHi
            self.thHi = self.thLo
            self.thLo = k
    ##############################
    # inputting data
    ##############################
    def areacheck(self, data):
    # for all. 
    #  0 |  | 50 |  | 100
    # -- thLo -- thHi --- 
        if data>self.thHi: #over high threshold
            return Triplet.Up
        elif data<self.thLo: #in hysteresis area
            return Triplet.Down
        else: #under low threshold
            return Triplet.Mid
    def udcheck(self, data):
        chkcfg = self.areacheck(data)
        try:
            if not self.highlimit:
                chkcfg = chkcfg.opposite()
        except TypeError:
            if self.verbose:
                print("Monitoring::Limiter::Undefined Value")
                raise TypeError
        return chkcfg
    def alertcheck(self, data):
        state = self.udcheck(data)
        if self.alert: #previous value of alert is true :: alert >> next
            if state in [Triplet.Up, Triplet.Mid]: #continue the alert state
                if self.verbose:
                    print("Monitoring::Limiter::Mid::Continue state of alert")
                return Triplet.Mid
            elif state == Triplet.Down: #off the alert state
                if self.verbose:
                    print("Monitoring::Limiter::Down::Off the Alert state")
                self.alert=False
                return Triplet.Down
            else:
                print("Monitoring::Limiter::UNKNOWN ERROR ACCOURED")
                raise TypeError
        else:
            if state == Triplet.Up: #Get the Alert State
                if self.verbose:
                    print("Monitoring::Limiter::Up::Raise Alert")
                self.alert=True
                return Triplet.Up
            elif state in [Triplet.Mid, Triplet.Down]: #Off the Alert State
                if self.verbose:
                    print("Monitoring::Limiter::Mid::Continue ordinary state")
                return Triplet.Mid
            else:
                print("Monitoring::Limiter::UNKNOWN ERROR ACCOURED")
                raise TypeError
    def datainput(self, data):
        self.alert = self.alertcheck(data)

if __name__ == "__main__":
    print("Data value flowing check on threshold with hysteresis")
    print("you can input value continously, with threshold")
    checker = Limiter(verbose=True)
    a = Triplet.Mid
    while True:
        try:
            print("R-ALERT STATE: ", end='')
            print(a)
            a = checker.alertcheck(float(input('input loop: ')))
        except ValueError:
            print("\n unknown value")
        except KeyboardInterrupt:
            print("\nKEYBOARD INTERRUPTED\n")
            exit()

