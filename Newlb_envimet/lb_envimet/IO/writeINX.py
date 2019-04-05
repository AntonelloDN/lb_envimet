"""
This modules provides the function for INX
"""

import re
import clr
clr.AddReference("System.Xml")
import System.Xml
import datetime
from xml.dom import minidom
from copy import deepcopy
from Geometry import Grid, Building, Dem, Object2d, Plant3d


def get2dObjectMatrix(grid, objects, baseMaterial):

    nestedMatrix = []
    materials = []

    for i, ob in enumerate(objects):
        matrix = ob.create2DMatrixPerObj(grid, i+1)
        nestedMatrix.append(matrix)
        materials.append(ob.material)

    mergedMatrix = Object2d.merge2dMatrix(nestedMatrix, materials, baseMaterial)
    matrix = grid.fromPythonToEnvimetMatrix(mergedMatrix)

    return matrix


def getDemMatrix(grid, terrain):

    # preparation
    demVoxel = []
    demDBMatrix = ''
    dem2d = re.sub('', '0', grid.emptyMatrix)

    if terrain:
        demVoxel = Building.voxelPoints(terrain.geometry, 0.01, grid)
        demDBMatrix = terrain.createVoxMatrixDem(demVoxel, grid)
        maxDem = Building.hmaxMatrixAndIndexMatrix([terrain.heights])
        mergedMaxMatrix = Building.mergeBuildingMatrix(maxDem)
        dem2d = grid.fromPythonToEnvimetMatrix(mergedMaxMatrix)

    return demVoxel, demDBMatrix, dem2d


def getBuildingPreparationMatrix(grid, buildings, terrain, demVoxel):

    listMatrixNormalMaterial, listMatrixGreenMaterial = [], []
    hightMatrixBuilding = []
    wallMaterial, greenWallMaterial = [], []
    roofMaterial, greenRoofMaterial = [], []
    buildingNumberMatrix = ""
    greenInfo = []

    for i, bld in enumerate(buildings):

        if demVoxel:
        	modBuildings = deepcopy(bld.geometry)
        	modBuildings = bld.moveBuildingsUp(modBuildings, terrain.geometry)
        else:
        	modBuildings = bld.geometry
        buildingVoxel = Building.voxelPoints(modBuildings, 0.01, grid)
        buildingFlagAndNr = bld.createVoxMatrixBuilding(buildingVoxel, demVoxel, i+1, grid)

        listMatrixNormalMaterial.append(bld.matrix)
        hightMatrixBuilding.append(bld.buildingHightMatrix)

        wallMaterial.append(bld.wallMaterial)
        roofMaterial.append(bld.roofMaterial)

        buildingNumberMatrix += buildingFlagAndNr

        # green
        if bld.greenWallMaterial != "" or bld.greenRoofMaterial != "":
            listMatrixGreenMaterial.append(bld.matrix)
            greenWallMaterial.append(bld.greenWallMaterial)
            greenRoofMaterial.append(bld.greenRoofMaterial)
            greenBld = [i, ' ', bld.wallMaterial, bld.roofMaterial, bld.greenWallMaterial, bld.greenRoofMaterial]
            greenInfo.append(greenBld)
        else:
            greenWallMaterial.append("")
            greenRoofMaterial.append("")

    # Building Matrix
    uniqueMatrix = Building.mergeMatrix(listMatrixNormalMaterial, buildings)
    wallDBMatrix = Building.setMaterials(uniqueMatrix, wallMaterial, roofMaterial)

    uniqueGreenMatrix = Building.mergeMatrix(listMatrixGreenMaterial, buildings)
    greenDBMatrix = Building.setMaterials(uniqueGreenMatrix, greenWallMaterial, greenRoofMaterial)

    # 2d part
    # Top Matrix
    tempHmaxMatrix = Building.hmaxMatrixAndIndexMatrix(hightMatrixBuilding)
    mergedMaxMatrix = Building.mergeBuildingMatrix(tempHmaxMatrix)
    topMatrix = grid.fromPythonToEnvimetMatrix(mergedMaxMatrix)

    # Bottom Matrix
    tempHminMatrix = Building.hminMatrix(hightMatrixBuilding, grid)
    mergedMimMatrix = Building.mergeBuildingMatrix(tempHminMatrix)
    bottomMatrix = grid.fromPythonToEnvimetMatrix(mergedMimMatrix)

    # Id Matrix
    tempHmaxMatrix = Building.hmaxMatrixAndIndexMatrix(listMatrixNormalMaterial)
    mergedMaxMatrix = Building.mergeBuildingMatrix(tempHmaxMatrix)
    IdMatrix = grid.fromPythonToEnvimetMatrix(mergedMaxMatrix)

    return IdMatrix, bottomMatrix, topMatrix, buildingNumberMatrix, wallDBMatrix, greenInfo, greenDBMatrix


