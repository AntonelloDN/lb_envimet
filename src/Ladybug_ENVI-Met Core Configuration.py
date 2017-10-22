# ENVI-Met Core Configuration
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
This component generates SIM files which are necessary for simulation.
-
Provided by Ladybug 0.0.65
    
    Args:
        ENVImetInstallFolder_: Optional folder path for ENVImet4 installation folder.
        _envimetFolder: Envimet project folder.
        ------------------------: (...)
        _mainSettings: Basic settings to run a simulation with ENVI_MET (required input from ENVI-Met MainSIMsettings).
        timing_: Connect the output comes from ENVI-MetTimingSettingsName to change timing settings.
        solarAdjust_: Connect the output comes from ENVI-MetSolarAdjustSettings to change solar irradiation settings.
        clouds_: Connect the output comes from ENVI-MetCloudSettings to consider clouds for your simulation.
        timesteps_: Connect the output comes from ENVI-MetTimestepsSettings to change timesteps of the sun.
        soilData_: Connect the output comes from ENVI-MetSoilDataSettings to change initial condition of the ground (temperature and relative humidiy).
        simpleForce_: Connect the output comes from ENVI-MetSimpleForceByEPW to force climatic condition using data of a day of a EPW file.
        lbcType_: Connect the output comes from ENVI-MetLBCSettings to change lateral boudary condition.
        turbulence_: Connect the output comes from ENVI-MetLBCSettings to change turbulence settings.
        ------------------------: (...)
        _writeIt: Set True to write the SIM file.
        runHeadquarter_: Set True to open ENVI_MET Headquarter directly where you can run the simulation.
        -
        Select ENVI-met / Version(...) / Load Simulation. It open the folder where SIM file is saved.
    Returns:
        readMe!: ...
        SIMfileAddress: full path of SIM file on your machine.
"""

ghenv.Component.Name = "Ladybug_ENVI-Met Core Configuration"
ghenv.Component.NickName = 'ENVI-MetCoreConfiguration'
ghenv.Component.Message = 'VER 0.0.65\nJUL_28_2017'
ghenv.Component.IconDisplayMode = ghenv.Component.IconDisplayMode.application
ghenv.Component.Category = "Ladybug"
ghenv.Component.SubCategory = "7 | WIP"
#compatibleLBVersion = VER 0.0.59\nFEB_01_2015
try: ghenv.Component.AdditionalHelpFromDocStrings = "1"
except: pass

import os
import Grasshopper.Kernel as gh


def checkENVIfolder():
    appdata = os.getenv("APPDATA")
    directory = os.path.join(appdata[:3], "ENVImet4")
    
    if os.path.isdir(directory):
        return True
    else:
        w = gh.GH_RuntimeMessageLevel.Warning
        ghenv.Component.AddRuntimeMessage(w, "Please, provide full path of your ENVI_MET installation folder.")
        return False


def main():
    
    text1 = _mainSettings.mainSettingsText
    
    if solarAdjust_:
        text2 = '\n' + solarAdjust_.solarAdjustSettingsText
    else:
        text2 = ''
    if clouds_:
        text3 = '\n' + clouds_.cloudSettingsText
    else:
        text3 = ''
    if timing_:
        text4 = '\n' + timing_.timingSettingsText
    else:
        text4 = ''
    if timesteps_:
        text5 = '\n' + timesteps_.timestepsSettingsText
    else:
        text6 = ''
    if soilData_:
        text6 = '\n' + soilData_.soilDataSettingsText
    else:
        text6 = ''
    if plantModel_:
        text7 = '\n' + plantModel_.plantModelSettingsText
    else:
        text7 = ''
    if simpleForce_:
        text8 = '\n' + simpleForce_.simpleForceSettingsText
    else:
        text8 = ''
    if lbcType_:
        text9 = '\n' + lbcType_.lbcTypesSettingsText
    else:
        text9 = ''
    if turbulence_:
        text10 = '\n' + turbulence_.turbulenceSettingsText
    else:
        text10 = ''
    
    fullPath = os.path.join(_envimetFolder, _mainSettings.SIMname + '.SIM')
    
    # write all
    with open(fullPath, "w") as f:
        f.write(text1 + text2 + text3 + text4 + text5 + text6 + text7 + text8 + text9 + text10)
    
    if checkENVIfolder():
        path = r"C:\ENVImet4\EnvimetHeadquarter.exe"
    else:
        path = ENVImetInstallFolder_
    if runHeadquarter_:
        os.startfile(path)
    
    return fullPath


if _envimetFolder and _mainSettings:
    if _writeIt:
        result = main()
        if result != -1:
            SIMfileAddress = result
            print("File written correctly.")
    else:
        print("Set writeIt to True.")
else:
    w = gh.GH_RuntimeMessageLevel.Warning
    ghenv.Component.AddRuntimeMessage(w, "Please, provide _envimetFolder and _mainSettings.")