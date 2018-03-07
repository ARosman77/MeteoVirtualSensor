# Meteo.si Virutal Sensor
#
# Author: ARosman77
#
"""
<plugin key="Meteo.si" name="Meteo.si Virtual Sensor" author="ARosman77"
version="1.0.0" externallink="https://github.com/ARosman77/MeteoVirtualSensor">
    <params>
        <param field="Mode1" label="Meteo.si URL" width="200px" required="true" default="http://www.meteo.si/uploads/probase/www/observ/surface/text/sl/observationAms_si_latest.xml"/>
        <param field="Mode2" label="Station name" width="200px" required="true"/>
            <options>
                <option label="Ljubljana" value="LJUBLJANA - BEŽIGRAD" default="true" />
                <option label="Velenje" value="VELENJE" />
                <option label="Novo Mesto" value="NOVO MESTO" />
            </options>
        <param field="Mode3" label="Update every x minutes" width="200px" required="true" default="10"/>
        <param field="Mode4" label="Temperature and humidity" width="200px" required="true">
            <options>
                <option label="Combined in one device" value="True" default="true" />
                <option label="Two separate devices" value="False" />
            </options>
        </param>
    </params>
</plugin>
"""

import Domoticz
import urllib.request
from xml.dom import minidom

#############################################################################
#                      Domoticz call back functions                         #
#############################################################################

class BasePlugin:

    def __init__ (self):
        self.TEMPERATURE = 1
        self.HUMIDITY = 2
        self.meteoURL = "http://www.meteo.si/uploads/probase/www/observ/surface/text/sl/observation_LJUBL-ANA_BEZIGRAD_latest.xml"
        return

    def onStart(s elf):
        Domoticz.Log("onStart called")
        if (len(Devices) == 0) :
            Domoticz.Log("Creating devices...")
            Domoticz.Device(Name="MeteoTemp",Unit=self.TEMPERATURE,TypeName="Temperature").Create()
            Domoticz.Device(Name="MeteoHumidity",Unit=self.HUMIDITY,TypeName="Humidity").Create()

    def onHeartbeat(self):
        Domoticz.Log("onHeartbeat called")
        dom = minidom.parse(urllib.request.urlopen(self.meteoURL))
        shortTitle = dom.getElementsByTagName('domain_shortTitle')[0].firstChild.data
        Domoticz.Log(shortTitle)
        tsUpdated = dom.getElementsByTagName('tsUpdated')[0].firstChild.data
        Domoticz.Log(tsUpdated)
        temperature = dom.getElementsByTagName('t_degreesC')[0].firstChild.data
        Domoticz.Log("Temperature = " + temperature + "°C")
        humidity = dom.getElementsByTagName('rh')[0].firstChild.data
        Domoticz.Log("Humidity = " + humidity)
        Devices[self.TEMPERATURE].Update(int(temperature),temperature)
        Devices[self.HUMIDITY].Update(int(humidity),humidity)
        return True

_plugin = BasePlugin()

def onStart():
    _plugin.onStart()

def onHeartbeat():
    _plugin.onHeartbeat()

#############################################################################
#                         Domoticz helper functions                         #
#############################################################################

#############################################################################
#                       Device specific functions                           #
#############################################################################
