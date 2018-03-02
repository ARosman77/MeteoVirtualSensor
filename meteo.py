# Meteo.si XML parser
#
# Author: ARosman77
#

import urllib.request
from xml.dom import minidom

def fetchData():
    #meteoURL = "http://www.meteo.si/uploads/probase/www/observ/surface/text/sl/observation_si_latest.xml"
    meteoURL = "http://www.meteo.si/uploads/probase/www/observ/surface/text/sl/observationAms_si_latest.xml"
    dom = minidom.parse(urllib.request.urlopen(meteoURL))
    metData = dom.getElementsByTagName('metData')
    #shortTitles = dom.getElementsByTagName('domain_shortTitle')
    #tsUpdated = dom.getElementsByTagName('tsUpdated')[1].firstChild.data
    #temperature = dom.getElementsByTagName('t_degreesC')[1].firstChild.data
    #humidity = dom.getElementsByTagName('rh')[1].firstChild.data

    for data in metData:
        print(data.getElementsByTagName('domain_shortTitle').item(0).firstChild.data)
        #print(data.firstChild.data)
    #print(tsUpdated)
    #print(temperature)
    #print(humidity)

fetchData()

