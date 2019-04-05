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
This component let you select materials from ENVI-Met library.
-
    Args:
        _dataType: Connect an integer from 0 to 8.
        -
        0 = soil
        1 = profile
        2 = material
        3 = wall
        4 = source
        5 = plant
        6 = plant3D
        7 = greening
        8 = simpleWall
        -
        Default value is 0.
        _keyword_: Connect a keyword to filter data. E.g. 'asphalt' (_dataType = 0)
    Returns:
        readMe!: ...
        soilId: ENVI-Met soil ID.
        soilData:
        0 = Id
        1 = Description
        2 = Versiegelung
        3 = Water Contentat Saturation
        4 = Water Content At Field Cap
        5 = WaterContentWiltingPoint
        6 = Matrix Potential
        7 = Hidraulic Conductivity
        8 = Volumetric HeatCapacity
        9 = Clapp Constant
        10 = Heat Conductivity
        11 = Group
        12 = Color
"""

ghenv.Component.Name = "lb_envimet Read Library"
ghenv.Component.NickName = 'lb_envimetReadLibrary'
ghenv.Component.Message = 'VER 0.0.02\nMAR_30_2019'
ghenv.Component.IconDisplayMode = ghenv.Component.IconDisplayMode.application
ghenv.Component.Category = "lb_envimet"
ghenv.Component.SubCategory = "0 | Settings"


import os
import re
import clr
import sys
clr.AddReference("Grasshopper")
clr.AddReference("System.Xml")
import System.Xml
import scriptcontext as sc
import Grasshopper.Kernel as gh
from Grasshopper.Kernel.Data import GH_Path
from Grasshopper import DataTree
##################LB ENVI_MET###################
userPath = os.getenv("APPDATA")
path = os.path.join(userPath, "lb_envimet")
sys.path.append(path)
from IO import ReadEnvimetLib
################################################


outputId = ['soil', 'profile', 'material', 'wall', 'source', 'plant', 'plant3D', 'greening', 'simpleWall']

outputsDict = {
0: ["readMe!", "..."],
1: ["soilId", "ENVI-Met soil ID."],
2: ["soilData", "0 = Id\n1 = Description\n2 = Versiegelung\n3 = Water Contentat Saturation\n4 = Water Content At Field Cap\n5 = WaterContentWiltingPoint" + \
"6 = Matrix Potential\n7 = Hidraulic Conductivity\n8 = Volumetric HeatCapacity\n9 = Clapp Constant\n10 = Heat Conductivity\n11 = Group\n12 = Color"]
}

otherFolderDict = {
'0': "0 = Id\n1 = Description\n2 = Versiegelung\n3 = Water Contentat Saturation\n4 = Water Content At Field Cap\n5 = WaterContent Wilting Point\n" + \
"6 = Matrix Potential\n7 = Hidraulic Conductivity\n8 = Volumetric HeatCapacity\n9 = Clapp Constant\n10 = Heat Conductivity\n11 = Group\n12 = Color",
'1': "0 = Id\n1 = Description\n2 = Microscale roughness length of surface(m)\n3 = soil profile\n4 = Albedo\n5 = Emissivity\n6 = ExtraID\n7 = Irrigated\n8 = Color\n9 = Group",
'2': "0 = Id\n1 = Description\n2 = Thickness\n3 = Absorption\n4 = Transmission\n5 = Reflection\n6 = Emissivity\n7 = SpecificHeat\n8 = Thermal Conductivity\n9 = Density\n10 = ExtraID\n11 = Color\n12 = Group",
'3': "0 = Id\n1 = Description\n2 = Materials\n3 = Thickness Layers(m)\n4 = TypeID\n5 = Color\n6 = Group",
'4': "0 = Id\n1 = Description\n2 = Color\n3 = Group\n4 = DefaultHeight\n5 = Source type\n6 = Special ID\n",
'5': "0 = Id\n1 = Description\n2 = Alternative Name\n3 = Plant type\n4 = Leaf type\n5 = Albedo\n6 = rs_min\n7 = Height\n8 = Root Zone Depth",
'6': "0 = Id and Description\n1 = Alternative Name\n2 = Plant type\n3 = Leaf type\n4 = Albedo\n5 = isoprene\n6 = leaf weigth\n7 = rs_min\n8 = Height\n" + \
"9 = Width\n10 = Depth\n11 = RootDiameter",
'7': "0 = Id\n1 = Name\n2 = Materials\n3 = HasSubstrate\n4 = SoilID\n5 = ThicknessLayers\n6 = subEmissivity\n7 = subAlbedo\n8 = subWaterCoeff\n9 = SimplePlantID\n10 = LAI\n11 = SimplePlantThickness\n12 = LeafAngleDistribution\n13 = AirGap\n15 = Color\n16 = Group\n17 = AddValue1\n18 = AddValue2",
'8': "0 = Id\n1 = Name\n2 = Materials\n3 = RoughnessLength\n4 = Thickness\n5 = Color\n6 = Group"
}


def setComponentOutputs(index):
    for output in range(3):
        if output == 0: 
            ghenv.Component.Params.Output[output].NickName = outputsDict[output][0]
            ghenv.Component.Params.Output[output].Name = outputsDict[output][0]
            ghenv.Component.Params.Output[output].Description = outputsDict[output][1]
        elif output == 1:
            ghenv.Component.Params.Output[output].NickName = outputId[index]+'Id'
            ghenv.Component.Params.Output[output].Name = outputId[index]+'Id'
            ghenv.Component.Params.Output[output].Description = "ENVI-Met {} ID.".format(outputId[index])
        elif output == 2:
            ghenv.Component.Params.Output[output].NickName = outputId[index]+'Data'
            ghenv.Component.Params.Output[output].Name = outputId[index]+'Data'
            ghenv.Component.Params.Output[output].Description = otherFolderDict[str(index)]


def restoreComponentOutputs():
    for output in range(3):
        ghenv.Component.Params.Output[output].NickName = outputsDict[output][0]
        ghenv.Component.Params.Output[output].Name = outputsDict[output][0]
        ghenv.Component.Params.Output[output].Description = outputsDict[output][1]


def makeFolder(subFolder):
    # make a folder
    subFolder = subFolder + '\\'
    appdata = os.getenv("APPDATA")
    try:
        directory = os.path.join(appdata, "Ladybug\ENVIbug", subFolder)
        if not os.path.exists(directory):
            os.makedirs(directory)
    except:
        directory = os.path.join(appdata[:3], "Ladybug\ENVIbug", subFolder)
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    return directory


def ENVIGeometryParser():
    
    def findValue(inputList):
        
        outList = []
        outTree = DataTree[System.Object]()
        
        # mod keyworld
        if _keyword_:
            if _keyword_.isupper() or _keyword_.islower():
                keyword = _keyword_.capitalize()
            else:
                keyword = _keyword_
            
            # id
            for i, data in enumerate(inputList):
                for word in data:
                    if keyword in word:
                        outList.append(data[0])
                        path = GH_Path(i)
                        outTree.AddRange(data, path)
            
        else:
            for i, data in enumerate(inputList):
                outList.append(data[0])
                path = GH_Path(i)
                outTree.AddRange(data, path)
                
        return outList, outTree
    
    
    def findINX():
        appdata = os.getenv("APPDATA")
        directory = os.path.join(appdata[:3], "ENVImet4\sys.basedata\\")
        try:
            if 'database.edb' in os.listdir(directory):
                path = os.path.join(directory, 'database.edb')
                return path
        except:
            w = gh.GH_RuntimeMessageLevel.Warning
            message = "Envimet DataBase not found!."
            ghenv.Component.AddRuntimeMessage(w, message)
            return -1  
    
    
    # path and default folder
    path = findINX()
    folder = makeFolder('DataBase')
    
    # run envimet core
    myFile = ReadEnvimetLib(path)
    soilList, profileList, materialList, wallList, sourceList, plantList, plant3DList, greeningList, simpleWallList = myFile.readLibrary(folder)
    
    
    # plants3D
    plant3DListMod = []
    for innerList in plant3DList:
        plant3DinnerList = []
        for i, element in enumerate(innerList[:12]):
            if i < 1:
                plant3DinnerList.append(element + ',.' + innerList[:12][1])
            else:
                plant3DinnerList.append(element)
        plant3DListMod.append(plant3DinnerList)
    
    
    # run
    soilId, soilData = findValue(soilList)
    profileId, profileData = findValue(profileList)
    materialId, materialData = findValue(materialList)
    wallId, wallData = findValue(wallList)
    sourceId, sourceData = findValue(sourceList)
    plantId, plantData = findValue(plantList)
    plant3DId, plant3DData = findValue(plant3DListMod)
    greeningId, greeningData = findValue(greeningList)
    simpleWallId, simpleWallData = findValue(simpleWallList)
    
    
    return soilId, soilData, profileId, profileData, materialId, materialData, wallId, wallData, sourceId, sourceData, plantId, plantData, plant3DId, plant3DData, greeningId, greeningData, simpleWallId, simpleWallData# metti tutti i possibili output qui


if _dataType > 0: setComponentOutputs(_dataType)
else: restoreComponentOutputs()

soilId, soilData, profileId, profileData, materialId, materialData, wallId, wallData, sourceId, sourceData, plantId, plantData, plant3DId, plant3DData, greeningId, greeningData, simpleWallId, simpleWallData = ENVIGeometryParser()