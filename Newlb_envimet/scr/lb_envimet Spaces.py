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
Use this component to generate ENVI-Met v4 3D geometry models.
-
Some components depend on Ladybug Legacy, please install Ladybug Legacy.
-
Provided by lb_envimet
    
    Args:
        _envimetFolder: Workspace folder which comes from lb_envimet ManageWorkspace"
        _envimetLocation: Location data which comes from "lb_envimet Location" component.
        --------------------: (...)
        _envimetGrid: Grid settings which comes from "lb_envimet Grid" component.
        nestingGrid_: Connect the output of "lb_envimet Nesting Grid".
        _envimetObjects_: Connect objects of lb_envimet you need in your model. The objects comes from:
        .
        1) "lb_envimet Building"
        .
        2) "lb_envimet Soil"
        .
        3) "lb_envimet 2D Plant"
        .
        4) "lb_envimet 3D Plant"
        .
        5) "lb_envimet Source"
        .
        6) "lb_envimet Terrain"
        --------------------: (...)
        fileName_: The file name that you would like the envimet model to be saved as. Default name is "LBenvimet".
        _runIt: Set to "True" to run the component and generate the envimet model.
        viewGridXY_: Set to "True" to view grid XY.
        viewGridXZ_: Set to "True" to view grid XZ.
        viewGridYZ_: Set to "True" to view grid YZ.
    Returns:
        readMe!: ...
        XYGrid: Preview of grid XY.
        XZGrid: Preview of 3D grid XZ.
        YZGrid: Preview of 3D grid YZ.
        INXfileAddress: The file path of the inx result file that has been generated on your machine.
