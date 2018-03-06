#!/usr/bin/env python3
#
# Meteo.si XML parser
#
# Author: ARosman77
#

import urllib.request
from xml.dom import minidom

# Meteo.si URLs
#testURL = "http://www.meteo.si/uploads/probase/www/observ/surface/text/sl/observation_si_latest.xml"
testURL = "http://www.meteo.si/uploads/probase/www/observ/surface/text/sl/observationAms_si_latest.xml"

class meteoData:
    # place for static global variables
    def __init__(self, meteoURL, tagName, tagData):
        self.tagName = tagName
        self.tagData = tagData
        self.meteoURL = meteoURL
        self.domDocument = None
        self.metData = None
        self.tagNameData = None
        # fetch data at creation
        self.refreshData()

    def fetchData(self):
        self.domDocument = minidom.parse(urllib.request.urlopen(self.meteoURL))
        self.metData = self.domDocument.getElementsByTagName('metData')
        return self.metData

    def getTagNameData(self):
        for data in self.metData:
            if ( data.getElementsByTagName(self.tagName).item(0).firstChild.data == self.tagData ):
                self.tagNameData = data
                return self.tagNameData
        self.tagNameData = None
        return self.tagNameData

    def getDataElement(self, tagName):
        element = self.tagNameData.getElementsByTagName(tagName).item(0).firstChild
        if (element!=None): return element.data
        else: return None

    def refreshData(self):
        self.fetchData()
        self.getTagNameData()

    def getLongTitle(self):
        return self.getDataElement('domain_longTitle')

    def getTemperature(self):
        return self.getDataElement('t')

    def getHumidity(self):
        return self.getDataElement('rh')

    def getWindSpeed(self):
        return self.getDataElement('ff_val')

dataLjubljana = meteoData(testURL,'domain_shortTitle','LJUBLJANA - BEŽIGRAD')
dataTitle = dataLjubljana.getLongTitle()
dataTemp = dataLjubljana.getTemperature()
dataHum = dataLjubljana.getHumidity()
dataWindSpeed = dataLjubljana.getWindSpeed()
if (dataWindSpeed == None) : dataWindSpeed=""
print(dataTitle + " : " + dataTemp + "°C / " + dataHum + "%  " + dataWindSpeed)
