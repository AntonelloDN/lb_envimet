# ENVI-Met Timing Settings
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
Use this component to change timing settings of your model. Pay attention when you change these values, it require experience.
-
Connect the output to LB ENVI-Met Core Configuration.
-
Provided by Ladybug 0.0.65
    
    Args:
        _dataSurface_: Update Surface Data each  ? sec. Default value is 30.00 seconds.
        _wind_: Update Wind field each ? sec. Default value is 900.00 seconds.
        _radiation_: Update Radiation and Shadows each ? sec. Default value is 600.00 seconds.
        _plant_: Update Plant Data each ? sec. Default value is 600.00 seconds.
    Returns:
        readMe!: ...
        timing: Settings of SIM file. Connect it to LB ENVI-Met Core Configuration.
"""

ghenv.Component.Name = "Ladybug_ENVI-Met Timing Settings"
ghenv.Component.NickName = 'ENVI-MetTimingSettings'
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
    if _dataSurface_:
        dataSurface = round(_dataSurface_, 2)
    else:
        dataSurface = 30.00
    if _wind_:
        wind = _wind_
    else:
        wind = 900.00
    if _radiation_:
        radiation = round(_radiation_, 2)
    else:
        radiation = 600.00
    if _plant_:
        plant = round(_plant_, 2)
    else:
        plant = 600.00
        
    timing = settings.timingSettings(dataSurface, wind, radiation, plant)
    
    return timing


result = main()
if result != -1:
    timing = result