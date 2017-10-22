# ENVI-Met Turbulence Settings
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
EXPERT SETTINGS
-
This component let you change turbulence closure of the model.
-
Connect the output to LB ENVI-Met Core Configuration.
-
Provided by Ladybug 0.0.65
    
    Args:
        _turbulence1d_: Turbulence schema for 1D ENVI_MET model. Default value is Prognostic.
        -
        Connect a boolean value:
        True = Prognostic TKE
        False = Diagnostic Mixing-Length
        _turbulence3d_: Turbulence schema for 3D ENVI_MET model. Default value is Prognostic.
        -
        Connect a boolean value:
        True = Prognostic TKE
        False = Diagnostic Mixing-Length
        _upperBoudary_: Upper Boundary condition for TKE. Default value is closed.
        _
        Connect a boolean value:
        True = Open
        False = Closed
    Returns:
        readMe!: ...
        turbulence: Settings of SIM file. Connect it to LB ENVI-Met Core Configuration.
"""

ghenv.Component.Name = "Ladybug_ENVI-Met Turbulence Settings"
ghenv.Component.NickName = 'ENVI-MetTurbulenceSettings'
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
    
    if _turbulence1d_:
        turbulence1d = 0
    else:
        turbulence1d = 1
    if _turbulence3d_:
        turbulence3d = 0
    else:
        turbulence3d = 1
    if _upperBoudary_:
        upperBoudary = 1
    else:
        upperBoudary = 0
    
    turbulence = settings.turbulenceSettings(turbulence1d, turbulence3d, upperBoudary)
    
    return turbulence


result = main()
if result != -1:
    turbulence = result