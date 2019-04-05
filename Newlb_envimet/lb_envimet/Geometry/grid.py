import re
import Rhino as rc
import collections


class Grid(object):

    def __init__(self):
        self._numZ = 15
        self._dimX = 3.0
        self._dimY = 3.0
        self._dimZ = 3.0
        self._startTelescopeHeight = 5.0
        self._extLeftXgrid = 2
        self._extRightXgrid = 2
        self._extUpYgrid = 2
        self._extDownYgrid = 2
        self._telescope = None
        self._numX = 0
        self._numY = 0
        self._minX, self._maxX = 0, 0
        self._minY, self._maxY = 0, 0
        self._maxZGrid = 40
        self._zHeight = []
        self.baseSurface = None


        # set telescope
        if self._telescope == None:
            self._numZ += 4

        # check additional cell
        if self._extLeftXgrid < 2: self._extLeftXgrid = 2
        if self._extRightXgrid < 2: self._extRightXgrid = 2
        if self._extUpYgrid < 2: self._extUpYgrid = 2
        if self._extDownYgrid < 2: self._extDownYgrid = 2


    def getDimX(self):
        return self._dimX

    def getDimY(self):
        return self._dimY

    def getDimZ(self):
        return self._dimZ

    def getZheight(self):
        return self._zHeight

    def getNumX(self):
        return self._numX

    def getNumY(self):
        return self._numY

    def getMinX(self):
        return self._minX

    def getMinY(self):
        return self._minY

    def setDimX(self, value):
        if value > 0:
            self._dimX = value
        else:
            raise ValueError('Only positive value are allowed.')

    def setDimY(self, value):
        if value > 0:
            self._dimY = value
        else:
            raise ValueError('Only positive value are allowed.')

    def setDimZ(self, value):
        if value > 0:
            self._dimZ = value
        else:
            raise ValueError('Only positive value are allowed.')

    def setTelescope(self, value):
        self._telescope = value

    def getTelescope(self):
        return self._telescope

    def setStartTelescopeHeight(self, value):
        self._startTelescopeHeight = value

    def getStartTelescopeHeight(self):
        return self._startTelescopeHeight

    def setStartExtLeftXgrid(self, value):
        self._extLeftXgrid = value

    def setStartExtRightXgrid(self, value):
        self._extRightXgrid = value

    def setStartExtUpYgrid(self, value):
        self._extUpYgrid = value

    def setStartExtDownYgrid(self, value):
        self._extDownYgrid = value

    def setNumZ(self, value):
        self._numZ = value

    def getNumZ(self):
        return self._numZ


    dimX = property(fget=getDimX, fset=setDimX)

    dimY = property(fget=getDimY, fset=setDimY)

    dimZ = property(fget=getDimZ, fset=setDimZ)

    zHeight = property(fget=getZheight)

    numX = property(fget=getNumX)

    numY = property(fget=getNumY)

    minX = property(fget=getMinX)

    minY = property(fget=getMinY)

    telescope = property(fset=setTelescope, fget=getTelescope)

    startTelescopeHeight = property(fset=setStartTelescopeHeight, fget=getStartTelescopeHeight)

    extLeftXgrid = property(fset=setStartExtLeftXgrid)

    extRightXgrid = property(fset=setStartExtRightXgrid)

    extUpYgrid = property(fset=setStartExtUpYgrid)

    extDownYgrid = property(fset=setStartExtDownYgrid)

    numZ = property(fset=setNumZ, fget=getNumZ)


    def gZmethod(self, geometry):

        distLeft    = self._extLeftXgrid  * self.dimX
        distRight   = self._extRightXgrid * self.dimX
        distUp      = self._extUpYgrid    * self.dimY
        distDown    = self._extDownYgrid  * self.dimY

        self._minX = self._minY = 10000000
        self._maxX = self._maxY = maxZ = -10000000
        for geo in geometry:
            BB1 = geo.GetBoundingBox(True)
            if self._minX > BB1.Min.X: self._minX = BB1.Min.X
            if self._maxX < BB1.Max.X: self._maxX = BB1.Max.X
            if self._minY > BB1.Min.Y: self._minY = BB1.Min.Y
            if self._maxY < BB1.Max.Y: self._maxY = BB1.Max.Y
            if maxZ < BB1.Max.Z: maxZ = BB1.Max.Z

        #Geometry BoundingBox limits NETO
        self._minX = self._minX - distLeft
        self._minY = self._minY - distDown
        self._maxX = self._maxX + distRight
        self._maxY = self._maxY + distUp

        # Required height -- Twice the heighest building
        reqHeight = maxZ * 2

        domX = self._maxX - self._minX
        domY = self._maxY - self._minY
        self._numX = int(domX / self.dimX)
        self._numY = int(domY / self.dimY)

        # Reccalculate maxX/Y just for the bounding box fit the grid size/length
        self._maxX = self._minX + (self._numX * self.dimX)
        self._maxY = self._minY + (self._numY * self.dimY)

        dimZ = self.dimZ

        gZ = []
        firstGrid = dimZ / 5
        for i in range(0, int(self._numZ) + 1):
            if self._telescope == None:
                if i <= 5: # In ENVImet the lowest cell is splitted into 5 sub-cells
                    if i == 0:
                        grid = 0
                    elif i == 1:
                        grid = firstGrid / 2
                    else:
                        grid = (i * firstGrid) - (firstGrid / 2)
                else:
                    grid = ((i - 4) * dimZ) - (dimZ / 2)

                if grid != 0:
                    gZ.append(grid)
            else:
                if i == 0: # For Telescope vertical grid calculation
                    grid = 0
                elif i == 1 or grid <= self._startTelescopeHeight:
                    grid = (i * dimZ) - (dimZ / 2)
                else:
                    g1 = grid
                    gz = dimZ
                    dimZ = dimZ + (dimZ * self._telescope/ 100 )
                    grid = grid + (dimZ + gz) / 2

                if grid != 0:
                    gZ.append(grid)

            self._zHeight = gZ


    def gridPreviewXY(self):

        gridPoints = []
        for ix in range (0, self.numX + 1):
            for iy in range (0, self.numY + 1):
                gridPoints.append(rc.Geometry.Point3d( (ix * self.dimX) + self._minX , (iy * self.dimY) + self._minY, self._zHeight[0]) )

        return gridPoints


    def gridPreviewXZ(self):

        gridPoints = []
        for ix in range (0, self.numX + 1):
            for iz in range (0, len(self._zHeight)):
                gridPoints.append(rc.Geometry.Point3d( (ix * self.dimX) + self._minX, self._maxY, self._zHeight[iz]) )

        return gridPoints


    def gridPreviewYZ(self):

        gridPoints = []
        for iy in range (0, self.numY + 1):
            for iz in range (0, len(self._zHeight)):
                gridPoints.append(rc.Geometry.Point3d( self._maxX, (iy * self.dimY) + self._minY, self._zHeight[iz]) )

        return gridPoints

    @property
    def emptyMatrix(self):
        matrix = []
        for j in range(self.numY+1):
            row = []
            for i in range(self.numX+1):
                row.append('')
            matrix.append(','.join(row))
        matrix = '\n'.join(matrix)

        return matrix


    def base3DMatrix(self, item):

        layer = []
        for k in range(0, len(self.zHeight)):
            column = []
            for j in range(self.numY+1):
                row = []
                for i in range(self.numX+1):
                    row.append(item)
                column.append(row)
            layer.append(column)

        return layer


    def fromPythonToEnvimetMatrix(self, uniqueMatrix):
        stringMatrix = []
        for line in uniqueMatrix:
            lineStr = ','.join(map(str, line))
            stringMatrix.append(lineStr)

        finalMatrix = '\n'.join(reversed(stringMatrix))

        return finalMatrix


    def castingPrecision(self, height, value):

        values = ['%.2f' % v for v in height]
        val = values.index('%.2f' % value)

        return val


class NestingGrid(object):
    """Use this class to set nesting grid
    """
    def __init__(self):
        self.numNestingGrid = 3
        self.soilProfileA = '0000LO'
        self.soilProfileB = '0000LO'
