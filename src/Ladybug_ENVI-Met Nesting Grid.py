# ENVI-Met Nesting Grid
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
Use this component to set ENVI-Met nesting grid for "LB ENVI-Met Spaces".
-
Provided by Ladybug 0.0.65
    
    Args:
        numNestingGrid_: Connect an integer to set how many nesting cells to use for calculation. Default value is 3.
        soilProfileA_: Connect a profileId that you want to use as first material of nesting grid. If no id is provided it will be 'LO'.
        soilProfileB_: Connect a profileId that you want to use as second material of nesting grid. If no id is provided it will be 'LO'.
    Returns:
        readMe!: ...
        nestingGrid: Connect this output to "ENVI-Met Spaces" in order to add sources to ENVI-Met model.
"""

ghenv.Component.Name = "Ladybug_ENVI-Met Nesting Grid"
ghenv.Component.NickName = 'ENVI-MetNestingGrid'
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
from envimetObj import autoGrid
################################################


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
    nestingGrid = autoGrid.NestingGrid()
    if numNestingGrid_: nestingGrid.numNestingGrid = numNestingGrid_
    if soilProfileA_: nestingGrid.soilProfileA = soilProfileA_
    if soilProfileB_: nestingGrid.soilProfileB = soilProfileB_