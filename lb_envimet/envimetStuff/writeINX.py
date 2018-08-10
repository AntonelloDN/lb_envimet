"""
This modules provides the function for INX
"""


import clr
clr.AddReference("System.Xml")
import System.Xml
import datetime
from xml.dom import minidom

def writeINX(fullPath, Xcells, Ycells, Zcells, Xdim, Ydim, Zdim, numNesting, matNesting, location, north, buildingCommonMaterial, buildingEmptyMatrix , buildingIds, buildingBottom2d, buildingTop2d, terrain3d , buildingFlag, building3D, plant2d, plant3d, soil, source, emptySequence, terrain2d , isFull3DDesign, verticalStretch, startStretch, telescopingGrid, has3DModel=1):

    # location data
    locationName, latitude, longitude, timeZone = location

    print verticalStretch, startStretch
    # set grid
    if telescopingGrid == 1:
        useSplitting = 0
        verticalStretch = verticalStretch
        startStretch = startStretch
        grids3DK = Zcells
    else:
        useSplitting = 1
        verticalStretch = 0
        startStretch = 0
        Zcells =  Zcells - 4
        grids3DK = Zcells + 4


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
    xml.appendChild(modelGeometry3D)
    xml.appendChild(buildings3D)
    xml.appendChild(dem3D)
    xml.appendChild(WallDB)
    xml.appendChild(SingleWallDB)

    # add child to header
    headerDict = {'filetype':'INPX ENVI-met Area Input File',
                  'version': '4',
                  'revisiondate':timeTxt,
                  'remark':'- Test version -',
                  'encryptionlevel':'0'
                  }
    baseDataDict = {'modelDescription':'DragonFly Document',
                  'modelAuthor': 'DragonFly'
                  }
    modelGeometryDict = {'grids-I': str(Xcells),
                  'grids-J': str(Ycells),
                  'grids-Z': str(Zcells),
                  'dx': '{:f}'.format(Xdim),
                  'dy': '{:f}'.format(Ydim),
                  'dz-base': '{:f}'.format(Zdim),
                  'useTelescoping_grid': str(telescopingGrid),
                  'useSplitting': str(useSplitting),
                  'verticalStretch': '{:f}'.format(verticalStretch),
                  'startStretch': '{:f}'.format(startStretch),
                  'has3DModel': str(has3DModel),
                  'isFull3DDesign': str(isFull3DDesign)
                  }
    nestingAreaDict = {'numberNestinggrids': str(numNesting),
                  'soilProfileA': matNesting[0],
                  'soilProfileB': matNesting[1]
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
    nameAttribute2D, dataAttribute2D = ['type', 'dataI', 'dataJ'], ['matrix-data', str(Xcells), str(Ycells)] #buildingIds
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
    modelGeometry3DDict = {'grids3D-I': str(Xcells),
                  'grids3D-J': str(Ycells),
                  'grids3D-K': str(grids3DK)
                  }
    nameAttribute3Dbuilding, dataAttribute3Dbuilding = ['type', 'dataI', 'dataJ', 'zlayers', 'defaultValue'], ['sparematrix-3D', str(Xcells), str(Ycells), str(grids3DK), '0']
    buildings3DDict = {'buildingFlagAndNr':'\n' + buildingFlag + '\n'
                  }
    nameAttribute3DTerrain, dataAttribute3DTerrain = ['type', 'dataI', 'dataJ', 'zlayers', 'defaultValue'], ['sparematrix-3D', str(Xcells), str(Ycells), str(grids3DK), '0.00000']
    dem3DDict = {'terrainflag':'\n' + terrain3d + '\n'
                  }
    nameAttributeWallDB, dataAttributeWallDB = ['type', 'dataI', 'dataJ', 'zlayers', 'defaultValue'], ['sparematrix-3D', str(Xcells), str(Ycells), str(grids3DK), '']
    WallDBDict = {'ID_wallDB':'\n' + building3D + '\n'
                  }
    nameAttributeSingleWallDB, dataAttributeSingleWallDB = ['type', 'dataI', 'dataJ', 'zlayers', 'defaultValue'], ['sparematrix-3D', str(Xcells), str(Ycells), str(grids3DK), '']
    SingleWallDBDict = {'ID_singlewallDB':''
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

    # pass xml in xml string
    xml_str = root.toprettyxml(indent=" ", newl="\n")

    with open(fullPath, "w") as f:
        f.write(xml_str[23:])
