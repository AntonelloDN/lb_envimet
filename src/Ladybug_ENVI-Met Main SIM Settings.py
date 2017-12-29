# ENVI-Met Main SIM Settings
#
# Ladybug: A Plugin for Environmental Analysis (GPL) started by Mostapha Sadeghipour Roudsari
# 
# This file is part of Ladybug.
# 
# Copyright (c) 2013-2018, Antonello Di Nunzio <antonellodinunzio@gmail.com> 
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
This component is necessary for simulation settings.
-
Connect the output to LB ENVI-Met Core Configuration.
-
Provided by Ladybug 0.0.65
    
    Args:
        _SIMname_: Filebase name for Output (Text).
        _INXfileAddress: Connect INXfileAddress which comes from "LB ENVI-Met Spaces".
        _projectName_: Name for Simulation (Text).
        _date: Start Simulation at Day (DD.MM.YYYY) and time (HH:MM:SS). Use LB ENVI-Met Start Date.
        _totalTime_: Total Simulation Time in Hours. Default value is 24. Usually from 24 to 48 hours.
        ---------------------------:(...)
        _windSpeed_: Wind Speed in 10 m ab. Ground [m/s]. Default value is 3.0 m/s.
        _windDirection_: Wind Direction (0:N..90:E..180:S..270:W..). Default value is 0.
        _roughness_: Roughness Length z0 at Reference Point [m]. Default value is 0.01.
        _initialTemperature_: Initial Temperature Atmosphere [C]. Default value is 21 C.
        _specificHumidity_: Specific Humidity in 2500 m [g Water/kg air]. Default value is 7.0.
        _relativeHumidity_: Relative Humidity in 2m [%]. Default value is 50%.
        ---------------------------:(...)
        _outputIntervalMainFile_: Output interval main files (min). Default value is 60.00 min (hour by hour you have an output file).
        _outputIntervalText_: Output interval text output files (min). Default value is 30.00 min.
        _includeNestingGrids_: Include Nesting Grids in Output (0:N,1:Y). Connect a boolean toggle to set it.
        Default value is False ('N').
    Returns:
        readMe!: ...
        mainSettings: Basic settings of SIM file. Connect it to LB ENVI-Met Core Configuration.
"""

ghenv.Component.Name = "Ladybug_ENVI-Met Main SIM Settings"
ghenv.Component.NickName = 'ENVI-Met MainSIMsettings'
ghenv.Component.Message = 'VER 0.0.65\nJUL_28_2017'
ghenv.Component.IconDisplayMode = ghenv.Component.IconDisplayMode.application
ghenv.Component.Category = "Ladybug"
ghenv.Component.SubCategory = "7 | WIP"
#compatibleLBVersion = VER 0.0.59\nFEB_01_2015
try: ghenv.Component.AdditionalHelpFromDocStrings = "1"
except: pass


import Grasshopper.Kernel as gh
import sys
import os
##################LB ENVI_MET###################
userPath = os.getenv("APPDATA")
path = os.path.join(userPath, "lb_envimet")
sys.path.append(path)
from envimetStuff import settings
################################################


def checkInputs():
    if not _INXfileAddress or not _date:
        return
    else:
        return True


def main():
    if _INXfileAddress:
        fileName = _INXfileAddress.split('\\')[-1]
    else: fileName = "LBenvimet.INX"
    if _projectName_: projectName = _projectName_
    else: projectName = "LBDATA"
    if _SIMname_: SIMname = _SIMname_
    else: SIMname = "NewSimulation"
    if _totalTime_: totalTime = _totalTime_
    else: totalTime = 24
    if _windSpeed_: windSpeed = round(_windSpeed_,1)
    else: windSpeed = 3.0
    if _windDirection_: windDirection = _windDirection_
    else: windDirection = 0
    if _roughness_: roughness = round(_roughness_,2)
    else: roughness = 0.01
    if _initialTemperature_: initialTemperature = round(_initialTemperature_,3) + 273.150 
    else: initialTemperature = 294.150
    if _specificHumidity_: specificHumidity = round(_specificHumidity_,1)
    else: specificHumidity = 7.0
    if _relativeHumidity_: relativeHumidity = int(round(_relativeHumidity_,0))
    else: relativeHumidity = 50
    
    if _outputIntervalMainFile_: outputIntervalMainFile = round(_outputIntervalMainFile_,2)
    else: outputIntervalMainFile = 60.00
    if _outputIntervalText_: outputIntervalText = round(_outputIntervalText_,2)
    else: outputIntervalText = 30.00
    if _includeNestingGrids_ == True:
        includeNestingGrids = '1'
    else:
        includeNestingGrids = '0'
    
    # check
    if totalTime > 48:
        w = gh.GH_RuntimeMessageLevel.Warning
        ghenv.Component.AddRuntimeMessage(w, "Please, simulation time should less than 48.")
    
    # time
    startSimulation = _date.strftime("%d.%m.%Y")
    startSimulationTime = _date.strftime("%H.%M.%S")
    
    
    mainSettings = settings.mainSettings(projectName, fileName, SIMname, startSimulation, \
    startSimulationTime, totalTime, windSpeed, windDirection, roughness, initialTemperature, \
    specificHumidity, relativeHumidity, outputIntervalMainFile, outputIntervalText, includeNestingGrids)
    
    return mainSettings

if checkInputs():
    result = main()
    if result != -1:
        mainSettings = result
else:
    w = gh.GH_RuntimeMessageLevel.Warning
    ghenv.Component.AddRuntimeMessage(w, "Please, provide _date and _fileName.")