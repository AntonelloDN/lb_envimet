# ENVI-Met Timesteps Settings
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
ADVANCED SETTINGS
-
This component let you change the timestep of the sun. For more info see the official website of ENVI_MET.
-
Connect the output to LB ENVI-Met Core Configuration.
-
Provided by Ladybug 0.0.65
    
    Args:
        _sunheightDelta0_: Sun height for switching dt(0). Defualt vale is 40.00 deg.
        -
        meaning = From 0 deg to 40.00 deg the time step of sun will be _timeStepInterval1_.
        _sunheightDelta1_: Sun height for switching dt(1). Defualt vale is 50.00 deg.
        -
        meaning = From 40.00 deg to 50.00 deg the time step of sun will be _timeStepInterval2_.
        _timeStepInterval1_: Time step (s) for interval 1 dt(0). Default value is 2 seconds.
        _timeStepInterval2_: Time step (s) for interval 1 dt(0). Default value is 2 seconds.
        _timeStepInterval3_: Time step (s) for interval 1 dt(0). Default value is 1 seconds.
        -
        You have much more radiation when the sun is high in the sky, for this reason ENVI_MET apply timestep 1 s when elevation degree is greater than 50.00 deg.
    Returns:
        readMe!: ...
        timesteps: Settings of SIM file. Connect it to LB ENVI-Met Core Configuration.
"""

ghenv.Component.Name = "Ladybug_ENVI-Met Timesteps Settings"
ghenv.Component.NickName = 'ENVI-MetTimestepsSettings'
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
    if _sunheightDelta0_:
        sunheightDelta0 = round(_sunheightDelta0_, 2)
    else:
        sunheightDelta0 = 40.00
    if _sunheightDelta1_:
        sunheightDelta1 = _sunheightDelta1_
    else:
        sunheightDelta1 = 50.00
    if _timeStepInterval1_:
        timeStepInterval1 = round(_timeStepInterval1_, 2)
    else:
        timeStepInterval1 = 2.00
    if _timeStepInterval2_:
        timeStepInterval2 = round(_timeStepInterval2_, 2)
    else:
        timeStepInterval2 = 2.00
    if _timeStepInterval3_:
        timeStepInterval3 = round(_timeStepInterval3_, 2)
    else:
        timeStepInterval3 = 1.00
        
    timesteps = settings.timestepsSettings(sunheightDelta0, sunheightDelta1, timeStepInterval1, timeStepInterval2, timeStepInterval3)
    
    return timesteps


result = main()
if result != -1:
    timesteps = result