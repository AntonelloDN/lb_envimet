"""
This modules provides main envimet classes.

Classes:
    NestingGrid
    Grid2D
    Grid3D
    Dem
    Plants3D
"""

import Rhino as rc
import scriptcontext as sc
import collections


class NestingGrid(object):
    """Use this class to set nesting grid
    """
    def __init__(self):
        self.numNestingGrid = 3
        self.soilProfileA = 'LO'
        self.soilProfileB = 'LO'
        self.name = 'NestingGrid'


class Grid2D(object):
    """Use this class to generate 2d element matrix
    """

    basePoint = rc.Geometry.Point3d.Origin

    def __init__(self, numX, numY, numZ, dimX, dimY, dimZ, verticalStretch=0, startStretch=0):
        self.numX = numX
        self.numY = numY
        self.numZ = numZ
        self.dimX = dimX
        self.dimY = dimY
        self.dimZ = dimZ
        self.startStretch = startStretch
        self.verticalStretch = verticalStretch


    def viewEquidistantGrid(self):

        points = []
        for k in range(self.numZ+5):
            for j in range(self.numY):
                for i in range(self.numX):
                    if k<5:
                        point = rc.Geometry.Point3d(i*self.dimX+self.dimX/2 + self.basePoint.X, j*self.dimY+self.dimY/2 + self.basePoint.Y, k*self.dimZ/5+self.dimZ/10 + self.basePoint.Z)
                    else:
                        point = rc.Geometry.Point3d(i*self.dimX+self.dimX/2 + self.basePoint.X, j*self.dimY+self.dimY/2 + self.basePoint.Y, (k-4)*self.dimZ+self.dimZ/2 + self.basePoint.Z)
                    points.append(point)

        points = [p for p in points if p.X == ((self.numX - 1)*self.dimX)+self.dimX/2 + self.basePoint.X or p.Y == ((self.numY - 1)*self.dimY)+self.dimY/2 + self.basePoint.Y or p.Z == self.dimZ/10 + self.basePoint.Z]

        return points


    def create2DMatrixPerObj(self, dataList):

        nestedMatrix = []
        pts = []

        for d in dataList:
            matrix = []
            for j in range(self.numY):
                row = []
                for i in range(self.numX):
                    point = rc.Geometry.Point3d(i*self.dimX+self.dimX/2 + self.basePoint.X, j*self.dimY+self.dimY/2 + self.basePoint.Y, self.basePoint.Z)
                    line = rc.Geometry.Line(point, rc.Geometry.Vector3d.ZAxis, self.dimX*2)

                    # this is because of class and basePoint
                    plane = rc.Geometry.Plane(self.basePoint, rc.Geometry.Vector3d.ZAxis)
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


    def fromPythonToEnvimetMatrix(self, mergedMatrix):
        stringMatrix = []
        for line in mergedMatrix:
            lineStr = ','.join(map(str, line))
            stringMatrix.append(lineStr)

        finalMatrix = '\n'.join(reversed(stringMatrix))

        return finalMatrix


    def emptyMatrix(self):
        matrix = []
        for j in range(self.numY+1):
            row = []
            for i in range(self.numX+1):
                row.append('')
            matrix.append(','.join(row))
        matrix = '\n'.join(matrix)

        return matrix


