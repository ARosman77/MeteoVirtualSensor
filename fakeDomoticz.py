#   Meteo.si Virutal Sensor
#
#   Author: ARosman77
#
#   fakeDomoticz Module written by: Frank Fesevur, 2017
#   https://github.com/ffes/domoticz-buienradar
#
#   Very simple module to make local testing easier
#   It "emulates" Domoticz.Log() and Domoticz.Debug()
#

def Log(s):
    print(s)

def Debug(s):
    print(s)

def Error(s):
    print(s)