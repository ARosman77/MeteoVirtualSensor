# Meteo.si Virutal Sensor
#
# Author: ARosman77
#
"""
<plugin key="Meteo.si" name="Meteo.si Virtual Sensor" author="ARosman77" version="1.0.0">
    <params>
        <param field="Mode1" label="Meteo.si URL" width="200px" required="true" default="http://www.meteo.si/uploads/probase/www/observ/surface/text/sl/observationAms_si_latest.xml"/>
        <param field="Mode2" label="Station name" width="200px" required="true">
            <options>
                <option label="Ljubljana" value="LJUBLJANA - BEŽIGRAD" default="true" />
                <option label="Velenje" value="VELENJE" />
                <option label="Novo Mesto" value="NOVO MESTO" />
            </options>
        </param>
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
from meteo import meteoData 
import urllib.request
from xml.dom import minidom

#############################################################################
#                      Domoticz call back functions                         #
#############################################################################

class BasePlugin:
    
    dataStation = None
    
    def __init__ (self):
        self.hbCounter = 0
        self.interval = 10
        return

    def onStart(self):
        
        global dataStation
        Domoticz.Log("onStart called")
        
        # connect to Meteo.si with set paramters
        Domoticz.Log("Connecting to Meteo.si ...")
        
        # debug
        for x in Parameters:
            if Parameters[x] != "":
                Domoticz.Log( "'" + x + "':'" + str(Parameters[x]) + "'")
        
        if Parameters["Mode1"] != "" and Parameters["Mode2"] != "":
            dataStation = meteoData(Parameters["Mode1"],'domain_shortTitle',Parameters["Mode2"])
        else:
            dataStation = meteoData("http://www.meteo.si/uploads/probase/www/observ/surface/text/sl/observationAms_si_latest.xml",'domain_shortTitle','LJUBLJANA - BEŽIGRAD')
                
        # get read interval from settings
        if Parameters["Mode3"] != "" :
            self.interval = int(Parameters["Mode3"])
            
        if self.interval == None:
            Domoticz.Log("Unable to parse interval, so set it to 10 minutes")
            self.interval = 10
        # Allowing values below 10 minutes will not get you more info
        if self.interval < 10:
            Domoticz.Log("Interval too small, changed to 10 minutes")
            self.interval = 10
        
        # create devices
        createDevices()
        
        # update devices data
        updateDevices()
        
        # set heartbeat interval
        Domoticz.Heartbeat(30)

    def onHeartbeat(self):
        # increase heartbeat counter (30s)
        self.hbCounter += 1
        if self.hbCounter >= (self.interval*2):
            Domoticz.Log("Updating Mete.si data ...")
            self.hbCounter = 0
            updateDevices()
        return True

_plugin = BasePlugin()

def onStart():
    _plugin.onStart()

def onHeartbeat():
    _plugin.onHeartbeat()

#############################################################################
#                         Domoticz helper functions                         #
#############################################################################

# Update Device into database
def UpdateDevice(Unit, nValue, sValue, AlwaysUpdate=False):
    # Make sure that the Domoticz device still exists (they can be deleted) before updating it
    if Unit in Devices:
        if Devices[Unit].nValue != nValue or Devices[Unit].sValue != sValue or AlwaysUpdate == True:
            Devices[Unit].Update(nValue, str(sValue))
            Domoticz.Log("Update " + Devices[Unit].Name + ": " + str(nValue) + " - '" + str(sValue) + "'")
    return

#############################################################################
#                       Device specific functions                           #
#############################################################################

def createDevices():

    # Are there any devices?
    ###if len(Devices) != 0:
        # Could be the user deleted some devices, so do nothing
        ###return

    # Give the devices a unique unit number. This makes updating them more easy.
    # UpdateDevice() checks if the device exists before trying to update it.

    # Add the temperature and humidity device(s)
    if Parameters["Mode4"] == "True":
        if 3 not in Devices:
            Domoticz.Device(Name="Temperature", Unit=3, TypeName="Temp+Hum", Used=1).Create()
    else:
        if 1 and 2 not in Devices:
            Domoticz.Device(Name="Temperature", Unit=1, TypeName="Temperature", Used=1).Create()
            Domoticz.Device(Name="Humidity", Unit=2, TypeName="Humidity", Used=1).Create()

    # Add the barometer device
    if 4 not in Devices:
        Domoticz.Device(Name="Barometer", Unit=4, TypeName="Barometer", Used=1).Create()

    # Add the wind device
    if 5 not in Devices:
        Domoticz.Device(Name="Wind", Unit=5, TypeName="Wind", Used=1).Create()
    
    # Add the Visibility device
    if 7 not in Devices:
        Domoticz.Device(Name="Visibility", Unit=7, TypeName="Visibility", Used=1).Create()
    
    # Add the Solar Radiation device
    if 8 not in Devices:
        Domoticz.Device(Name="Solar Radiation", Unit=8, TypeName="Solar Radiation", Used=1).Create()
    
    Domoticz.Log("Devices checked and created/updated if necessary")

def updateDevices():

    # Refresh data and update devices
    dataStation.refreshData()
    
    # Temperature
    if dataStation.getTemperature() != None:
        UpdateDevice(1, 0, dataStation.getTemperature())

    # Humidity
    if dataStation.getHumidity() != None:
        UpdateDevice(2, int(dataStation.getHumidity()), dataStation.getHumidity())

    # Temperature and Humidity
    if dataStation.getTemperature() != None and dataStation.getHumidity() != None:
        UpdateDevice(3, 0,
                dataStation.getTemperature()
                + ";" + dataStation.getHumidity()
                + ";" + dataStation.getHumidity())

    # Barometer
    if dataStation.getAtmPressure() != None:
        UpdateDevice(4, 0,
                dataStation.getAtmPressure()
                + ";" + dataStation.getAtmPressure())

    # Visibility
    if dataStation.getVisibility() != None:
        UpdateDevice(7, 0, dataStation.getVisibility())

    # Solar Radiation
    if dataStation.getGlobalSunRad() != None:
        UpdateDevice(8, 0, dataStation.getGlobalSunRad())
