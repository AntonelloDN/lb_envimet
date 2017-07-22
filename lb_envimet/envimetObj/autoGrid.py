# Abraham Yezioro <ayez@ar.technion.ac.il>, Antonello Di Nunzio  <antonellodinunzio@gmail.com>

import Rhino as rc
import scriptcontext as sc
import collections

class setGrid(object):

    def __init__(self, telescope=None, ENVImetVersion=0, maxZGrid = 40, zGrids=15, dimX=3.0, dimY=3.0, dimZ=3.0, startTelescopeHeight=5.0, extLeftXgrid=2, extRightXgrid=2, extUpYgrid=2, extDownYgrid=2, numX=0, numY=0, minX=0, maxX=0, minY=0, maxY=0):
        self.zGrids = zGrids
        self.dimX = dimX
        self.dimY = dimY
        self.dimZ = dimZ
        self.startTelescopeHeight = startTelescopeHeight
        self.extLeftXgrid = extLeftXgrid
        self.extRightXgrid = extRightXgrid
        self.extUpYgrid = extUpYgrid
        self.extDownYgrid = extDownYgrid
        self.telescope = telescope
        self.numX = numX
        self.numY = numY
        self.minX, self.maxX = minX, maxX
        self.minY, self.maxY = minY, maxY
        self.ENVImetVersion = ENVImetVersion
        self.maxZGrid = maxZGrid

        # set Envimet maxZGrid
        if ENVImetVersion == 0: self.maxZGrid = 40
        elif ENVImetVersion == 1: self.maxZGrid = 35
        elif ENVImetVersion == 2: self.maxZGrid = 25

        # set telescope
        if self.telescope == None:
            self.zGrids += 4

        # check additional cell
        if self.extLeftXgrid < 2: self.extLeftXgrid = 2
        if self.extRightXgrid < 2: self.extRightXgrid = 2
        if self.extUpYgrid < 2: self.extUpYgrid = 2
        if self.extDownYgrid < 2: self.extDownYgrid = 2
        if self.extDownYgrid < 2: self.extDownYgrid = 2


    def gZmethod(self, geometry):

        distLeft    = self.extLeftXgrid  * self.dimX
        distRight   = self.extRightXgrid * self.dimX
        distUp      = self.extUpYgrid    * self.dimY
        distDown    = self.extDownYgrid  * self.dimY

        self.minX = self.minY = 10000000
        self.maxX = self.maxY = maxZ = -10000000
        for geo in geometry:
            BB1 = geo.GetBoundingBox(True)
            if self.minX > BB1.Min.X: self.minX = BB1.Min.X
            if self.maxX < BB1.Max.X: self.maxX = BB1.Max.X
            if self.minY > BB1.Min.Y: self.minY = BB1.Min.Y
            if self.maxY < BB1.Max.Y: self.maxY = BB1.Max.Y
            if maxZ < BB1.Max.Z: maxZ = BB1.Max.Z

        #Geometry BoundingBox limits NETO
        self.minX = self.minX - distLeft
        self.minY = self.minY - distDown
        self.maxX = self.maxX + distRight
        self.maxY = self.maxY + distUp

        # Required height -- Twice the heighest building
        reqHeight = maxZ * 2

        domX = self.maxX - self.minX
        domY = self.maxY - self.minY
        self.numX = int(domX / self.dimX)
        self.numY = int(domY / self.dimY)

            # Reccalculate maxX/Y just for the bounding box fit the grid size/length
        self.maxX = self.minX + (self.numX * self.dimX)
        self.maxY = self.minY + (self.numY * self.dimY)

        dimZ = self.dimZ

        gZ = []
        firstGrid = dimZ / 5
        for i in range(0, int(self.zGrids) + 1):
            if self.telescope == None:
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
                elif i == 1 or grid <= self.startTelescopeHeight:
                    grid = (i * dimZ) - (dimZ / 2)
                else:
                    g1 = grid
                    gz = dimZ
                    dimZ = dimZ + (dimZ * self.telescope/ 100 )
                    grid = grid + (dimZ + gz) / 2

                if grid != 0:
                    gZ.append(grid)

            self.gZ = gZ


    def createGridOnBorders(self):
        gridPoints = []
        # XY Grid
        for ix in range (0, self.numX + 1):
            for iy in range (0, self.numY + 1):
                gridPoints.append(rc.Geometry.Point3d( (ix * self.dimX) + self.minX , (iy * self.dimY) + self.minY, self.gZ[0]) )

        # XZ Grid
        for ix in range (0, self.numX + 1):
            for iz in range (0, len(self.gZ)):
                gridPoints.append(rc.Geometry.Point3d( (ix * self.dimX) + self.minX, self.maxY, self.gZ[iz]) )

        # YZ Grid
        for iy in range (0, self.numY + 1):
            for iz in range (0, len(self.gZ)):
                gridPoints.append(rc.Geometry.Point3d( self.maxX, (iy * self.dimY) + self.minY, self.gZ[iz]) )
        return gridPoints


    def emptyMatrix(self):
        matrix = []
        for j in range(self.numY+1):
            row = []
            for i in range(self.numX+1):
                row.append('')
            matrix.append(','.join(row))
        matrix = '\n'.join(matrix)

        return matrix


    def fromPythonToEnvimetMatrix(self, mergedMatrix):
        stringMatrix = []
        for line in mergedMatrix:
            lineStr = ','.join(map(str, line))
            stringMatrix.append(lineStr)

        finalMatrix = '\n'.join(reversed(stringMatrix))

        return finalMatrix

        ###############
        ### 2D OBJ ####
        ###############

    def create2DMatrixPerObj(self, dataList):

        nestedMatrix = []
        pts = []

        for d in dataList:
            matrix = []
            for j in range(self.numY + 1):
                row = []
                for i in range(self.numX + 1):
                    point = rc.Geometry.Point3d((i * self.dimX) + self.minX, (j * self.dimY) + self.minY, self.gZ[0])
                    line = rc.Geometry.Line(point, rc.Geometry.Vector3d.ZAxis, self.dimX*2)

                    # prj on gZ[0]
                    plane = rc.Geometry.Plane(rc.Geometry.Point3d(0, 0, self.gZ[0]), rc.Geometry.Vector3d.ZAxis)
                    xprj = rc.Geometry.Transform.PlanarProjection(plane)
                    d[0].Transform(xprj)

                    if rc.Geometry.Intersect.Intersection.CurveBrep(line.ToNurbsCurve(), d[0], sc.doc.ModelAbsoluteTolerance)[2]:
                        row.append(str(d[1]))
                    else:
                        row.append('')

                matrix.append(row)
            nestedMatrix.append(matrix)

        return nestedMatrix



    def mergeMatrix(self, nestedMatrix, altObj):

        mergeMatrix = []
        for m in zip(*nestedMatrix):
            row = []
            for l in zip(*m):
                counter = collections.Counter(l)
                if len(''.join(l)) == 4:
                    row.append(''.join(l)[:-2])
                elif len(counter.values()) != 1 and '' in l:
                    row.append(''.join(l))
                elif len(''.join(l)) == 2:
                    row.append(''.join(l))
                else:
                    row.append(altObj)
            mergeMatrix.append(row)

        return mergeMatrix

        ###############
        ## BUILDINGS ##
        ###############

    def buildingGrid(self, flag, buildings):

        buildingFlagAndNr, nestedLayers = [], []
        # XY Grid
        for index, building in enumerate(buildings):
            layers = []
            for k in range(0, len(self.gZ)):
                columns = []
                for j in range(self.numY + 1):
                    rows = []
                    for i in range(self.numX + 1):
                        point = rc.Geometry.Point3d((i * self.dimX) + self.minX, (j * self.dimY) + self.minY, self.gZ[k])

                        if building.IsPointInside(point, sc.doc.ModelAbsoluteTolerance * 10, False):
                            bNr = ','.join([str(i), str(j), str(k), '1', str(index + 1)])
                            id = index + 1
                            buildingFlagAndNr.append(bNr)

                            if flag == 0:
                                rows.append(point.Z)
                            else:
                                rows.append(id)
                        else:
                            rows.append(0)
                    columns.append(rows)
                layers.append(columns)
            nestedLayers.append(layers)

        buildingFlagAndNrMatrix = '\n'.join(buildingFlagAndNr)

        return buildingFlagAndNrMatrix, nestedLayers


    def createOneMatrixForBuildings(self, nestedLayers, buildings):
        # merge Matrix
        oneMatrix = []
        for k in zip(*nestedLayers):
            columns = []
            for y in zip(*k):
                rows = []
                for x in zip(*y):
                    total = sum(x)
                    # overlap issue ;)
                    if total > len(buildings):
                        total = 0
                    rows.append(total)
                columns.append(rows)
            oneMatrix.append(columns)

        return oneMatrix


    def setMaterials(self, oneMatrix, matWall, matRoof):
        # spare matrix
        WallDB = []

        for k, layer in enumerate(oneMatrix):
            for j, column in enumerate(layer):
                for i, row in enumerate(column):

                    if row != 0 and oneMatrix[k][j][i-1] == 0 and oneMatrix[k][j-1][i] == 0 and oneMatrix[k-1][j][i] == 0:
                        index = int(row)-1
                        WallDB.append(','.join([str(i),str(j),str(k),matWall[index],matWall[index],matRoof[index]]))
                    elif row != 0 and oneMatrix[k][j][i-1] == 0 and oneMatrix[k][j-1][i] != 0 and oneMatrix[k-1][j][i] == 0:
                        index = int(row)-1
                        WallDB.append(','.join([str(i),str(j),str(k),matWall[index],'',matRoof[index]]))
                    elif row != 0 and oneMatrix[k][j][i-1] != 0 and oneMatrix[k][j-1][i] == 0 and oneMatrix[k-1][j][i] == 0:
                        index = int(row)-1
                        WallDB.append(','.join([str(i),str(j),str(k),'',matWall[index],matRoof[index]]))

                    elif row != 0 and oneMatrix[k][j][i-1] == 0 and oneMatrix[k][j-1][i] == 0 and oneMatrix[k-1][j][i] != 0:
                        index = int(row)-1
                        WallDB.append(','.join([str(i),str(j),str(k),matWall[index],matWall[index],'']))
                    elif row != 0 and oneMatrix[k][j][i-1] == 0 and oneMatrix[k][j-1][i] != 0 and oneMatrix[k-1][j][i] != 0:
                        index = int(row)-1
                        WallDB.append(','.join([str(i),str(j),str(k),matWall[index],'','']))
                    elif row != 0 and oneMatrix[k][j][i-1] != 0 and oneMatrix[k][j-1][i] == 0 and oneMatrix[k-1][j][i] != 0:
                        index = int(row)-1
                        WallDB.append(','.join([str(i),str(j),str(k),'',matWall[index],'']))
                    elif row != 0 and oneMatrix[k][j][i-1] != 0 and oneMatrix[k][j-1][i] != 0 and oneMatrix[k-1][j][i] == 0:
                        index = int(row)-1
                        WallDB.append(','.join([str(i),str(j),str(k),'','',matRoof[index]]))

                    # empty cells
                    elif row == 0 and oneMatrix[k][j][i-1] != 0 and oneMatrix[k][j-1][i] == 0 and oneMatrix[k-1][j][i] == 0:
                        index = int(oneMatrix[k][j][i-1])-1
                        WallDB.append(','.join([str(i),str(j),str(k),matWall[index],'','']))
                    elif row == 0 and oneMatrix[k][j][i-1] == 0 and oneMatrix[k][j-1][i] != 0 and oneMatrix[k-1][j][i] == 0:
                        index = int(oneMatrix[k][j-1][i])-1
                        WallDB.append(','.join([str(i),str(j),str(k),'',matWall[index],'']))
                    elif row == 0 and oneMatrix[k][j][i-1] == 0 and oneMatrix[k][j-1][i] == 0 and oneMatrix[k-1][j][i] != 0:
                        index = int(oneMatrix[k-1][j][i])-1
                        WallDB.append(','.join([str(i),str(j),str(k),'','',matRoof[index]]))

                    elif row == 0 and oneMatrix[k][j][i-1] != 0 and oneMatrix[k][j-1][i] != 0 and oneMatrix[k-1][j][i] == 0:
                        index = int(oneMatrix[k][j-1][i])-1
                        WallDB.append(','.join([str(i),str(j),str(k),matWall[index],matWall[index],'']))
                    elif row == 0 and oneMatrix[k][j][i-1] != 0 and oneMatrix[k][j-1][i] == 0 and oneMatrix[k-1][j][i] != 0:
                        indexW = int(oneMatrix[k][j][i-1])-1
                        indexR = int(oneMatrix[k-1][j][i])-1
                        WallDB.append(','.join([str(i),str(j),str(k),matWall[indexW],'',matRoof[indexR]]))
                    elif row == 0 and oneMatrix[k][j][i-1] == 0 and oneMatrix[k][j-1][i] != 0 and oneMatrix[k-1][j][i] != 0:
                        indexW = int(oneMatrix[k][j-1][i])-1
                        indexR = int(oneMatrix[k-1][j][i])-1
                        WallDB.append(','.join([str(i),str(j),str(k),'',matWall[indexW],matRoof[indexR]]))
                    elif row == 0 and oneMatrix[k][j][i-1] != 0 and oneMatrix[k][j-1][i] != 0 and oneMatrix[k-1][j][i] != 0:
                        indexW = int(oneMatrix[k][j-1][i])-1
                        indexR = int(oneMatrix[k-1][j][i])-1
                        WallDB.append(','.join([str(i),str(j),str(k),matWall[indexW],matWall[indexW],matRoof[indexR]]))

        WallDBMatrix = '\n'.join(WallDB)

        return WallDBMatrix, oneMatrix


    def HmaxNestedMatrix(self, nestedLayers):
        edifici = []
        for singoloEd in nestedLayers:
            lista = []
            for y in zip(*singoloEd):
                listaMaxAltezza = []
                for x in zip(*y):
                    total = max(x)
                    if total != 0:
                        total = int(round(total, 1))
                    listaMaxAltezza.append(total)
                lista.append(listaMaxAltezza)
            edifici.append(lista)
        return edifici


    def HminNestedMatrix(self, nestedLayers):
        edifici = []
        for singoloEd in nestedLayers:
            lista = []
            for y in zip(*singoloEd):
                listaMinAltezza = []
                for x in zip(*y):
                    for num in x:
                        if num != 0:
                            if not self.telescope:
                                num = int(round(num - self.dimZ/10, 1))
                            else:
                                num = int(round(num - self.gZ[0]/2, 1))
                            break
                    listaMinAltezza.append(num)
                lista.append(listaMinAltezza)
            edifici.append(lista)

        return edifici


    def mergeBuildingMatrix(self, hmatrix):
        mergeMatrix = []
        for m in zip(*hmatrix):
            row = []
            for l in zip(*m):
                if 0 in l:
                    num = sum(l)
                else:
                    num = l[0]

                row.append(num)
            mergeMatrix.append(row)

        return mergeMatrix


    def index2DMatrix(self, oneMatrix):
        buildingNr = []

        for k in zip(*oneMatrix):
            columns = []
            emptyColumns = []
            for y in zip(*k):
                index = sum(set(y))
                columns.append(index)

            linebuildingNr = ','.join(map(str, columns))
            buildingNr.append(linebuildingNr)

        buildingNrMatrix = '\n'.join(reversed(buildingNr))

        return buildingNrMatrix

        ###############
        ### TERRAIN ###
        ###############

    def digitalElevationModel3D(self, terrain):

        terrainflag = []
        for k in range(0, len(self.gZ)):
            columns = []
            for j in range(self.numY + 1):
                rows = []
                for i in range(self.numX + 1):
                    point = rc.Geometry.Point3d((i * self.dimX) + self.minX, (j * self.dimY) + self.minY, self.gZ[k])
                    if terrain.IsPointInside(point, sc.doc.ModelAbsoluteTolerance*10, False):
                        tN = ','.join([str(i),str(j),str(k),str('1.00000')])

                        terrainflag.append(tN)

        terrainFlagMatrix = '\n'.join(terrainflag)

        return terrainFlagMatrix


    def digitalElevationModel2D(self, terrain):

        def findMaxHeight(terrain):
            bbox = terrain.GetBoundingBox(True)
            maxHeight = bbox.Max.Z
            return maxHeight

        altitude = findMaxHeight(terrain)

        terrainPattern = []

        for j in range(self.numY + 1):
            rowsHeight = []
            rowsBottom = []
            for i in range(self.numX + 1):
                line = rc.Geometry.Line(rc.Geometry.Point3d((i * self.dimX) + self.minX, (j * self.dimY) + self.minY, self.gZ[0]), rc.Geometry.Vector3d.ZAxis, altitude*2)
                intersection = rc.Geometry.Intersect.Intersection.MeshLine(terrain, line)[0]
                if intersection:
                    heightData = sorted(intersection)
                    rowsHeight.append(str(int(round(max([h.Z for h in heightData]),0))))
                else:
                    rowsHeight.append('0')
                line = ','.join(map(str, rowsHeight))
            terrainPattern.append(line)

        demPattern = '\n'.join(reversed(terrainPattern))

        return demPattern

        ###############
        ## 3D PLANTS ##
        ###############

    def threeDimensionalPlants(self, dataList):
        nestedMatrix = []
        for index, d in enumerate(dataList):
            curves = [c for c in d[0].DuplicateEdgeCurves()]
            closedCrv = [crv for crv in rc.Geometry.Curve.JoinCurves(curves)][0]

            for j in range(self.numY + 1):
                for i in range(self.numX + 1):
                    point = rc.Geometry.Point3d((i * self.dimX) + self.minX, (j * self.dimY) + self.minY, self.gZ[0])
                    if rc.Geometry.Curve.Contains(closedCrv, point, rc.Geometry.Plane.WorldXY, sc.doc.ModelAbsoluteTolerance) == rc.Geometry.PointContainment.Inside:
                        idAndDescription = d[1].split(',')
                        nestedMatrix.append([str(i+1),str(j+1),'0', idAndDescription[0], idAndDescription[1], '0'])
        return nestedMatrix


class NestingGrid(object):
    """Use this class to set nesting grid
    """
    def __init__(self):
        self.numNestingGrid = 3
        self.soilProfileA = 'LO'
        self.soilProfileB = 'LO'
        self.name = 'NestingGrid'
