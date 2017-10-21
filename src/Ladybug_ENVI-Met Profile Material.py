# ENVI-Met Profile Material
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
Use this component to create your own profile material. Note that there are many advanced properties you can set.
-
Provided by Ladybug 0.0.64
    
    Args:
        _Id: Database-ID of User Material, just two letters or numbers(e.g. MP).
        _description: Name of User Material (e.g. My Profile Material).
        _microscaleRoughness: Microscale roughness length of surface [m].
        _albedo: Albedo (reflectivity) for shortwave radiation [Frac].
        _emissivity: Emissivity for longwave thermal radiation [Frac].
        _extraId_: Different purposes. Default value is 0.
        _irrigated_: Is Surface irrigated? True = Yes, False = No.
        Default value is False.
        _groupProfileSoil_: Connect "LB_ENVI-Met Group Profile Soil". Default value is "Road Pavements".
        -----------------------------: (...)
        _layers: from 0cm to 1cm below ground surface. Click on "+" to add a next layer.
    Returns:
        readMe!: ...
        profileId: ENVI-Met soil ID of User Material. Connect it to "Ladybug_ENVI-Met Soil".
"""

ghenv.Component.Name = "Ladybug_ENVI-Met Profile Material"
ghenv.Component.NickName = 'ENVI-MetProfileMaterial'
ghenv.Component.Message = 'VER 0.0.64\nFEB_26_2017'
ghenv.Component.IconDisplayMode = ghenv.Component.IconDisplayMode.application
ghenv.Component.Category = "Ladybug"
ghenv.Component.SubCategory = "7 | WIP"
#compatibleLBVersion = VER 0.0.62\nJUN_07_2016
try: ghenv.Component.AdditionalHelpFromDocStrings = "1"
except: pass

import clr
clr.AddReference("Grasshopper")
import Grasshopper.Kernel as gh
from Grasshopper.Kernel.Data import GH_Path


import os
import sys
import Rhino as rc
import scriptcontext as sc
import Grasshopper.Kernel as gh
##################LB ENVI_MET###################
userPath = os.getenv("APPDATA")
path = os.path.join(userPath, "lb_envimet")
sys.path.append(path)
from envimetObj import material
################################################

def main():

    if _Id and _description and _microscaleRoughness and _albedo and _emissivity and _layers:
        if _extraId_: extraId = _extraId_
        else: extraId = '0'
        if _groupProfileSoil_: groupProfileSoil = _groupProfileSoil_
        else: groupProfileSoil = 'RoadsPavements'
        if _irrigated_ == True:
            irrigated = '1'
        else:
            irrigated = '0'
        
        # layers
        stringLayers = ','.join([element for element in _layers])
        print(stringLayers)
        
        # run envimet core
        envObj = material.createProfileMaterial(_Id, _description, _microscaleRoughness, stringLayers, _albedo, _emissivity, extraId, irrigated, groupProfileSoil)
    
    else:
        w = gh.GH_RuntimeMessageLevel.Warning
        message = "Please provide all mandatory inputs (_nameInput)."
        ghenv.Component.AddRuntimeMessage(w, message)
        return -1
        
    return envObj, _Id


result = main()
if result != -1:
    userMaterial, profileId = result