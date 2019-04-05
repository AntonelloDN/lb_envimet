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
Use this component to set ENVI-Met nesting grid for "lb_envimet Spaces".
-
Some components depend on Ladybug Legacy, please install Ladybug Legacy.
-
Provided by lb_envimet
    
    Args:
        numNestingGrid_: Connect an integer to set how many nesting cells to use for calculation. Default value is 3.
        soilProfileA_: Connect a profileId that you want to use as first material of nesting grid. If no id is provided it will be 'LO'.
        soilProfileB_: Connect a profileId that you want to use as second material of nesting grid. If no id is provided it will be 'LO'.
    Returns:
        readMe!: ...
        nestingGrid: Connect this output to "lb_envimet Spaces" in order to add sources to ENVI-Met model.
"""

ghenv.Component.Name = "lb_envimet Nesting Grid"
ghenv.Component.NickName = 'lb_envimetNestingGrid'
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
from Geometry import NestingGrid
################################################

nestingGrid = NestingGrid()
if numNestingGrid_: nestingGrid.numNestingGrid = numNestingGrid_
if soilProfileA_: nestingGrid.soilProfileA = soilProfileA_
if soilProfileB_: nestingGrid.soilProfileB = soilProfileB_