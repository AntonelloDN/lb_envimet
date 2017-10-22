# ENVI-Met Simple Force by EPW
#
# Ladybug: A Plugin for Environmental Analysis (GPL) started by Mostapha Sadeghipour Roudsari
# 
# This file is part of Ladybug.
# 
# Copyright (c) 2013-2017, Antonello Di Nunzio <antonellodinunzio@gmail.com> 
# Ladybug is free software; you can redistribute it and/or modify 
# it under the terms of the GNU General Public License as published 
# by the Free Software Foundation; either version 3 of the License, 
# or (at your option) any later version. 
# 
# Ladybug is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Ladybug; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>


"""
This component let you force climate condition of the simulation. Data of this component comes from EPW file.
Basically, it extract 24 values of temperature and relative humidity by using DOY.
-
It is a good element to find a relation between calculation with EnergyPlus and calculation with ENVI_MET.
-
Connect "simpleForce" to LB ENVI-Met Core Configuration.
-
Provided by Ladybug 0.0.65
    
    Args:
        _epwFile:  An .epw file path on your system as a string.
        _DOY: The day of the year. Connect a number from 1 to 365.
        -
        It is compatible with "Ladybug_DOY_HOY".
    Returns:
        readMe!: ...
        dryBulbTemperature: The dry bulb temperature values [C] from selected day.
        relativeHumidity: The relative humidity values [%] from selected day.
        ------------------------ : (...)
        simpleForce: Settings of SIM file. Connect it to LB ENVI-Met Core Configuration.
"""

ghenv.Component.Name = "Ladybug_ENVI-Met Simple Force by EPW"
ghenv.Component.NickName = 'ENVI-MetSimpleForceByEPW'
ghenv.Component.Message = 'VER 0.0.65\nJUL_28_2017'
ghenv.Component.IconDisplayMode = ghenv.Component.IconDisplayMode.application
ghenv.Component.Category = "Ladybug"
ghenv.Component.SubCategory = "7 | WIP"
#compatibleLBVersion = VER 0.0.59\nFEB_01_2015
try: ghenv.Component.AdditionalHelpFromDocStrings = "1"
except: pass


import Grasshopper.Kernel as gh
import scriptcontext as sc
import sys
import os
##################LB ENVI_MET###################
userPath = os.getenv("APPDATA")
path = os.path.join(userPath, "lb_envimet")
sys.path.append(path)
from envimetStuff import settings
################################################

def extractNumbers(listName, DOY):
    chunks = [listName[n:n+24] for n in range(0, len(listName), 24)]
    return chunks[DOY]

def main():
    
    if _DOY:
        DOY = _DOY - 1
    else:
        DOY = 145
    
    weatherData = lb_preparation.epwDataReader(_epwFile)
    temperatureData = weatherData[0][7:]
    RHdata = weatherData[2][7:]
    
    dryBulbTemperature = extractNumbers(temperatureData, DOY)
    relativeHumidity = extractNumbers(RHdata, DOY)
    
    simpleForce = settings.simpleForceSettings(dryBulbTemperature, relativeHumidity)
    
    return dryBulbTemperature, relativeHumidity, simpleForce


# import the classes
initCheck = False
w = gh.GH_RuntimeMessageLevel.Warning
if sc.sticky.has_key('ladybug_release'):
    initCheck = True
    try:
        if not sc.sticky['ladybug_release'].isCompatible(ghenv.Component): initCheck = True
    except:
        initCheck = False
        warning = "You need a newer version of Ladybug to use this compoent." + \
        "Use updateLadybug component to update userObjects.\n" + \
        "If you have already updated userObjects drag Ladybug_Ladybug component " + \
        "into canvas and try again."
        ghenv.Component.AddRuntimeMessage(w, warning)
    lb_preparation = sc.sticky["ladybug_Preparation"]()
else:
    initCheck = False
    print "You should first let the Ladybug fly..."
    ghenv.Component.AddRuntimeMessage(w, "You should first let the Ladybug fly...")


#Check the data
if _epwFile and _DOY:
    
    if initCheck == True:
        result = main()
        if result != -1:
            dryBulbTemperature, relativeHumidity, simpleForce = result
else:
    ghenv.Component.AddRuntimeMessage(w, "Connect all inputs.")