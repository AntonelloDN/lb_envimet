# ENVI-Met Soil Data Settings
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
This component let you change the inital temperature and initial relative humidity of the ground. For more info see the official website of ENVI_MET.
-
Connect the output to LB ENVI-Met Core Configuration.
-
Provided by Ladybug 0.0.65
    
    Args:
        _initialTempUpperLayer_: Initial Temperature Upper Layer (0-20 cm) [C]. Defualt vale is 19.85 C.
        _initialTempMiddleLayer_: Initial Temperature Middle Layer (20-50 cm) [C]. Defualt vale is 19.85 C.
        _initialTempDeepLayer_: Initial Temperature Deep Layer (below 50 cm) [C]. Defualt vale is 19.85 C.
        _RHupperLayer_: Relative Humidity Upper Layer (0-20 cm). Default value is 50.00%.
        _RHmiddleLayer_: Relative Humidity Middle Layer (20-50 cm). Default value is 60.00%.
        _RHdeepLayer_: Relative Humidity Deep Layer (below 50 cm). Default value is 60.00%.
    Returns:
        readMe!: ...
        soilData: Settings of SIM file. Connect it to LB ENVI-Met Core Configuration.
"""

ghenv.Component.Name = "Ladybug_ENVI-Met Soil Data Settings"
ghenv.Component.NickName = 'ENVI-MetSoilDataSettings'
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


def main():
    if _initialTempUpperLayer_:
        initialTempUpperLayer = round(_initialTempUpperLayer_, 2) + 273.15
    else:
        initialTempUpperLayer = 19.85 + 273.15
    if _initialTempMiddleLayer_:
        initialTempMiddleLayer = round(_initialTempMiddleLayer_, 2) + 273.15
    else:
        initialTempMiddleLayer = 19.85 + 273.15
    if _initialTempDeepLayer_:
        initialTempDeepLayer = round(_initialTempDeepLayer_, 2) + 273.15
    else:
        initialTempDeepLayer = 19.85 + 273.15
    
    if _RHupperLayer_:
        RHupperLayer = round(_RHupperLayer_, 2)
    else:
        RHupperLayer = 50.00
    if _RHmiddleLayer_:
        RHmiddleLayer = round(_RHmiddleLayer_, 2)
    else:
        RHmiddleLayer = 60.00
    if _RHdeepLayer_:
        RHdeepLayer = round(_RHdeepLayer_, 2)
    else:
        RHdeepLayer = 60.00
    
    soilData = settings.soilDataSettings(initialTempUpperLayer, initialTempMiddleLayer, initialTempDeepLayer, RHupperLayer, RHmiddleLayer, RHdeepLayer)
    
    return soilData


result = main()
if result != -1:
    soilData = result