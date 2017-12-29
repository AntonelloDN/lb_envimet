# ENVI-Met Spaces
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
Use this component to generate ENVI-Met v4.0 3D geometry models.
-
Analyze parametric models with ENVI-Met!
-
Save the model in the ENVI_MET Workspace, set the simulation file with ENVI_MET ConfigWizard and run the simulation.
-
It can write files with equidistant grid only. I add telescopic grid soon.
-
Provided by Ladybug 0.0.65
    
    Args:
        _north_: Input a number between 0 and 360 that represents the degrees off from the y-axis to make North.  The default North direction is set to the Y-axis (0 degrees).
        basePoint_: Input a point here to move ENVI-Met grid. If no input is provided it will be origin point.
        _envimetLocation: Location data which comes from "Ladybug_ENVI-Met Location" component.
        --------------------: (...)
        _gridSettings: Grid settings which comes from "Ladybug_ENVI-Met Grid" component.
        nestingGrid_: Connect the output of "Ladybug_ENVI-Met Nesting Grid".
        _baseSurface_: Connect a planar surface if you do not want to use buildings for grid.
        _envimetObjects_: Connect objects of Ladybug_ENVI-Met you need in your model. The objects comes from:
        .
        1) "Ladybug_ENVI-Met Building"
        .
        2) "Ladybug_ENVI-Met Soil"
        .
        3) "Ladybug_ENVI-Met 2D Plant"
        .
        4) "Ladybug_ENVI-Met 3D Plant"
        .
        5) "Ladybug_ENVI-Met Source"
        .
        6) "Ladybug_ENVI-Met Terrain"
        --------------------: (...)
        _folder: The folder into which you would like to write the envimet model. This should be a complete file path to the folder.
        fileName_: The file name that you would like the envimet model to be saved as. Default name is "LBenvimet".
        _runIt: Set to "True" to run the component and generate the envimet model.
    Returns:
        readMe!: ...
        points: Preview of 3D grid of points.
        INXfileAddress: The file path of the inx result file that has been generated on your machine.
