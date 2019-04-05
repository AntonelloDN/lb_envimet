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
Use this component to generate ENVI-Met plants for "lb_envimet Spaces".
-
Some components depend on Ladybug Legacy, please install Ladybug Legacy.
-
Provided by lb_envimet
    
    Args:
        _plant2D: Geometry that represent ENVI-Met plant 2d.  Geometry must be a Surface or Brep on xy plane.
        _plantId_: ENVI-Met plant id. You can use "id outputs" which comes from "lb_envimet Read Library".
        -
        E.g. 0000XX
    Returns:
        readMe!: ...
        envimetPlant: Connect this output to "lb_envimet Spaces" in order to add plants to ENVI-Met model.
"""

ghenv.Component.Name = "lb_envimet 2D Plant"
ghenv.Component.NickName = 'lb_envimetPlant'
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
from Geometry import Object2d
################################################


def checkGeometry(geo):
    if type(geo) != type(rc.Geometry.Mesh()):
        w = gh.GH_RuntimeMessageLevel.Warning
        message = "Please provide valid breps."
        ghenv.Component.AddRuntimeMessage(w, message)
        return -1


def main():
    if _plant2D:
        checkGeometry(_plant2D)
        
        if _plantId_ != None:
            plantId = _plantId_
        else:
            plantId = "0000XX"
        
        # run envimet core
        envObj = Object2d(_plant2D, plantId, 'Plant2d')
        
        return envObj
        
    else:
        w = gh.GH_RuntimeMessageLevel.Warning
        message = "Please provide _plant2D."
        ghenv.Component.AddRuntimeMessage(w, message)
        return -1


result = main()
if result != -1:
    envimetPlant = result