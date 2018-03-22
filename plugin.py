# Meteo.si Virutal Sensor
#
# Author: ARosman77
#
"""
<plugin key="MeteoSI" name="Meteo.si Virtual Sensor" author="ARosman77" version="1.0.0" wikilink="" externallink="">
    <params>
        <param field="Address" label="Meteo.si URL" width="600px" required="true" default="http://www.meteo.si/uploads/probase/www/observ/surface/text/sl/observationAms_si_latest.xml"/>
        <param field="Mode2" label="Station name" width="200px" required="true">
            <options>
                <option label="Ljubljana" value="LJUBLJANA - BEŽIGRAD" default="true" />
                <option label="Velenje" value="VELENJE" />
                <option label="Novo Mesto" value="NOVO MESTO" />
            </options>
        </param>
        <param field="Mode3" label="Update every x minutes" width="60px" required="true" default="10"/>
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
    
    # dataStation = None
    
    def __init__ (self):
        self.hbCounter = 0
        self.interval = 10
        self.dataStation = None
        return

    def onStart(self):
        
        # global dataStation
        Domoticz.Log("onStart called")
        
        # connect to Meteo.si with set paramters

        if Parameters["Address"] != "" and Parameters["Mode2"] != "":
            self.dataStation = meteoData(Parameters["Address"],'domain_shortTitle',Parameters["Mode2"])
        else:
            self.dataStation = meteoData("http://www.meteo.si/uploads/probase/www/observ/surface/text/sl/observationAms_si_latest.xml",'domain_shortTitle','LJUBLJANA - BEŽIGRAD')
                
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
        updateDevices(self.dataStation)
        
        # set heartbeat interval
        Domoticz.Heartbeat(30)
        # Domoticz.Heartbeat(10)

    def onHeartbeat(self):
        # increase heartbeat counter (30s)
        self.hbCounter += 1
        if self.hbCounter >= (self.interval*2):
            self.hbCounter = 0
            updateDevices(self.dataStation)
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

def updateDevices(dataStation):

    # Refresh data and update devices
    dataStation.refreshData()
    
    # Temperature
    if dataStation.getTemperature() != None:
        UpdateDevice(1, 0, dataStation.getTemperature())
    
    # Humidity
    # -- Mapping for Humidity_status:
    #  -- 0    			    = Normal 
    #  -- 1    <> 46-70%   	= Comfortable 
    #  -- 2    < 38        	= Dry
    #  -- 3    > 70%       	= Wet
    if dataStation.getHumidity() != None:
        _humidity = int(dataStation.getHumidity())
        _humidity_status = 0
        if (_humidity >= 46) and (_humidity <= 70):
            _humidity_status = 1
        if (_humidity < 38):
            _humidity_status = 2
        if (_humidity > 70):
            _humidity_status = 3
        UpdateDevice(2, _humidity, str(_humidity_status))

    # Temperature and Humidity
    if dataStation.getTemperature() != None and dataStation.getHumidity() != None:
        UpdateDevice(3, 0,
                dataStation.getTemperature()
                + ";" + dataStation.getHumidity()
                + ";" + str(_humidity_status))

    # Barometer
    if dataStation.getAtmPressure() != None:
        UpdateDevice(4, 0,
                dataStation.getAtmPressure()
                + ";" + str(0) )    # Barometer forecast not implemented

    # Visibility
    if dataStation.getVisibility() != None:
        UpdateDevice(7, 0, dataStation.getVisibility())

    # Solar Radiation
    if dataStation.getGlobalSunRad() != None:
        UpdateDevice(8, 0, dataStation.getGlobalSunRad())
