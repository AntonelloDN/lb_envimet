# ENVI-Met Soil
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
Use this component to generate ENVI-Met inputs for "LB ENVI-Met Spaces".
-
Provided by Ladybug 0.0.64
    
    Args:
        _soil: Geometry that represent ENVI-Met soil.  Geometry must be a Surface or Brep on xy plane.
        _soilId_: ENVI-Met profile id. You can use "id outputs" which comes from "LB ENVI-Met Read Library".
        -
        E.g. L0
        baseSoilmaterial_: Connect a profileId that you want to use as base material of soil. If no id is provided it will be 'LO'.
    Returns:
        readMe!: ...
        envimetSoils: Connect this output to "ENVI-Met Spaces" in order to add soils to ENVI-Met model.
"""

ghenv.Component.Name = "Ladybug_ENVI-Met Soil"
ghenv.Component.NickName = 'ENVI-MetSoil'
ghenv.Component.Message = 'VER 0.0.64\nFEB_26_2017'
ghenv.Component.IconDisplayMode = ghenv.Component.IconDisplayMode.application
ghenv.Component.Category = "Ladybug"
ghenv.Component.SubCategory = "7 | WIP"
#compatibleLBVersion = VER 0.0.62\nJUN_07_2016
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
from envimetObj import material, grid
################################################


def checkGeometry(geoList):
    for geo in geoList:
        if type(geo) != type(rc.Geometry.Brep()):
            w = gh.GH_RuntimeMessageLevel.Warning
            message = "Please provide valid breps."
            ghenv.Component.AddRuntimeMessage(w, message)
            return -1


def main():
    if _soil:
        checkGeometry(_soil)
        
        if baseSoilmaterial_: baseSoilmaterial = baseSoilmaterial_
        else: baseSoilmaterial = 'LO'
        
        # run envimet core
        envObj = material.SetMaterials(_soil, _soilId_, 'LO', 0, 'Soil', baseSoilmaterial)
        
        return envObj
        
    else:
        w = gh.GH_RuntimeMessageLevel.Warning
        message = "Please provide _soil."
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
        envimetSoils = result
