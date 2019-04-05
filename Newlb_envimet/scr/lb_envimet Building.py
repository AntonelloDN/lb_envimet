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
Use this component to generate inputs for "lb_envimet Spaces".
-
Some components depend on Ladybug Legacy, please install Ladybug Legacy.
-
Provided by lb_envimet
    
    Args:
        _geometry: Geometry that represent ENVI-Met buildings.
        -
        Geometry must be closed Brep or closed Mesh. Merge more than one geometry to create a unique Mesh (Eg. Context).
        _wallMaterial_: Use this input to change wall material.
        _roofMaterial_: Use this input to change roof material.
        greenWallMaterial_: Default wall property. Use this input to set default building material.
        -
        If no input is connected this input will be concrete slab '000000'.
        greenRoofMaterial_: Default roof property. Use this input to set default building material.
        -
        If no input is connected this input will be concrete slab '000000'.
    Returns:
        readMe!: ...
        envimetBuilding: Connect this output to "ENVI-Met Spaces" in order to add buildings to ENVI-Met model.
"""

ghenv.Component.Name = "lb_envimet Building"
ghenv.Component.NickName = 'lb_envimetBuilding'
ghenv.Component.Message = 'VER 0.0.02\nMAR_30_2019'
ghenv.Component.IconDisplayMode = ghenv.Component.IconDisplayMode.application
ghenv.Component.Category = "lb_envimet"
ghenv.Component.SubCategory = "1 | Geometry"

import os
import sys
import scriptcontext as sc
import Grasshopper.Kernel as gh
import Rhino as rc
##################LB ENVI_MET###################
userPath = os.getenv("APPDATA")
path = os.path.join(userPath, "lb_envimet")
sys.path.append(path)
from Geometry import Grid, Building
################################################


def checkGeometry(geo):
    if type(geo) != type(rc.Geometry.Mesh()) or not geo.IsClosed:
        w = gh.GH_RuntimeMessageLevel.Warning
        message = "Please provide valid closed breps."
        ghenv.Component.AddRuntimeMessage(w, message)
        return -1
    return True


def main():
    if _geometry and checkGeometry(_geometry):
        # default materials
        if _wallMaterial_: wallMaterial = _wallMaterial_
        else: wallMaterial = "000000"
        if _roofMaterial_: roofMaterial = _roofMaterial_
        else: roofMaterial = "000000"
        
        bulding = Building(_geometry, wallMaterial, roofMaterial)
        
        if greenWallMaterial_: bulding.greenWallMaterial = greenWallMaterial_
        if greenRoofMaterial_: bulding.greenRoofMaterial = greenRoofMaterial_
        
        return bulding
    
    else:
        w = gh.GH_RuntimeMessageLevel.Warning
        message = "Please provide _buildings."
        ghenv.Component.AddRuntimeMessage(w, message)
        return -1


result = main()
if result != -1:
    envimetBuilding = result