# ENVI-Met Building
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
Use this component to generate inputs for "LB ENVI-Met Spaces".
-
Sometimes some buildings are not generated when you connect terrain input. Try to move buildings or move the terrain to solve this issue.
-
Provided by Ladybug 0.0.65
    
    Args:
        _buildings: Geometry that represent ENVI-Met buildings.
        -
        Geometry must be closed Brep/Breps.
        _wallMaterial_: Use this input to change wall materials.
        _roofMaterial_: Use this input to change roof materials.
        commonWallMaterial_: Default wall property. Use this input to set default building materials.
        -
        If no input is connected this input will be concrete slab '00'.
        commonRoofMaterial_: Default roof property. Use this input to set default building materials.
        -
        If no input is connected this input will be concrete slab '00'.
    Returns:
        readMe!: ...
        envimetBuildings: Connect this output to "ENVI-Met Spaces" in order to add buildings to ENVI-Met model.
"""

ghenv.Component.Name = "Ladybug_ENVI-Met Building"
ghenv.Component.NickName = 'ENVI-MetBuilding'
ghenv.Component.Message = 'VER 0.0.65\nJUL_28_2017'
ghenv.Component.IconDisplayMode = ghenv.Component.IconDisplayMode.application
ghenv.Component.Category = "Ladybug"
ghenv.Component.SubCategory = "7 | WIP"
#compatibleLBVersion = VER 0.0.59\nFEB_01_2015
try: ghenv.Component.AdditionalHelpFromDocStrings = "1"
except: pass


import os
import sys
import Rhino as rc
import scriptcontext as sc
import Grasshopper.Kernel as gh
##################LB ENVI_MET###################
userPath = os.getenv("APPDATA")
path = os.path.join(userPath, "lb_envimet")
sys.path.append(path)
from envimetObj import material, geometry
################################################


def checkGeometry(geoList):
    for geo in geoList:
        if type(geo) != type(rc.Geometry.Brep()) or not geo.IsSolid:
            w = gh.GH_RuntimeMessageLevel.Warning
            message = "Please provide valid closed breps."
            ghenv.Component.AddRuntimeMessage(w, message)
            return -1


def main():
    if _buildings:
        
        # default materials
        if commonWallMaterial_: commonWallMaterial = commonWallMaterial_
        else: commonWallMaterial = '00'
        if commonRoofMaterial_: commonRoofMaterial = commonRoofMaterial_
        else: commonRoofMaterial = '00'
        
        breps = geometry.buildingGeometry(_buildings)
        #buildings = breps.fromBrepToMesh() # meshes are faster than breps but not accurate! :P
        
        materials = material.SetMaterials.createMaterialListForBuildings(_wallMaterial_, _roofMaterial_, _buildings, commonWallMaterial, commonRoofMaterial)
        envObj = material.SetMaterials(_buildings, materials, [commonWallMaterial, commonRoofMaterial], 0, 'Building')
        
        return envObj
    
    else:
        w = gh.GH_RuntimeMessageLevel.Warning
        message = "Please provide _buildings."
        ghenv.Component.AddRuntimeMessage(w, message)
        return -1


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
        envimetBuildings = result