"""

ghenv.Component.Name = "Ladybug_ENVI-Met Spaces"
ghenv.Component.NickName = 'ENVI-MetSpaces'
ghenv.Component.Message = 'VER 0.0.65\nJUL_28_2017'
ghenv.Component.IconDisplayMode = ghenv.Component.IconDisplayMode.application
ghenv.Component.Category = "Ladybug"
ghenv.Component.SubCategory = "7 | WIP"
#compatibleLBVersion = VER 0.0.59\nFEB_01_2015
try: ghenv.Component.AdditionalHelpFromDocStrings = "1"
except: pass


import os
import re
import sys
import Rhino as rc
import scriptcontext as sc
import Grasshopper.Kernel as gh
##################LB ENVI_MET###################
userPath = os.getenv("APPDATA")
path = os.path.join(userPath, "lb_envimet")
sys.path.append(path)
from envimetObj import material, autoGrid
from envimetStuff import writeINX
################################################


def createGrid(objects, baseSurface, envimetGrid):
    
    geometry = None
    
    if baseSurface:
        geometry = [baseSurface]
    
    elif not baseSurface and objects:
        for obj in objects:
            if obj.name == "Building":
                buildingObj = obj
                # properties
                properties = buildingObj.makeAttributeTuple
                geometry = [buildingData[0] for buildingData in properties]
            else:
                continue
        if geometry == None:
            w = gh.GH_RuntimeMessageLevel.Warning
            message = "Please provide envimetBuildings if your grid is based on buildings "\
            "or baseSurface if your grid is based on surface"
            ghenv.Component.AddRuntimeMessage(w, message)
            return -1
    else:
        w = gh.GH_RuntimeMessageLevel.Warning
        message = "Please provide envimetBuildings if your grid is based on buildings "\
        "or baseSurface if your grid is based on surface"
        ghenv.Component.AddRuntimeMessage(w, message)
        return -1
    
    envimetGrid.gZmethod(geometry)
    gridPoints = envimetGrid.createGridOnBorders()
    
    return gridPoints


def checkDistanceFromBorder(points, buildings, dimX, dimY):
    
    def messageForUserBorder():
        w = gh.GH_RuntimeMessageLevel.Warning
        message = "There is not enough space between the border and Building n{0}."
        ghenv.Component.AddRuntimeMessage(w, message.format(index))
        return False
    
    ptMin = rc.Geometry.Point3d(min(points).X, min(points).Y, 0)
    ptMax = rc.Geometry.Point3d(max(points).X, max(points).Y, 0)
    border = rc.Geometry.Rectangle3d(rc.Geometry.Plane.WorldXY, ptMin, ptMax).ToNurbsCurve()
    
    # let's check!
    cornerStyle = rc.Geometry.CurveOffsetCornerStyle.Sharp
    firstCheck = rc.Geometry.Rectangle3d(rc.Geometry.Plane.WorldXY, rc.Geometry.Point3d(ptMin.X + dimX, ptMin.Y + dimY, 0), rc.Geometry.Point3d(ptMax.X - dimX, ptMax.Y - dimY, 0)).ToNurbsCurve()
    
    for index, building in enumerate(buildings):
        bbox = building.GetBoundingBox(True).ToBrep()
        xprj = rc.Geometry.Transform.PlanarProjection(rc.Geometry.Plane.WorldXY)
        bbox.Transform(xprj)
        
        for v in bbox.Vertices:
            if firstCheck.Contains(v.Location, rc.Geometry.Plane.WorldXY) == rc.Geometry.PointContainment.Outside:
                return messageForUserBorder()
    return True


def evimetPartsGenerator(objects, envimetGrid, gridPoints):
    
    # create a dict for all envimet objects
    envimet2dMatrix = {}
    
    for obj in objects:
        if obj.name == 'Building':
            # separete properties
            properties = obj.makeAttributeTuple
            buildings = [buildingData[0] for buildingData in properties]
            wallMaterials = [buildingData[1][0] for buildingData in properties]
            roofMaterials = [buildingData[1][1] for buildingData in properties]
            if checkDistanceFromBorder(gridPoints, buildings, envimetGrid.dimX, envimetGrid.dimY):
                # common materials
                envimet2dMatrix['BuildingCommonMaterial'] = obj.defaultMat
                
                # run
                nestedMatrix = envimetGrid.buildingGrid(0, buildings)[1]
                
                # create bottom Building Matrix
                minBuildingMatrix = envimetGrid.HminNestedMatrix(nestedMatrix)
                mergedMinMatrix = envimetGrid.mergeBuildingMatrix(minBuildingMatrix)
                
                # create top Building Matrix
                maxBuildingMatrix = envimetGrid.HmaxNestedMatrix(nestedMatrix)
                mergedMaxMatrix = envimetGrid.mergeBuildingMatrix(maxBuildingMatrix)
                
                bottomBuildingMatrix = envimetGrid.fromPythonToEnvimetMatrix(mergedMinMatrix)
                topBuildingMatrix = envimetGrid.fromPythonToEnvimetMatrix(mergedMaxMatrix)
                
                envimet2dMatrix['BuildingTop2d'] = topBuildingMatrix
                envimet2dMatrix['BuildingBottom2d'] = bottomBuildingMatrix
                
                # detailed and ids
                flagMatrix, nestedMatrix = envimetGrid.buildingGrid(1, buildings)
                mergedMatrix = envimetGrid.createOneMatrixForBuildings(nestedMatrix, buildings)
                
                list3DInfoBuildings = envimetGrid.setMaterials(mergedMatrix, wallMaterials, roofMaterials)[0]
                matrixIds = envimetGrid.index2DMatrix(mergedMatrix)
                
                envimet2dMatrix['BuildingFlag'] = flagMatrix
                envimet2dMatrix['Building3D'] = list3DInfoBuildings
                envimet2dMatrix['BuildingIds'] = matrixIds
                envimet2dMatrix['BuildingEmptyMatrix'] = re.sub('\d+','0',matrixIds)
        
        elif obj.name == 'Terrain':
            terrainMesh = obj.creteBrepTerrain()
            dem3D = envimetGrid.digitalElevationModel3D(terrainMesh)
            dem2D = envimetGrid.digitalElevationModel2D(terrainMesh)
            envimet2dMatrix['Terrain2d'] = dem2D
            envimet2dMatrix['Terrain3d'] = dem3D
        else:
            altMat = obj.baseMat
            tupleProperties = obj.makeAttributeTuple
            if obj.name != 'Plant3d':
                
                nestedMatrix = envimetGrid.create2DMatrixPerObj(tupleProperties)
                mergedMatrix = envimetGrid.mergeMatrix(nestedMatrix, altMat)
                matrix = envimetGrid.fromPythonToEnvimetMatrix(mergedMatrix)
            else:
                matrix = envimetGrid.threeDimensionalPlants(obj.makeAttributeTuple)
                
            envimet2dMatrix[obj.name] = matrix
    
    return envimet2dMatrix

def main():
    
    if _north_ == None:
        north = 0.00
    else: north = _north_
    
    # name of file
    if fileName_ == None:
        fileName = 'LBenvimet.INX'
    else:
        fileName = fileName_ + '.INX'
    
    if not os.path.exists(_envimetFolder):
        os.makedirs(_envimetFolder)
    fileAddress = _envimetFolder + '\\' + fileName
    
    
    numX, numY, dimX, dimY, dimZ  = _envimetGrid.numX + 1, _envimetGrid.numY + 1, _envimetGrid.dimX, _envimetGrid.dimY, _envimetGrid.dimZ
    numZ, verticalStretch, startStretch = _envimetGrid.zGrids, _envimetGrid.telescope, _envimetGrid.startTelescopeHeight
    telescopingGrid = 1 if _envimetGrid.telescope else 0
    
    
    # create grid
    if _envimetObjects_ or _baseSurface_:
        gridPoints = createGrid(_envimetObjects_, _baseSurface_, _envimetGrid)
        
        if _runIt:
            # create parts
            envimetObjDict = evimetPartsGenerator(_envimetObjects_, _envimetGrid, gridPoints)
            # add emptyMatrix
            envimetObjDict['EmptyMatrix'] = _envimetGrid.emptyMatrix()
            # keys
            envimetObjDictKeys = envimetObjDict.keys()
            # default assignments
            terrain3d, buildingFlag, building3D, plant2d, plant3d, source, terrain2d, buildingBottom2d, buildingTop2d, buildingCommonMaterial, soil, buildingEmptyMatrix, buildingIds = '', '', '', envimetObjDict['EmptyMatrix'], '', envimetObjDict['EmptyMatrix'], envimetObjDict['EmptyMatrix'], envimetObjDict['EmptyMatrix'], envimetObjDict['EmptyMatrix'], ['00','00'], re.sub('', 'LO', envimetObjDict['EmptyMatrix']), re.sub('', '0', envimetObjDict['EmptyMatrix']), re.sub('', '0', envimetObjDict['EmptyMatrix'])
            
             
            for key in envimetObjDictKeys:
                if key == 'BuildingCommonMaterial':
                    buildingCommonMaterial = envimetObjDict['BuildingCommonMaterial']
                elif key == 'BuildingEmptyMatrix':
                    buildingEmptyMatrix = envimetObjDict['BuildingEmptyMatrix']
                elif key == 'BuildingIds':
                    buildingIds = envimetObjDict['BuildingIds']
                elif key == 'BuildingBottom2d':
                    buildingBottom2d = envimetObjDict['BuildingBottom2d']
                elif key == 'BuildingTop2d':
                    buildingTop2d = envimetObjDict['BuildingTop2d']
                elif key == 'Terrain3d':
                    terrain3d = envimetObjDict['Terrain3d']
                elif key == 'BuildingFlag':
                    buildingFlag = envimetObjDict['BuildingFlag']
                elif key == 'Building3D':
                    building3D = envimetObjDict['Building3D']
                elif key == 'Plant2d':
                    plant2d = envimetObjDict['Plant2d']
                elif key == 'Plant3d':
                    plant3d = envimetObjDict['Plant3d']
                elif key == 'Soil':
                    soil = envimetObjDict['Soil']
                elif key == 'Source':
                    source = envimetObjDict['Source']
                elif key == 'EmptyMatrix':
                    emptyMatrix = envimetObjDict['EmptyMatrix']
                elif key == 'Terrain2d':
                    terrain2d = envimetObjDict['Terrain2d']
            
            # other args
            isFull3DDesign = 1
            if nestingGrid_:
                numNesting = nestingGrid_.numNestingGrid
                matNesting = [nestingGrid_.soilProfileA, nestingGrid_.soilProfileB]
            else:
                numNesting, matNesting = 3, ['LO', 'LO']
            location = _envimetLocation.locationAttributes
            
            # write file
            writeINX(fileAddress, numX, numY, numZ, dimX, dimY,
                    dimZ, str(numNesting), matNesting, location, north, buildingCommonMaterial,
                    buildingEmptyMatrix , buildingIds, buildingBottom2d, buildingTop2d, terrain3d ,
                    buildingFlag, building3D, plant2d, plant3d, soil, source, emptyMatrix, terrain2d , 
                    isFull3DDesign, verticalStretch, startStretch, telescopingGrid, has3DModel = 1)
            
            INXfileAddress = fileAddress
            
            # open the file
            os.startfile(INXfileAddress)
            
            return gridPoints, INXfileAddress
        
        return gridPoints, None
    
    else:
        w = gh.GH_RuntimeMessageLevel.Warning
        message = "Please provide envimetBuildings if your grid is based on buildings "\
        "or baseSurface if your grid is based on surface"
        ghenv.Component.AddRuntimeMessage(w, message)
        return None, None


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
    if _envimetGrid and _envimetLocation and _envimetFolder:
        result = main()
        if result != -1:
            gridPoints, INXfileAddress = result
    else:
        w = gh.GH_RuntimeMessageLevel.Warning
        message = "Please provide _envimetGrid, _envimetLocation and _envimetFolder."
        ghenv.Component.AddRuntimeMessage(w, message)