# ENVI-Met Grid
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
Use this component to set ENVI-Met grid for "LB ENVI-Met Spaces".
-
Provided by Ladybug 0.0.64
    
    Args:
        _numX_: Number of grid cells in base plane x direction. Default value is 25.
        _numY_: Number of grid cells in base plane y direction. Default value is 25.
        _numZ_: Number of grid cells in base plane z direction. Default value is 15.
        _dimX_: Size of grid cell in meter. Default value is 3.0.
        _dimY_: Size of grid cell in meter. Default value is 3.0.
        _dimZ_: Size of grid cell in meter. Default value is 3.0.
    Returns:
        readMe!: ...
        gridSettings: Connect this output to "ENVI-Met Spaces" in order to add sources to ENVI-Met model.
"""

ghenv.Component.Name = "Ladybug_ENVI-Met Grid"
ghenv.Component.NickName = 'ENVI-MetGrid'
ghenv.Component.Message = 'VER 0.0.64\nFEB_26_2017'
ghenv.Component.IconDisplayMode = ghenv.Component.IconDisplayMode.application
ghenv.Component.Category = "Ladybug"
ghenv.Component.SubCategory = "7 | WIP"
#compatibleLBVersion = VER 0.0.62\nJUN_07_2016
try: ghenv.Component.AdditionalHelpFromDocStrings = "1"
except: pass


import os
import sys
import scriptcontext as sc
import Grasshopper.Kernel as gh
##################LB ENVI_MET###################
userPath = os.getenv("APPDATA")
path = os.path.join(userPath, "lb_envimet")
sys.path.append(path)
from envimetObj import grid
################################################


def main():
    
    if _numX_ == None:
        numX = 25
    else:
        numX = _numX_ 
    if _numY_ == None:
        numY = 25
    else:
        numY = _numY_ 
    if _numZ_ == None:
        numZ = 15
    else:
        numZ = _numZ_ 
    
    if _dimX_ == None:
        dimX = 3.0
    else:
        dimX = _dimX_ 
    if _dimY_ == None:
        dimY = 3.0
    else:
        dimY = _dimY_
    if _dimZ_ == None:
        dimZ = 3.0
    else:
        dimZ = _dimZ_
    
    
    gridSettings = grid.Grid2D(numX, numY, numZ, dimX, dimY, dimZ)
    
    return gridSettings


initCheck = False
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
        w = gh.GH_RuntimeMessageLevel.Warning
        ghenv.Component.AddRuntimeMessage(w, warning)
else:
    initCheck = False
    print "You should first let the Ladybug fly..."
    w = gh.GH_RuntimeMessageLevel.Warning
    ghenv.Component.AddRuntimeMessage(w, "You should first let the Ladybug fly...")


if initCheck:
    result = main()
    if result != -1:
        gridSettings = result

