# ENVI-Met Soil Material
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
This component let you create user soil materials which are compatible with ENVI-Met.
A soil material is a layer of profile material that ENVI-Met uses as property of the soil geometry.
-
Provided by Ladybug 0.0.64
    
    Args:
        _Id: Database-ID of User Material, just two letters or numbers(e.g. DK).
        _description: Name of User Material (e.g. Dark Concrete Road).
        _versiegelung_: (n/d) Default value is 0.
        _waterContentatSaturation_: Volumetric water content at saturation point [m3(water)/m3(soil)].
        Default value is 0.00 (like default Asphalt Material).
        _waterContentAtFieldCap_: Volumetric water content at field capacity [m3(water)/m3(soil)].
        Default value is 0.00 (like default Asphalt Material).
        _waterContentWiltingPoint_: Volumetric water content at wilting point [m3(water)/m3(soil)].
        Default value is 0.00 (like default Asphalt Material).
        _matrixPotential_: Matrix Potential at water saturation [m].
        Default value is 0.00 (like default Asphalt Material).
        _hidraulicConductivity_: Hydraulic conductivity at water saturation [m/s*10^-6].
        Default value is 0.00 (like default Asphalt Material).
        _volumetricHeatCapacity: Volumetric heat capacity of dry soil [J/(m3K)*10^6].
        _clappConstant_: Clapp & Hornberger Constant b.
        Default value is 0.00 (like default Asphalt Material).
        _heatConductivity: Heat Conductivity of material. Calculated from water content for natural soils [W/mK].
        _naturalsoil_: Type of material ["Natural soil" or "Artificial material"]. Set true for Natural Soil, default value is Artificial Material.
    Returns:
        readMe!: ...
        soilId: ENVI-Met soil ID of User Material.
"""

ghenv.Component.Name = "Ladybug_ENVI-Met Soil Material"
ghenv.Component.NickName = 'ENVI-MetSoilMaterial'
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
from envimetObj import material
################################################

def main():

    if _Id and _description and _volumetricHeatCapacity and _heatConductivity:
        if _versiegelung_: versiegelung = _versiegelung_
        else: versiegelung = '0'
        if _waterContentatSaturation_: waterContentatSaturation = _waterContentatSaturation_
        else: waterContentatSaturation= '0'
        if _waterContentAtFieldCap_: waterContentAtFieldCap = _waterContentAtFieldCap_
        else: waterContentAtFieldCap = '0'
        if _waterContentWiltingPoint_: waterContentWiltingPoint = _waterContentWiltingPoint_
        else: waterContentWiltingPoint = '0'
        if _matrixPotential_: matrixPotential = _matrixPotential_
        else: matrixPotential = '0'
        if _hidraulicConductivity_: hidraulicConductivity = _hidraulicConductivity_
        else: hidraulicConductivity = '0'
        if _clappConstant_: clappConstant = _clappConstant_
        else: clappConstant = '0'
        if _naturalsoil_: naturalsoil = "Natural Soils"
        else: naturalsoil = "Artificial Soils"

        # run envimet core
        envObj = material.createSoilMaterial(_Id, _description, versiegelung, waterContentatSaturation, waterContentAtFieldCap, waterContentWiltingPoint, matrixPotential, hidraulicConductivity, _volumetricHeatCapacity, clappConstant, _heatConductivity, naturalsoil)
    
    else:
        w = gh.GH_RuntimeMessageLevel.Warning
        message = "Please provide all mandatory inputs (_nameInput)."
        ghenv.Component.AddRuntimeMessage(w, message)
        return -1
        
    return envObj, _Id


result = main()
if result != -1:
    userMaterial, soilId = result
