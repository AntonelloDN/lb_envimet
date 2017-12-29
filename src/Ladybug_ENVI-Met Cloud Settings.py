# ENVI-Met Cloud Settings
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
Use this component to add cloud to your model. The default setting is with no clouds.
-
Connect the output to LB ENVI-Met Core Configuration.
-
Provided by Ladybug 0.0.65
    
    Args:
        _lowValue_: Fraction of LOW clouds (x/8). Default value is 0 (no clouds).
        _middleValue_: Fraction of MIDDLE clouds (x/8). Default value is 0 (no clouds).
        _highValue_: Fraction of HIGH clouds (x/8). Default value is 0 (no clouds).
    Returns:
        readMe!: ...
        solarAdjust: Settings of SIM file. Connect it to LB ENVI-Met Core Configuration.
"""

ghenv.Component.Name = "Ladybug_ENVI-Met Cloud Settings"
ghenv.Component.NickName = 'ENVI-MetCloudSettings'
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


def checkInputs(value):
    if (value < 0.00 or value > 8.00) and value != None:
        return -1
    else:
        return True


def main():
    if _lowValue_:
        if checkInputs(_lowValue_):
            lowValue = _lowValue_
    else:
        lowValue = 0.00
    
    if _middleValue_:
        if checkInputs(_middleValue_):
            middleValue = _middleValue_
    else:
        middleValue = 0.00
    
    if _highValue_:
        if checkInputs(_highValue_):
            highValue = _highValue_
    else:
        highValue = 0.00
            
    clouds = settings.cloudSettings(lowValue, middleValue, highValue)
    
    return clouds


result = main()
if result != -1:
    clouds = result
else:
    w = gh.GH_RuntimeMessageLevel.Warning
    ghenv.Component.AddRuntimeMessage(w, "Please, provide a value from 0.00 to 8.00.")