# ENVI-Met Building Cutter
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
Use this component to generate inputs for "LB ENVI-Met Spaces".
-
Sometimes some buildings are not generated when you connect terrain input. Try to move buildings or move the terrain to solve this issue.
-
Provided by Ladybug 0.0.64
    
    Args:
        _buildings: Geometry that represent ENVI-Met buildings.
        -
        Geometry must be closed Brep/Breps.
        -
        Try to connect "threeDeeShapes" output of "Gismo" (a plugin for GIS environmental analysis).
        _terrain: Provide surface which comes from "LB Terrain Generator" or connect a valid surface.
        _runIt: Set to "True" to run the component and generate envimetBuildings and envimetTerrain.
    Returns:
        readMe!: ...
        buildings: Connect this output to "Ladybug_ENVI-Met Building".
"""

ghenv.Component.Name = "Ladybug_ENVI-Met Building Cutter"
ghenv.Component.NickName = 'ENVI-MetBuildingCutter'
ghenv.Component.Message = 'VER 0.0.64\nFEB_26_2017'
ghenv.Component.IconDisplayMode = ghenv.Component.IconDisplayMode.application
ghenv.Component.Category = "Ladybug"
ghenv.Component.SubCategory = "7 | WIP"
#compatibleLBVersion = VER 0.0.62\nJUN_07_2016
try: ghenv.Component.AdditionalHelpFromDocStrings = "1"
except: pass


import Rhino as rc
import scriptcontext as sc
import Grasshopper.Kernel as gh


def checkTerrain(terrain):
    bbox = terrain.GetBoundingBox(terrain)
    if bbox.Min.Z <= 0:
        return False
    else: return True


def creteBrepTerrain(terrain):
    terrainToPrj = rc.Geometry.Brep.Duplicate(terrain)
    prj = rc.Geometry.Transform.PlanarProjection(rc.Geometry.Plane.WorldXY)
    terrainToPrj.Transform(prj)
    
    # create 'solid'
    borderCrvUp = [crv for crv in terrain.DuplicateEdgeCurves()]
    borderCrvDown = [crv for crv in terrainToPrj.DuplicateEdgeCurves()]
    borderCrvUp = rc.Geometry.Curve.JoinCurves(borderCrvUp)[0]
    borderCrvDown = rc.Geometry.Curve.JoinCurves(borderCrvDown)[0]
    
    terrainBrep = rc.Geometry.Brep.CreateFromLoft([borderCrvUp, borderCrvDown], rc.Geometry.Point3d.Unset, rc.Geometry.Point3d.Unset, rc.Geometry.LoftType.Straight, False)
    terrainBrep = rc.Geometry.Brep.JoinBreps([terrain, terrainBrep[0], terrainToPrj], sc.doc.ModelAbsoluteTolerance)[0]
    
    if terrainBrep.IsSolid:
        return terrainBrep
    else: return None


def moveAndCutBuilding(buildings, terrain):
    
    # this happens because of LB terrain output
    def reverseTerrainU(terrain):
        if terrain.Faces[0].Domain(0)[0] == 0.0:
            terrainR = terrain.Faces[0].Reverse(0, True).ToBrep()
        else:
            terrainR = terrain
        return terrainR
    
    terrainR = reverseTerrainU(terrain)
    
    # trim buildings
    trimmedBuildings = []
    for i, building in enumerate(buildings):
        points = []
        bbox = building.GetBoundingBox(True)
        corners = bbox.GetCorners()
        point = rc.Geometry.Intersect.Intersection.ProjectPointsToBreps([terrain], corners, rc.Geometry.Vector3d.ZAxis, sc.doc.ModelAbsoluteTolerance)
        points.extend(point)
        minPoint = [pt.Z for pt in points]
        index = minPoint.index(min(minPoint))
        
        moveUp = rc.Geometry.Transform.Translation(rc.Geometry.Vector3d.Add(-rc.Geometry.Vector3d(corners[index]), rc.Geometry.Vector3d(point[index])))
        
        building.Transform(moveUp)
        
        trimmedBrep = building.Trim(terrainR, sc.doc.ModelAbsoluteTolerance)
        
        if len(trimmedBrep) == 1:
            trimmedBuildings.append(trimmedBrep[0])
        else:
            w = gh.GH_RuntimeMessageLevel.Warning
            message = "It is not possible move Building n{}. Please, move it manually.".format(i)
            ghenv.Component.AddRuntimeMessage(w, message)
    
    # cap buildings
    solidBuildings = []
    for building in trimmedBuildings:
        surfaces = [t for t in terrain.Split(building, sc.doc.ModelAbsoluteTolerance)]
        area = [rc.Geometry.AreaMassProperties.Compute(srf).Area for srf in surfaces]
        if len(surfaces) == 2:
            cap = surfaces[area.index(min(area))]
            building.Join(cap, sc.doc.ModelAbsoluteTolerance, True)
        else:
            areaTest = []
            testSurfaces = []
            # courtyard
            for i, srf in enumerate(surfaces):
                check = rc.Geometry.Curve.JoinCurves(srf.DuplicateEdgeCurves())
                if len(check) > 1:
                    testSurfaces.append(srf)
            areaTest = [rc.Geometry.AreaMassProperties.Compute(srf).Area for srf in testSurfaces]
            cap = testSurfaces[areaTest.index(min(areaTest))]
            building.Join(cap, sc.doc.ModelAbsoluteTolerance, True)
        
        solidBuildings.append(building)
    
    return solidBuildings


def checkType(buildings):
    for building in buildings:
        if building.GetType() != type(rc.Geometry.Brep()) or not building.IsSolid:
            w = gh.GH_RuntimeMessageLevel.Warning
            message = "Please provide closed breps."
            ghenv.Component.AddRuntimeMessage(w, message)
            return -1
    else: return True


def main():
    
    # check main input
    if _buildings != [] and not None in _buildings and _terrain:
        if checkType(_buildings):
            if checkTerrain(_terrain):
                if _runIt:
                    envimetTerrain = creteBrepTerrain(_terrain)
                    
                    # from breps to meshes
                    meshTerrain = rc.Geometry.Mesh()
                    meshSrf = rc.Geometry.Mesh.CreateFromBrep(envimetTerrain, rc.Geometry.MeshingParameters.Coarse)
                    for m in meshSrf:
                        meshTerrain.Append(m)
                    terrain = meshTerrain
                    
                    buildings = moveAndCutBuilding(_buildings, _terrain)
                    
                    
                else: buildings, terrain = None, None
            else:
                w = gh.GH_RuntimeMessageLevel.Warning
                message = "Please move terrain."
                ghenv.Component.AddRuntimeMessage(w, message)
                return -1
    else:
        w = gh.GH_RuntimeMessageLevel.Warning
        message = "Please provide _inputs."
        ghenv.Component.AddRuntimeMessage(w, message)
        return -1
    
    return buildings


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
    lb_preparation = sc.sticky["ladybug_Preparation"]()
else:
    initCheck = False
    print "You should first let the Ladybug fly..."
    w = gh.GH_RuntimeMessageLevel.Warning
    ghenv.Component.AddRuntimeMessage(w, "You should first let the Ladybug fly...")


if initCheck:
    result = main()
    if result != -1:
        buildings = result