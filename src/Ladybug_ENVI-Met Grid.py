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
Provided by Ladybug 0.0.65
    
    Args:
        dimX_: Size of grid cell in meter. Default value is 3.0.
        dimY_: Size of grid cell in meter. Default value is 3.0.
        dimZ_: Size of grid cell in meter. Default value is 3.0.
        _ENVImetVersion_: Version of ENVI-met to use for simulation. 0: 100x100x40; 1: 150x150x35 (Pro only); 2: 250x250x25 (Pro only) 
        numCellsZ_: Number grid for Height domain. Default 15
        _telescope_:    Choose telescope option if your Z domain can't be reached with equidistant Z grid. Default: 5 (growing percentage)
        startTelescopeHeight_: Height where to start the telesscoping Z grid growth. Default: 5.0
        addCellsLeft_: Default: 2
        addCellsUp_: Default: 2
        addCellslRight_: Default: 2
        addCellsDown_: Default: 2
    Returns:
        readMe!: ...
        envimentGrid: Connect this output to "ENVI-Met Spaces" in order to add sources to ENVI-Met model.
"""

ghenv.Component.Name = "Ladybug_ENVI-Met Grid"
ghenv.Component.NickName = 'ENVI-MetGrid'
ghenv.Component.Message = 'VER 0.0.65\nJUL_28_2017'
ghenv.Component.IconDisplayMode = ghenv.Component.IconDisplayMode.application
ghenv.Component.Category = "Ladybug"
ghenv.Component.SubCategory = "7 | WIP"
#compatibleLBVersion = VER 0.0.59\nFEB_01_2015
try: ghenv.Component.AdditionalHelpFromDocStrings = "1"
except: pass


import os
import sys
import scriptcontext as sc
import Grasshopper.Kernel as gh
import Rhino as rc
##################LB ENVI_MET###################
userPath = os.getenv("APPDATA")
path = os.path.join(userPath, "lb_envimet")
sys.path.append(path)
from envimetObj import autoGrid, material
################################################



def main():
    
    envimentGrid = autoGrid.setGrid()
    
    if _ENVImetVersion_:
        envimentGrid.ENVImetVersion = _ENVImetVersion_
    if _telescope_:
        envimentGrid.telescope = _telescope_
        if _telescope_ >= 20.0:
            w = gh.GH_RuntimeMessageLevel.Warning
            message = "max telescope factor is 20.".format(envimentGrid.maxZGrid)
            ghenv.Component.AddRuntimeMessage(w, message)
            envimentGrid.zGrids = envimentGrid.maxZGrid - 1
            envimentGrid.telescope = 20.0
    if dimX_:
        envimentGrid.dimX = dimX_
    if dimY_:
        envimentGrid.dimY = dimY_
    if dimZ_:
        envimentGrid.dimZ = dimZ_
    if startTelescopeHeight_:
        envimentGrid.startTelescopeHeight = startTelescopeHeight_
    if addCellsLeft_:
        envimentGrid.extLeftXgrid = addCellsLeft_
    if addCellslRight_ and addCellslRight_ > 2:
        envimentGrid.extRightXgrid = addCellslRight_
    if addCellsUp_ and addCellsUp_ > 2:
        envimentGrid.extUpYgrid = addCellsUp_
    if addCellsDown_ and addCellsDown_ > 2:
        envimentGrid.extDownYgrid = addCellsDown_
    if numCellsZ_ and numCellsZ_ > 2:
        envimentGrid.zGrids = numCellsZ_
    if numCellsZ_ >= envimentGrid.maxZGrid:
        w = gh.GH_RuntimeMessageLevel.Warning
        message = "numCellsZ_ should be less than {}".format(envimentGrid.maxZGrid)
        ghenv.Component.AddRuntimeMessage(w, message)
        envimentGrid.zGrids = envimentGrid.maxZGrid - 1
    
    return envimentGrid

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
        envimentGrid = result