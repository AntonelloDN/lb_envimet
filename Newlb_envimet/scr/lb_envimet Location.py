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
Use this component to generate ENVI-Met location for "lb_envimet Spaces".
-
This components depend on Ladybug Legacy, please install Ladybug Legacy.
-
Provided by lb_envimet
    
    Args:
        _location: The output from the importEPW or constructLocation component.  This is essentially a list of text summarizing a location on the earth.
    Returns:
        readMe!: ...
        envimetLocation: Connect this output to "ENVI-Met Spaces" in order to add sources to ENVI-Met model.
"""

ghenv.Component.Name = "lb_envimet Location"
ghenv.Component.NickName = 'lb_envimetLocation'
ghenv.Component.Message = 'VER 0.0.02\nMAR_30_2019'
ghenv.Component.IconDisplayMode = ghenv.Component.IconDisplayMode.application
ghenv.Component.Category = "lb_envimet"
ghenv.Component.SubCategory = "0 | Settings"


import os
import sys
import scriptcontext as sc
import Grasshopper.Kernel as gh
import Rhino as rc
from copy import deepcopy
##################LB ENVI_MET###################
userPath = os.getenv("APPDATA")
path = os.path.join(userPath, "lb_envimet")
sys.path.append(path)
from Settings import LocationFromLB
################################################

initCheck = False
if sc.sticky.has_key('ladybug_release'):
    initCheck = True
else:
    initCheck = False
    print "You should first let the Ladybug fly..."
    w = gh.GH_RuntimeMessageLevel.Warning
    ghenv.Component.AddRuntimeMessage(w, "You should first let the Ladybug fly...")


if initCheck:
    if _location:
        if _north_ != None: north = _north_
        else: north = 0
        envimetLocation = LocationFromLB(_location, north)