# lb_envimet: A series of component for ENVI_MET
# 
# It depends on Ladybug Legacy.
# 
# Copyright (c) 2013-2019, Antonello Di Nunzio <antonellodinunzio@gmail.com> 
# lb_envimet is free software; you can redistribute it and/or modify 
# it under the terms of the GNU General Public License as published 
# by the Free Software Foundation; either version 3 of the License, 
# or (at your option) any later version. 
# 
# lb_envimet is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with lb_envimet; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>


"""
Use this component to set ENVI-Met grid for "lb_envimet Spaces".
-
Some components depend on Ladybug Legacy, please install Ladybug Legacy.
-
Provided by lb_envimet
    
    Args:
        _baseSurface_: Connect a planar XY surface to create the grid base on a surface.
        dimX_: Size of grid cell in meter. Default value is 3.0.
        dimY_: Size of grid cell in meter. Default value is 3.0.
        dimZ_: Size of grid cell in meter. Default value is 3.0.
        numCellsZ_: Number grid for Height domain. Default 15
        _telescope_:    Choose telescope option if your Z domain can't be reached with equidistant Z grid. Default: 5 (growing percentage)
        startTelescopeHeight_: Height where to start the telesscoping Z grid growth. Default: 5.0
        addCellsLeft_: Default: 2
        addCellsUp_: Default: 2
        addCellslRight_: Default: 2
        addCellsDown_: Default: 2
    Returns:
        readMe!: ...
        envimentGrid: Connect this output to "lb_envimet Spaces" in order to add sources to ENVI-Met model.
"""

ghenv.Component.Name = "lb_envimet Grid"
ghenv.Component.NickName = 'lb_envimetGrid'
ghenv.Component.Message = 'VER 0.0.02\nMAR_30_2019'
ghenv.Component.IconDisplayMode = ghenv.Component.IconDisplayMode.application
ghenv.Component.Category = "lb_envimet"
ghenv.Component.SubCategory = "0 | Settings"


import os
import sys
import scriptcontext as sc
import Grasshopper.Kernel as gh
import Rhino as rc
##################LB ENVI_MET###################
userPath = os.getenv("APPDATA")
path = os.path.join(userPath, "lb_envimet")
sys.path.append(path)
from Geometry import Grid
################################################

def main():
    
    envimentGrid = Grid()
    
    if _telescope_:
        envimentGrid.telescope = _telescope_
        if _telescope_ >= 20.0:
            w = gh.GH_RuntimeMessageLevel.Warning
            message = "max telescope factor is 20."
            ghenv.Component.AddRuntimeMessage(w, message)
            envimentGrid.telescope = 20.0
    if _baseSurface_:
        envimentGrid.baseSurface = _baseSurface_
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
        envimentGrid.numZ = numCellsZ_
    
    return envimentGrid


result = main()
if result != -1:
    envimentGrid = result