def treeObjectMatrix(grid, trees):
    nestedMatrix = []

    for i, ob in enumerate(trees):
        matrix = ob.threeDimensionalPlants(grid)
        nestedMatrix.extend(matrix)

    return nestedMatrix


def getSimpleWall(grid, shadings):

    content = ""

    for i, ob in enumerate(shadings):
        content += ob.simpleWallStringCalcZdir(grid)

    return content



def writeINX(fullPath, grid, location, nesting, buildingMatrix, buildingCommonMaterial, terrain2d, terrain3d, plant2d, plant3d, soil, source, shadings):
    """
        Write INX file
    """

    # only 3d models
    has3DModel, isFull3DDesign = 1, 1
    emptySequence = grid.emptyMatrix
    unit = 1

    # building data
    buildingEmptyMatrix , buildingIds, buildingBottom2d, buildingTop2d, buildingFlag, building3D, greenIds, greenDBMatrix = buildingMatrix
    # location data
    locationName, latitude, longitude, timeZone, north = location

    # set grid (this part will be implemented)
    gridX = grid.numX + unit
    gridY = grid.numY + unit
    if grid.telescope != None:
        telescopingGrid = 1
        useSplitting = 0
        verticalStretch = grid.telescope
        startStretch = grid.startTelescopeHeight
        grids3DK = grid.numZ
        grids2DK = grid.numZ
    else:
        telescopingGrid = 0
        useSplitting = 1
        verticalStretch = 0
        startStretch = 0
        grids2DK = grid.numZ - 4
        grids3DK = grid.numZ


    def appendMultipleChild(childChild, childRoot):
        elements = []
        for key, element in childChild.items():
            xmlElement = root.createElement(key)
            xmlElement.appendChild(root.createTextNode(element))
            elements.append(xmlElement)
        for node in elements:
            childRoot.childNodes.append(node)


    def appendMultipleChildWithAttribute(childChild, childRoot, nameAttribute, dataAttribute):
        elements = []
        for key, element in childChild.items():
            xmlElement = root.createElement(key)
            for name, attr in zip(nameAttribute, dataAttribute):
                xmlElement.setAttribute(name, attr)
            xmlElement.appendChild(root.createTextNode(element))
            elements.append(xmlElement)
        for node in elements:
            childRoot.childNodes.append(node)


    # date
    timeTxt = datetime.datetime.now()
    timeTxt = str(timeTxt)[:-7]

    root = minidom.Document()

    # create an xml document, ENVI-MET_Datafile
    xml = root.createElement('ENVI-MET_Datafile')
    root.appendChild(xml)


    # child of root, Header
    header = root.createElement('Header')
    baseData = root.createElement('baseData')
    modelGeometry = root.createElement('modelGeometry')
    nestingArea = root.createElement('nestingArea')
    locationData = root.createElement('locationData')
    defaultSettings = root.createElement('defaultSettings')
    buildings2D = root.createElement('buildings2D')
    simpleplants2D = root.createElement('simpleplants2D')
    soils2D = root.createElement('soils2D')
    dem = root.createElement('dem')
    sources2D = root.createElement('sources2D')
    receptors2D = root.createElement('receptors2D')# empty
    additionalData = root.createElement('additionalData')# empty
    modelGeometry3D = root.createElement('modelGeometry3D')
    buildings3D = root.createElement('buildings3D')
    dem3D = root.createElement('dem3D')
    WallDB = root.createElement('WallDB')
    SingleWallDB = root.createElement('SingleWallDB')
    GreeningDB = root.createElement('GreeningDB')


    xml.appendChild(header)
    xml.appendChild(baseData)
    xml.appendChild(modelGeometry)
    xml.appendChild(nestingArea)
    xml.appendChild(locationData)
    xml.appendChild(defaultSettings)
    xml.appendChild(buildings2D)
    xml.appendChild(simpleplants2D)
    if plant3d:
        for plant in plant3d:
            plants3D = root.createElement('3Dplants')
            xml.appendChild(plants3D)
            plants3DDict = {'rootcell_i': str(plant[0]),
                          'rootcell_j': str(plant[1]),
                          'rootcell_k': str(plant[2]),
                          'plantID': str(plant[3]),
                          'name': str(plant[4]),
                          'observe': str(plant[5])
                          }
            appendMultipleChild(plants3DDict, plants3D)
    xml.appendChild(soils2D)
    xml.appendChild(dem)
    xml.appendChild(sources2D)
    xml.appendChild(receptors2D)
    xml.appendChild(additionalData)
    if greenIds:
        for green in greenIds:
            greenIdsRoot = root.createElement('Buildinginfo')
            xml.appendChild(greenIdsRoot)
            greenDict = {'BuildingInternalNr': str(green[0] + unit),
                          'BuildingName': str(green[1]),
                          'BuildingWallMaterial': str(green[2]),
                          'BuildingRoofMaterial': str(green[3]),
                          'BuildingFacadeGreening': str(green[4]),
                          'BuildingRoofGreening': str(green[5])
                          }
            appendMultipleChild(greenDict, greenIdsRoot)
    xml.appendChild(modelGeometry3D)
    xml.appendChild(buildings3D)
    xml.appendChild(dem3D)
    xml.appendChild(WallDB)
    xml.appendChild(SingleWallDB)
    xml.appendChild(GreeningDB)

    # add child to header
    headerDict = {'filetype':'INPX ENVI-met Area Input File',
                  'version': '401',
                  'revisiondate':timeTxt,
                  'remark':'- Test version -',
                  'encryptionlevel':'0'
                  }
    baseDataDict = {'modelDescription':'DragonFly Document',
                  'modelAuthor': 'DragonFly'
                  }
    modelGeometryDict = {'grids-I': str(gridX),
                  'grids-J': str(gridY),
                  'grids-Z': str(grids2DK),
                  'dx': '{:f}'.format(grid.dimX),
                  'dy': '{:f}'.format(grid.dimY),
                  'dz-base': '{:f}'.format(grid.dimZ),
                  'useTelescoping_grid': str(telescopingGrid),
                  'useSplitting': str(useSplitting),
                  'verticalStretch': '{:f}'.format(verticalStretch),
                  'startStretch': '{:f}'.format(startStretch),
                  'has3DModel': str(has3DModel),
                  'isFull3DDesign': str(isFull3DDesign)
                  }
    nestingAreaDict = {'numberNestinggrids': str(nesting.numNestingGrid),
                  'soilProfileA': nesting.soilProfileA,
                  'soilProfileB': nesting.soilProfileB
                  }
    locationDataDict = {'modelRotation':'{:f}'.format(north),
                  'projectionSystem': '',
                  'realworldLowerLeft_X':'0.00000',
                  'realworldLowerLeft_Y':'0.00000',
                  'locationName':locationName,
                  'location_Longitude':longitude,
                  'location_Latitude':latitude,
                  'locationTimeZone_Name':timeZone,
                  'locationTimeZone_Longitude':'15.00000'
                  }
    defaultSettingsDict = {'commonWallMaterial': buildingCommonMaterial[0],
                  'commonRoofMaterial': buildingCommonMaterial[1]
                  }
    nameAttribute2D, dataAttribute2D = ['type', 'dataI', 'dataJ'], ['matrix-data', str(gridX), str(gridY)] #buildingIds
    buildings2DDict = {'zTop':'\n' + buildingTop2d + '\n',
                  'zBottom': '\n' + buildingBottom2d + '\n',
                  'buildingNr': '\n' + buildingIds + '\n',
                  'fixedheight': '\n' + buildingEmptyMatrix + '\n'
                  }
    simpleplants2DDict = {'ID_plants1D':'\n' + plant2d + '\n'
                  }
    soils2DDict = {'ID_soilprofile':'\n' + soil + '\n'
                  }
    demDict = {'terrainheight':'\n' + terrain2d + '\n'
                  }
    sources2DDict = {'ID_sources':'\n' + source + '\n'
                  }
    receptors2DDict = {'ID_receptors':'\n' + emptySequence + '\n'
                  }# empty
    additionalDataDict = {'db_link_point':'\n' + emptySequence + '\n',
                  'db_link_area':'\n' + emptySequence + '\n'
                  }# empty
    modelGeometry3DDict = {'grids3D-I': str(gridX),
                  'grids3D-J': str(gridY),
                  'grids3D-K': str(grids3DK)
                  }
    nameAttribute3Dbuilding, dataAttribute3Dbuilding = ['type', 'dataI', 'dataJ', 'zlayers', 'defaultValue'], ['sparematrix-3D', str(gridX), str(gridY), str(grids3DK), '0']
    buildings3DDict = {'buildingFlagAndNr':'\n' + buildingFlag + '\n'
                  }
    nameAttribute3DTerrain, dataAttribute3DTerrain = ['type', 'dataI', 'dataJ', 'zlayers', 'defaultValue'], ['sparematrix-3D', str(gridX), str(gridY), str(grids3DK), '0.00000']
    dem3DDict = {'terrainflag':'\n' + terrain3d + '\n'
                  }
    nameAttributeWallDB, dataAttributeWallDB = ['type', 'dataI', 'dataJ', 'zlayers', 'defaultValue'], ['sparematrix-3D', str(gridX), str(gridY), str(grids3DK), '']
    WallDBDict = {'ID_wallDB':'\n' + building3D + '\n'
                  }
    nameAttributeSingleWallDB, dataAttributeSingleWallDB = ['type', 'dataI', 'dataJ', 'zlayers', 'defaultValue'], ['sparematrix-3D', str(gridX), str(gridY), str(grids3DK), '']
    SingleWallDBDict = {'ID_singlewallDB':'\n' + shadings
                  }
    nameAttributeGreenDB, dataAttributeGreenDB = ['type', 'dataI', 'dataJ', 'zlayers', 'defaultValue'], ['sparematrix-3D', str(gridX), str(gridY), str(grids3DK), '']
    GreeningDBDict = {'ID_GreeningDB':'\n' + greenDBMatrix + '\n'
                  }

    # appendChild!
    appendMultipleChild(headerDict, header)
    appendMultipleChild(baseDataDict, baseData)
    appendMultipleChild(modelGeometryDict, modelGeometry)
    appendMultipleChild(nestingAreaDict, nestingArea)
    appendMultipleChild(locationDataDict, locationData)
    appendMultipleChild(defaultSettingsDict, defaultSettings)
    appendMultipleChildWithAttribute(buildings2DDict, buildings2D, nameAttribute2D, dataAttribute2D)
    appendMultipleChildWithAttribute(simpleplants2DDict, simpleplants2D, nameAttribute2D, dataAttribute2D)
    appendMultipleChildWithAttribute(soils2DDict, soils2D, nameAttribute2D, dataAttribute2D)
    appendMultipleChildWithAttribute(demDict, dem, nameAttribute2D, dataAttribute2D)
    appendMultipleChildWithAttribute(sources2DDict, sources2D, nameAttribute2D, dataAttribute2D)
    appendMultipleChildWithAttribute(receptors2DDict, receptors2D, nameAttribute2D, dataAttribute2D)
    appendMultipleChildWithAttribute(additionalDataDict, additionalData, nameAttribute2D, dataAttribute2D)
    appendMultipleChild(modelGeometry3DDict, modelGeometry3D)
    appendMultipleChildWithAttribute(buildings3DDict, buildings3D, nameAttribute3Dbuilding, dataAttribute3Dbuilding)
    appendMultipleChildWithAttribute(dem3DDict, dem3D, nameAttribute3DTerrain, dataAttribute3DTerrain)
    appendMultipleChildWithAttribute(WallDBDict, WallDB, nameAttributeWallDB, dataAttributeWallDB)
    appendMultipleChildWithAttribute(SingleWallDBDict, SingleWallDB, nameAttributeSingleWallDB, dataAttributeSingleWallDB)
    appendMultipleChildWithAttribute(GreeningDBDict, GreeningDB, nameAttributeGreenDB, dataAttributeGreenDB)

    # pass xml in xml string
    xml_str = root.toprettyxml(indent=" ", newl="\n")

    with open(fullPath, "w") as f:
        f.write(xml_str[23:])
