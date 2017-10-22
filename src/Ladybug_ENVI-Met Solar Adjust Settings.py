# ENVI-Met Solar Adjust Settings
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
Use this component to alterate solar irradiation within your simulation. Please, note that this setting is optional.
-
Connect it to LB ENVI-Met Core Configuration.
-
Provided by Ladybug 0.0.65
    
    Args:
        _value_: Factor of shortwave adjustment (0.5 to 1.5). Default value is 1.0.
    Returns:
        readMe!: ...
        solarAdjust: Settings of SIM file. Connect it to LB ENVI-Met Core Configuration.
"""

ghenv.Component.Name = "Ladybug_ENVI-Met Solar Adjust Settings"
ghenv.Component.NickName = 'ENVI-MetSolarAdjustSettings'
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
    if (value < 1.0 or value > 1.5) and value != None:
        return
    else:
        return True


def main():
    if _value_:
        value = _value_
    else: value = 1.0
    
    solarAdjust = settings.solarAdjustSettings(value)
    
    return solarAdjust

if checkInputs(_value_):
    result = main()
    if result != -1:
        solarAdjust = result
else:
    w = gh.GH_RuntimeMessageLevel.Warning
    ghenv.Component.AddRuntimeMessage(w, "Please, provide a value from 1.0 to 1.5.")