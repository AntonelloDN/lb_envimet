"""
This modules provides the function for Material
"""


import clr
clr.AddReference("System.Xml")
import System.Xml
import datetime
from xml.dom import minidom


def writeMaterials(userMaterials, fullPath):

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
    xml.appendChild(header)

    # add child to header
    headerDict = {'filetype':'DATA',
                  'version': '1',
                  'revisiondate':timeTxt,
                  'remark':'Envi-Data',
                  'encryptionlevel':'1701377'
                  }

    # appendChild
    appendMultipleChild(headerDict, header)


    # add child to header
    for element in userMaterials:
        if element.name == 'SOIL':
            # child of root, Soil
            soil = root.createElement('SOIL')
            xml.appendChild(soil)

            soilMatDict = {'ID':element.id,
                          'Description':element.description,
                          'versiegelung':element.versiegelung,
                          'ns':element.ns,
                          'nfc':element.nfc,
                          'nwilt':element.nwilt,
                          'matpot':element.matpot,
                          'hydro_lf':element.hydro_lf,
                          'volumenw':element.volumenw,
                          'b':element.b,
                          'waerme_lf':element.waerme_lf,
                          'Group':element.Group,
                          'Color':element.Color,
                          'AddValue1':element.AddValue1,
                          'AddValue2':element.AddValue2
                          }
            appendMultipleChild(soilMatDict, soil)
        elif element.name == 'PROFILE':
            # child of root, Profile
            profile = root.createElement('PROFILE')
            xml.appendChild(profile)

            profileMatDict = {'ID':element.id,
                          'Description':element.description,
                          'z0_Length':element.z0_Length,
                          'soilprofil':element.soilprofil,
                          'Albedo':element.Albedo,
                          'Emissivit\xc3\xa4t':element.Emiss,
                          'ExtraID':element.ExtraID,
                          'Irrigated':element.Irrigated,
                          'Color':element.Color,
                          'Color':element.Group,
                          'AddValue1':element.AddValue1,
                          'AddValue2':element.AddValue2
                          }
            appendMultipleChild(profileMatDict, profile)

    # pass xml in xml string
    xml_str = root.toprettyxml(indent="  ")

    with open(fullPath, "w") as f:
        f.write(xml_str[23:])