"""

ghenv.Component.Name = "lb_envimet Spaces"
ghenv.Component.NickName = 'lb_envimetSpaces'
ghenv.Component.Message = 'VER 0.0.02\nMAR_30_2019'
ghenv.Component.IconDisplayMode = ghenv.Component.IconDisplayMode.application
ghenv.Component.Category = "lb_envimet"
ghenv.Component.SubCategory = "2 | Simulation"


import os
import re
import sys
import scriptcontext as sc
import Grasshopper.Kernel as gh
import Rhino as rc
from copy import deepcopy
##################LB ENVI_MET###################
userPath = os.getenv("APPDATA")
path = os.path.join(userPath, "lb_envimet")
sys.path.append(path)
from Geometry import Grid, Building, Dem, Object2d, NestingGrid, SingleWall
from IO.writeINX import *
################################################


def separateObjects(objects):
    
    buildings, terrain, plant3d, plant2d, soils, sources, singleWall  = [], None, [], [], [], [], []
    
    for obj in objects:
        if obj.__class__ is Building:
            buildings.append(obj)
        elif obj.__class__ is Dem:
            terrain = obj
        elif obj.__class__ is Plant3d:
            plant3d.append(obj)
        elif obj.__class__ is SingleWall:
            singleWall.append(obj)
        elif obj.name == 'Plant2d':
            plant2d.append(obj)
        elif obj.name == 'Soil':
            soils.append(obj)
        elif obj.name == 'Source':
            sources.append(obj)

    
    return buildings, terrain, plant3d, plant2d, soils, sources, singleWall


def createGrid(buildings, grid):
    
    baseObject = []
    
    if not grid.baseSurface:
        baseObject = [building.geometry for building in buildings]
    else:
        baseObject = [grid.baseSurface]
    
    if baseObject:
        grid.gZmethod(baseObject)
        gridXY = grid.gridPreviewXY()
        
        return gridXY
    else:
        w = gh.GH_RuntimeMessageLevel.Warning
        message = "Please provide envimetBuildings if your grid is based on buildings "\
        "or baseSurface if your grid is based on surface"
        ghenv.Component.AddRuntimeMessage(w, message)
        return -1


def checkDistanceFromBorder(points, buildings, grid):
    
    planeWorldXY = rc.Geometry.Plane.WorldXY
    
    ptMin = rc.Geometry.Point3d(min(points).X, min(points).Y, 0)
    ptMax = rc.Geometry.Point3d(max(points).X, max(points).Y, 0)
    border = rc.Geometry.Rectangle3d(planeWorldXY, ptMin, ptMax).ToNurbsCurve()
    
    # let's check!
    cornerStyle = rc.Geometry.CurveOffsetCornerStyle.Sharp
    firstCorner = rc.Geometry.Point3d(ptMin.X + grid.dimX, ptMin.Y + grid.dimY, 0)
    secondCorner = rc.Geometry.Point3d(ptMax.X - grid.dimX, ptMax.Y - grid.dimY, 0)
    firstCheck = rc.Geometry.Rectangle3d(planeWorldXY, firstCorner, secondCorner).ToNurbsCurve()
    
    geometry = [building.geometry for building in buildings]
    
    for index, building in enumerate(geometry):
        bbox = building.GetBoundingBox(True).ToBrep()
        xprj = rc.Geometry.Transform.PlanarProjection(planeWorldXY)
        bbox.Transform(xprj)
        
        for v in bbox.Vertices:
            if firstCheck.Contains(v.Location, planeWorldXY) == rc.Geometry.PointContainment.Outside:
                w = gh.GH_RuntimeMessageLevel.Warning
                message = "There is not enough space between the border and Building n°{0}."
                ghenv.Component.AddRuntimeMessage(w, message.format(index))
                return -1


def main():
    
    XYGrid, XZGrid, YZGrid, INXfileAddress = None, None, None, None
    
    # default materials
    if defaultSoilMaterial_ == None:
        defaultSoilMaterial = '000000'
    else:
        defaultSoilMaterial = defaultSoilMaterial_
    
    if defaultBuildingMaterial_ == None:
        buildingCommonMaterial = ['000000'] * 2
    else:
        buildingCommonMaterial = [defaultBuildingMaterial_] * 2
    
    # name of file
    if fileName_ == None:
        fileName = 'LBenvimet.INX'
    else:
        fileName = fileName_ + '.INX'
    
    if not os.path.exists(_envimetFolder):
        os.makedirs(_envimetFolder)
    fileAddress = _envimetFolder + '\\' + fileName
    
    if nestingGrid_:
        nesting = nestingGrid_
    else:
        nesting = NestingGrid()
    
    location = _envimetLocation.locationAttributes
    
    # separate objects
    try:
        buildings, terrain, plant3ds, plant2ds, soils, sources, singleWall = separateObjects(_envimetObjects_)
    except AttributeError:
        w = gh.GH_RuntimeMessageLevel.Warning
        message = "An input is missing. Please check it."
        ghenv.Component.AddRuntimeMessage(w, message)
        return -1
    
    if buildings or _envimetGrid:
        gridXY = createGrid(buildings, _envimetGrid)
        
        if viewGridXY_:
            XYGrid = _envimetGrid.gridPreviewXY()
        if viewGridXZ_:
            XZGrid = _envimetGrid.gridPreviewXZ()
        if viewGridYZ_:
            YZGrid = _envimetGrid.gridPreviewYZ()
    if _runIt:
            # preparation
            plant2d, source = _envimetGrid.emptyMatrix, _envimetGrid.emptyMatrix
            soil = re.sub('', defaultSoilMaterial, _envimetGrid.emptyMatrix)
            plant3d, shadings = '', ''
            
            # terrain
            demVoxel, demDBMatrix, dem2d = getDemMatrix(_envimetGrid, terrain)
            
            # buildings
            zeroMatrix = re.sub('', '0', _envimetGrid.emptyMatrix)
            IdMatrix, bottomMatrix, topMatrix = zeroMatrix, zeroMatrix, zeroMatrix
            wallDBMatrix, buildingNumberMatrix, greenIds, greenDBMatrix = '', '', '', ''
            
            buildingMatrix = [_envimetGrid.emptyMatrix , IdMatrix, bottomMatrix, topMatrix, buildingNumberMatrix, wallDBMatrix, greenIds, greenDBMatrix]
            
            if buildings:
                checkDistanceFromBorder(gridXY, buildings, _envimetGrid)
                IdMatrix, bottomMatrix, topMatrix, buildingNumberMatrix, wallDBMatrix, greenIds, greenDBMatrix = getBuildingPreparationMatrix(_envimetGrid, buildings, terrain, demVoxel)
                
                buildingMatrix = [_envimetGrid.emptyMatrix , IdMatrix, bottomMatrix, topMatrix, buildingNumberMatrix, wallDBMatrix, greenIds, greenDBMatrix]
            
            # other
            if plant3ds:
                plant3d = treeObjectMatrix(_envimetGrid, plant3ds)
            if plant2ds:
                plant2d = get2dObjectMatrix(_envimetGrid, plant2ds, '')
            if soils:
                soil = get2dObjectMatrix(_envimetGrid, soils, defaultSoilMaterial)
            if sources:
                source = get2dObjectMatrix(_envimetGrid, sources, '')
            if singleWall:
                shadings = getSimpleWall(_envimetGrid, singleWall)
            
            writeINX(fileAddress, _envimetGrid, _envimetLocation.locationAttributes, nesting, buildingMatrix, buildingCommonMaterial, dem2d, demDBMatrix, plant2d, plant3d, soil, source, shadings)
            INXfileAddress = fileAddress
        
    return XYGrid, XZGrid, YZGrid, INXfileAddress


if _envimetGrid and _envimetLocation and _envimetFolder:
    result = main()
    if result != -1:
        XYGrid, XZGrid, YZGrid, INXfileAddress = result
else:
    w = gh.GH_RuntimeMessageLevel.Warning
    message = "Please provide _envimetGrid, _envimetLocation and _envimetFolder."
    ghenv.Component.AddRuntimeMessage(w, message)