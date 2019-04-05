"""
This modules provides classes.

Classes:
    ReadEnvimet
    ReadEnvimetLib
"""

import re
import os
import struct
import clr
clr.AddReference("System.Xml")
import System.Xml

class ReadEnvimet(object):
    """This class read Envimet File
    """

    def __init__(self, metaname):
        self.metaname = metaname


    def readEnvimetNoBinaryFile(self, flag):
        """read Envimet file xml, set 0 if you want to read EDX,
        instead use 1 if you want to read Envimet library.
        """
        if flag == 0:
            characters = '[^\s()_<>/,\.A-Za-z0-9]+'
        else:
            characters = '[^\s()_<>/,\.A-Za-z0-9=""]+'
        with open(self.metaname, 'r') as metafile:
            metainfo = re.sub(characters, '', metafile.read())
        return metainfo


    def writeReadebleEDXFile(self, path, metainfo, variableName = "ENVI", fileType = ".EDX"):
        """write xml version of Envimet File"""
        newFile = os.path.join(path, str(variableName) + fileType)
        with open(newFile, 'w+') as f:
            f.write(metainfo)
        return newFile


    def readXmlwithSystem(self, newXmlFile, date = 'No Date'):
        """Use this method to read xml file"""
        def findTxt(mf, key):
            return mf.GetElementsByTagName(key)[0].InnerText

        # initialize
        metafile = System.Xml.XmlDocument()
        metafile.Load(newXmlFile)
        root = metafile.DocumentElement

        # get variable names as list
        elementList = metafile.GetElementsByTagName("name_variables")
        for item in elementList:
            varnames = item.InnerText.split(',')

        # location
        projectName = findTxt(metafile, "projectname") + ',' + findTxt(metafile, "locationname") + ',' + date
        # dimension of the grid
        gridDimension = [findTxt(metafile, "spacing_x"), findTxt(metafile, "spacing_y"), findTxt(metafile, "spacing_z")]
        dimension = '\n'.join(gridDimension)
        # number of cells
        numOfCells = ','.join([findTxt(metafile,"nr_xdata"), findTxt(metafile, "nr_ydata"), findTxt(metafile, "nr_zdata")])

        xdim = int(findTxt(metafile, "nr_xdata"))
        ydim = int(findTxt(metafile, "nr_ydata"))
        zdim = int(findTxt(metafile, "nr_zdata"))

        return varnames, xdim, ydim, zdim, projectName, dimension, numOfCells


    def writeReadebleTxt(self, newFilePath, dataEDT, variableHeader, newXmlFile, indexVarible, date = 'No Date'):

        # nested method
        varnames, xdim, ydim, zdim, projectName, dimension, numOfCells = self.readXmlwithSystem(newXmlFile, date)
        variables = {}

        # read binary file
        datafile = open(dataEDT, 'rb')
        fileName = os.path.join(newFilePath, indexVarible + ".txt")

        # write txt file
        with open(fileName, 'w') as f:
            f.write(variableHeader + '\n' + projectName + '\n' + numOfCells + '\n' + dimension + '\n')
            for var in varnames:
                variables[var] = struct.unpack('f'*xdim*ydim*zdim, datafile.read(4*xdim*ydim*zdim))
                if var == variableHeader:
                    data = '\n'.join(map(str, variables[variableHeader]))
                    f.write(data)
        datafile.close()

        return fileName


class ReadEnvimetLib(ReadEnvimet):

    def __init__(self, metaname):
        ReadEnvimet.__init__(self, metaname)
        #super().__init__(metaname)


    @staticmethod
    def generateLists(root, key):
        """ Use this method to parse Envimet Library
        """
        nestedList = []
        for element in root.GetElementsByTagName(key):
            childs = []
            for child in element.ChildNodes:
                childs.append(child.InnerText[1:-1])
            nestedList.append(childs)
        return nestedList


    def readLibrary(self, path):

        metainfoLib = self.readEnvimetNoBinaryFile(1)
        newXmlLibFile = self.writeReadebleEDXFile(path, metainfoLib, "dataBase", ".xml")

        # initialize
        metafile = System.Xml.XmlDocument()
        metafile.Load(newXmlLibFile)
        root = metafile.DocumentElement

        # read
        soilList = self.generateLists(root, "SOIL")
        profileList = self.generateLists(root, "PROFILE")
        materialList = self.generateLists(root, "MATERIAL")
        wallList = self.generateLists(root, "WALL")
        sourceList = self.generateLists(root, "SOURCE")
        plantList = self.generateLists(root, "PLANT")
        plant3DList = self.generateLists(root, "PLANT3D")
        greeningList = self.generateLists(root, "GREENING")
        simpleWallList = self.generateLists(root, "SINGLEWALL")


        return soilList, profileList, materialList, wallList, sourceList, plantList, plant3DList, greeningList, simpleWallList