class Grid3D(Grid2D):
    """Use this class to generate 3d element matrix
    """
    def __init__(self, numX, numY, numZ, dimX, dimY, dimZ):
        Grid2D.__init__(self, numX, numY, numZ, dimX, dimY, dimZ)

        #super().__init__(metaname)

    def createAllGridPoints(self, numX, numY, numZ, dimX, dimY, gZ, flag):
        buildingFlagAndNr, nestedLayers = [], []
        # XY Grid
        for index, building in enumerate(buildings):
            layers = []
            for k in range(len(gZ)):
                columns = []  # Antonello
                for j in range(self.numY):
                    rows = []  # Antonello
                    for i in range(self.numX):
                        point = rc.Geometry.Point3d((i * dimX) + minX, (j * self.dimY) + minY, gZ[k])

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


    def matrixConstruction(self, buildings, flag=0):
        """Set flag = 1 if you want to run detailed mode
        """
        buildingFlagAndNr, nestedLayers = [], []

        for index, building in enumerate(buildings):
            layers = []
            for k in range(self.numZ+5):
                columns = []
                for j in range(self.numY):
                    rows = []
                    for i in range(self.numX):
                        if k<5:
                            point = rc.Geometry.Point3d(i*self.dimX+self.dimX/2 + self.basePoint.X, j*self.dimY+self.dimY/2 + self.basePoint.Y, k*self.dimZ/5+self.dimZ/10 + self.basePoint.Z)
                        else:
                            point = rc.Geometry.Point3d(i*self.dimX+self.dimX/2 + self.basePoint.X, j*self.dimY+self.dimY/2 + self.basePoint.Y, (k-4)*self.dimZ+self.dimZ/2 + self.basePoint.Z)

                        if building.IsPointInside(point, sc.doc.ModelAbsoluteTolerance * 10, False):
                            bNr = ','.join([str(i),str(j),str(k),'1',str(index+1)])
                            id = index+1
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


    def createOneMatrixForBuildings(self, buildings, nestedLayers):
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
                        total = int(round(total - self.basePoint.Z, 1))
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
                            num = int(round(num - self.basePoint.Z - self.dimZ/10, 1))
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


class Dem(Grid2D):
    """Use this class to generate envimet dem, this is temporarily available only for equidistant grid
    """
    def __init__(self, numX, numY, numZ, dimX, dimY, dimZ):
        Grid2D.__init__(self, numX, numY, numZ, dimX, dimY, dimZ)
        #super().__init__(metaname)


    def digitalElevationModel3D(self, terrain):

        terrainflag = []

        for k in range(self.numZ+5):
            columns = []
            for j in range(self.numY):
                rows = []
                for i in range(self.numX):
                    if k<5:
                        point = rc.Geometry.Point3d(i*self.dimX+self.dimX/2 + self.basePoint.X, j*self.dimY+self.dimY/2 + self.basePoint.Y, k*self.dimZ/5+self.dimZ/10 + self.basePoint.Z)
                    else:
                        point = rc.Geometry.Point3d(i*self.dimX+self.dimX/2 + self.basePoint.X, j*self.dimY+self.dimY/2 + self.basePoint.Y, (k-4)*self.dimZ+self.dimZ/2 + self.basePoint.Z)
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

        for y in range(self.numY):
            rowsHeight = []
            rowsBottom = []
            for x in range(self.numX):
                line = rc.Geometry.Line(rc.Geometry.Point3d(x*self.dimX + self.basePoint.X + self.dimX/2, y*self.dimY + self.basePoint.Y + self.dimY/2, self.basePoint.Z), rc.Geometry.Vector3d.ZAxis, altitude*2)
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


class Plants3D(Grid2D):
    """Use this class to generate envimet 3d plants
    """
    def __init__(self, numX, numY, numZ, dimX, dimY, dimZ):
        Grid2D.__init__(self, numX, numY, numZ, dimX, dimY, dimZ)


    def threeDimensionalPlants(self, dataList):
        nestedMatrix = []
        for index, d in enumerate(dataList):
            curves = [c for c in d[0].DuplicateEdgeCurves()]
            closedCrv = [crv for crv in rc.Geometry.Curve.JoinCurves(curves)][0]

            for j in range(self.numY):
                for i in range(self.numX):
                    point = rc.Geometry.Point3d(i*self.dimX+self.dimX/2 + self.basePoint.X, j*self.dimY+self.dimY/2 + self.basePoint.Y, self.basePoint.Z)
                    if rc.Geometry.Curve.Contains(closedCrv, point, rc.Geometry.Plane.WorldXY, sc.doc.ModelAbsoluteTolerance) == rc.Geometry.PointContainment.Inside:
                        idAndDescription = d[1].split(',')
                        nestedMatrix.append([str(i+1),str(j+1),'0', idAndDescription[0], idAndDescription[1], '0'])
        return nestedMatrix
