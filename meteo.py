#!/usr/bin/env python3
#
# Meteo.si XML parser
#
# Author: ARosman77
#

import urllib.request
from xml.dom import minidom

# Meteo.si URLs
#meteoURL = "http://www.meteo.si/uploads/probase/www/observ/surface/text/sl/observation_si_latest.xml"
meteoURL = "http://www.meteo.si/uploads/probase/www/observ/surface/text/sl/observationAms_si_latest.xml"

def fetchData(url):
    dom = minidom.parse(urllib.request.urlopen(url))
    return dom.getElementsByTagName('metData')

def getRegionData(metData, tagName, tagData):
    for data in metData:
        if ( data.getElementsByTagName(tagName).item(0).firstChild.data == tagData ):
            return data
    return None

def getRegionDataElement(regionData, tagName):
    element = regionData.getElementsByTagName(tagName).item(0).firstChild
    if (element!=None): return element.data
    else: return None

regionData = getRegionData(fetchData(meteoURL),
                           'domain_shortTitle',
                           'LJUBLJANA - BEŽIGRAD')
if (regionData != None):
    dataTitle = getRegionDataElement(regionData,'domain_longTitle')
    dataTemp = getRegionDataElement(regionData,'t')
    dataHum = getRegionDataElement(regionData,'rh')
    dataWindSpeed = getRegionDataElement(regionData,'ff_val') 
    if (dataWindSpeed == None) : dataWindSpeed=""
    print(dataTitle + " : " + dataTemp + "°C / " + dataHum + "%  " + dataWindSpeed)
else:
    print("Region data doesn't exist!")


