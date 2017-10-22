# ENVI-Met LBC Settings
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
This component let you change boundary condition of the model.
-
Connect the output to LB ENVI-Met Core Configuration.
-
Provided by Ladybug 0.0.65
    
    Args:
        _lbcTq_: Lateral Boundary Condition for Temperature and humidity. Default value is 0 (Open).
        -
        Connect a value from 1 to 3:
        1 = Open
        2 = Forced
        3 = Cyclic
        -
        For more info see official documentation of ENVI_MET.
        _lbcTKE_: Lateral Boundary Condition for Turbulence. Default value is 0 (Open).
        -
        Connect a value from 0 to 2:
        1 = Open
        2 = Forced
        3 = Cyclic
        -
        For more info see official documentation of ENVI_MET.
    Returns:
        readMe!: ...
        lbcTypes: Settings of SIM file. Connect it to LB ENVI-Met Core Configuration.
"""

ghenv.Component.Name = "Ladybug_ENVI-Met LBC Settings"
ghenv.Component.NickName = 'ENVI-MetLBCSettings'
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
    
    w = gh.GH_RuntimeMessageLevel.Warning
    
    if _lbcTq_:
        if 0<_lbcTq_<4:
            lbcTq = _lbcTq_
        else:
            lbcTq = 1
            ghenv.Component.AddRuntimeMessage(w, "Connect a value from 1 to 3.")
    else:
        lbcTq = 1
    if _lbcTKE_:
        if 0<_lbcTKE_<4:
            lbcTKE = _lbcTKE_
        else:
            lbcTKE = 1
            ghenv.Component.AddRuntimeMessage(w, "Connect a value from 1 to 3.")
    else:
        lbcTKE = 1
    
    lbcTypes = settings.lbcTypesSettings(lbcTq, lbcTKE)
    
    return lbcTypes


result = main()
if result != -1:
    lbcTypes = result