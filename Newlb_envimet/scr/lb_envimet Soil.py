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
Use this component to generate ENVI-Met inputs for "lb_envimet Spaces".
-
Some components depend on Ladybug Legacy, please install Ladybug Legacy.
-
Provided by lb_envimet
    
    Args:
        _soil: Geometry that represent ENVI-Met soil.  Geometry must be a Surface or Brep on xy plane.
        _soilId_: ENVI-Met profile id. You can use "id outputs" which comes from "lb_envimet Read Library".
        -
        E.g. L0
        baseSoilmaterial_: Connect a profileId that you want to use as base material of soil. If no id is provided it will be '000000'.
    Returns:
        readMe!: ...
        envimetSoils: Connect this output to "lb_envimet Spaces" in order to add soils to ENVI-Met model.
"""

ghenv.Component.Name = "lb_envimet Soil"
ghenv.Component.NickName = 'lb_envimetSoil'
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
    if _soil:
        checkGeometry(_soil)
        
        if _soilId_ != None: soilId = _soilId_
        else: soilId = "000000"
        
        # run envimet core
        envObj = Object2d(_soil, soilId, 'Soil')
        
        return envObj
        
    else:
        w = gh.GH_RuntimeMessageLevel.Warning
        message = "Please provide _soil."
        ghenv.Component.AddRuntimeMessage(w, message)
        return -1


result = main()
if result != -1:
    envimetSoil = result
