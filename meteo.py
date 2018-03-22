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
        try:
            self.domDocument = minidom.parse(urllib.request.urlopen(self.meteoURL))
            self.metData = self.domDocument.getElementsByTagName('metData')
        except urllib.error.HTTPError:
            self.metData = None;
        return self.metData

    def getTagNameData(self):
        if (self.metData != None):
            for data in self.metData:
                if ( data.getElementsByTagName(self.tagName).item(0).firstChild.data == self.tagData ):
                    self.tagNameData = data
                    return self.tagNameData
        self.tagNameData = None
        return self.tagNameData

    def getDataElement(self, tagName):
        if (self.tagNameData != None):
            element = self.tagNameData.getElementsByTagName(tagName).item(0).firstChild
            if (element!=None): return element.data
        return None

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

    def getWindDirection(self):
        return self.getDataElement('dd_val')

    def getDewTemp(self):
        return self.getDataElement('td')

    def getAtmPressure(self):
        return self.getDataElement('msl')

    def getRainfallMm(self):
        return self.getDataElement('rr_val')

    def getSnowCm(self):
        return self.getDataElement('snow')

    def getWaterTemp(self):
        return self.getDataElement('tw')

    def getVisibility(self):
        return self.getDataElement('vis_val')

    def getGlobalSunRad(self):
        # Global sun radiation in W/m2
        return self.getDataElement('gSunRad')

    def getDiffuseSunRad(self):
        # Diffuse sun radiation in W/m2
        return self.getDataElement('diffSunRad')


dataLjubljana = meteoData(testURL,'domain_shortTitle','LJUBLJANA - BEŽIGRAD')
dataTitle = dataLjubljana.getLongTitle()
dataTemp = dataLjubljana.getTemperature()
dataHum = dataLjubljana.getHumidity()
dataWindSpeed = dataLjubljana.getWindSpeed()
if (dataWindSpeed == None) : dataWindSpeed=""
if (dataTitle == None) : dataTitle = "Unknown"
if (dataTemp == None) : dataTemp = "N/A";
if (dataHum == None) : dataHum = "N/A";
print(dataTitle + " : " + dataTemp + "°C / " + dataHum + "%  " + dataWindSpeed)
print(dataLjubljana.getWindDirection())
print(dataLjubljana.getDewTemp())
print(dataLjubljana.getAtmPressure())
print(dataLjubljana.getRainfallMm())
print(dataLjubljana.getSnowCm())
print(dataLjubljana.getWaterTemp())
print(dataLjubljana.getVisibility())
print(dataLjubljana.getGlobalSunRad())
print(dataLjubljana.getDiffuseSunRad())