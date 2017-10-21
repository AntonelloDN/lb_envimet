# ENVI-Met Write User Materials
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
Use this component to create User Materials.
-
Provided by Ladybug 0.0.64
    
    Args:
        _envimetFolder: Envimet project folder. I comes from ENVI-MetManageWorkspace.
        _userMaterials: Materials you want to add to your model.
        _runIt: Set to "True" to run the component and generate the envimet model.
    Returns:
        readMe!: ...
"""

ghenv.Component.Name = "Ladybug_ENVI-Met Write User Materials"
ghenv.Component.NickName = 'ENVI-Met WriteUserMaterials'
ghenv.Component.Message = 'VER 0.0.64\nFEB_26_2017'
ghenv.Component.IconDisplayMode = ghenv.Component.IconDisplayMode.application
ghenv.Component.Category = "Ladybug"
ghenv.Component.SubCategory = "7 | WIP"
#compatibleLBVersion = VER 0.0.62\nJUN_07_2016
try: ghenv.Component.AdditionalHelpFromDocStrings = "1"
except: pass


import Grasshopper.Kernel as gh
import sys
import os
##################LB ENVI_MET###################
userPath = os.getenv("APPDATA")
path = os.path.join(userPath, "lb_envimet")
sys.path.append(path)
from envimetStuff import writeMaterial
################################################


def main():
    
    if _envimetFolder and _userMaterials:
        if _runIt:
            # run envimet core
            myFile = writeMaterial.writeMaterials(_userMaterials, _envimetFolder + '//' + 'projectdatabase.edb')
            print("Materials written successfully!")
        else:
            print("Set runIt to True.")
    else:
        w = gh.GH_RuntimeMessageLevel.Warning
        message = "Please provide _envimetFolder and _userMaterials."
        ghenv.Component.AddRuntimeMessage(w, message)


# run component
result = main()
if result != -1:
    envimetFolder = result