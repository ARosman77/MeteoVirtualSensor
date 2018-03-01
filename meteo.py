# Meteo.si XML parser
#
# Author: ARosman77
#

import urllib.request
from xml.dom import minidom

def fetchData():
    meteoURL = "http://www.meteo.si/uploads/probase/www/observ/surface/text/sl/observationAms_si_latest.xml"
    dom = minidom.parse(urllib.request.urlopen(meteoURL))
    shortTitles = dom.getElementsByTagName('domain_shortTitle')
    tsUpdated = dom.getElementsByTagName('tsUpdated')[1].firstChild.data
    temperature = dom.getElementsByTagName('t_degreesC')[1].firstChild.data
    humidity = dom.getElementsByTagName('rh')[1].firstChild.data

    for title in shortTitles:
        print(title.firstChild.data)
    print(tsUpdated)
    print(temperature)
    print(humidity)

fetchData()

