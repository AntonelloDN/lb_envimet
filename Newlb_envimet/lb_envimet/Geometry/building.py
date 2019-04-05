import Rhino as rc
import collections


class Building(object):

    def __init__(self, geometry, wallMaterial, roofMaterial):
        self._matrix = []
        self._heightMatrix = []
        self.geometry = geometry
        self.wallMaterial = wallMaterial
        self.roofMaterial = roofMaterial
        self.greenWallMaterial = ""
        self.greenRoofMaterial = ""

    def setMatrix(self, value):
        self._matrix = value

    def getBuildingFlagAndNr(self):
        return self._buildingFlagAndNr

    def setBuildingFlagAndNr(self, value):
        self._buildingFlagAndNr = value

    def getMatrix(self):
        return self._matrix

    def getHightMatrix(self):
        return self._heightMatrix

    matrix = property(fset=setMatrix, fget=getMatrix)

    buildingHightMatrix = property(fget=getHightMatrix)

    buildingFlagAndNr = property(fset=setBuildingFlagAndNr, fget=getBuildingFlagAndNr)


    @staticmethod
    def voxelPoints(mesh, tol, grid):

        zAxis = rc.Geometry.Vector3d.ZAxis

        planes = []
        for i, num in enumerate(grid.zHeight):
            pl = rc.Geometry.Plane(rc.Geometry.Point3d(0,0,num), zAxis)
            planes.append(pl)

        gridXY = grid.gridPreviewXY()

        polilinee = rc.Geometry.Intersect.Intersection.MeshPlane(mesh, planes)
        polilinee = [ln.ToNurbsCurve() for ln in polilinee]

        superfici = rc.Geometry.Brep.CreatePlanarBreps(polilinee, tol);

        bbox = mesh.GetBoundingBox(False);

        pointForProjection = []

        # small scaled grid
        for i, pt in enumerate(gridXY):
            if (pt.X >= bbox.Min.X - grid.dimX and pt.X <= bbox.Max.X + grid.dimX):
                if (pt.Y >= bbox.Min.Y - grid.dimY and pt.Y <= bbox.Max.Y + grid.dimY):
                    pointForProjection.append(rc.Geometry.Point3d(pt.X, pt.Y, 0));

        voxelPoints = rc.Geometry.Intersect.Intersection.ProjectPointsToBreps(superfici, pointForProjection, zAxis, tol);

        return voxelPoints


    def createVoxMatrixBuilding(self, buildingPoints, terrainPoints, index, grid):

        buildingFlagAndNr = ""

        self._matrix, self._heightMatrix = grid.base3DMatrix(0), grid.base3DMatrix(0)

        for i, pt in enumerate(buildingPoints):
            valX = round(((pt.X - grid.minX) / grid.dimX), 0)
            valY = round(((pt.Y - grid.minY) / grid.dimY), 0)

            if pt not in terrainPoints:
                valZ = grid.castingPrecision(grid.zHeight, pt.Z)

                valX = int(valX)
                valY = int(valY)
                valZ = int(valZ)

                # layer, column, item
                self._heightMatrix [valZ][valY][valX] = pt.Z
                self._matrix[valZ][valY][valX] = index
                buildingFlagAndNr += "{0},{1},{2},{3},{4}\n".format(valX, valY, valZ, 1, index)

        return buildingFlagAndNr


    # last step, just one matrix
    @classmethod
    def mergeMatrix(cls, buildingMatrix, buildings):
        # merge Matrix
        uniqueMatrix = []
        for k in zip(*buildingMatrix):
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
            uniqueMatrix.append(columns)

        return uniqueMatrix


    @classmethod
    def setMaterials(cls, uniqueMatrix, matWall, matRoof):
        # spare matrix
        WallDB = []

        for k, layer in enumerate(uniqueMatrix):
            for j, column in enumerate(layer):
                for i, row in enumerate(column):

                    if row != 0 and uniqueMatrix[k][j][i-1] == 0 and uniqueMatrix[k][j-1][i] == 0 and uniqueMatrix[k-1][j][i] == 0:
                        index = int(row)-1
                        WallDB.append(','.join([str(i),str(j),str(k),matWall[index],matWall[index],matRoof[index]]))
                    elif row != 0 and uniqueMatrix[k][j][i-1] == 0 and uniqueMatrix[k][j-1][i] != 0 and uniqueMatrix[k-1][j][i] == 0:
                        index = int(row)-1
                        WallDB.append(','.join([str(i),str(j),str(k),matWall[index],'',matRoof[index]]))
                    elif row != 0 and uniqueMatrix[k][j][i-1] != 0 and uniqueMatrix[k][j-1][i] == 0 and uniqueMatrix[k-1][j][i] == 0:
                        index = int(row)-1
                        WallDB.append(','.join([str(i),str(j),str(k),'',matWall[index],matRoof[index]]))

                    elif row != 0 and uniqueMatrix[k][j][i-1] == 0 and uniqueMatrix[k][j-1][i] == 0 and uniqueMatrix[k-1][j][i] != 0:
                        index = int(row)-1
                        WallDB.append(','.join([str(i),str(j),str(k),matWall[index],matWall[index],'']))
                    elif row != 0 and uniqueMatrix[k][j][i-1] == 0 and uniqueMatrix[k][j-1][i] != 0 and uniqueMatrix[k-1][j][i] != 0:
                        index = int(row)-1
                        WallDB.append(','.join([str(i),str(j),str(k),matWall[index],'','']))
                    elif row != 0 and uniqueMatrix[k][j][i-1] != 0 and uniqueMatrix[k][j-1][i] == 0 and uniqueMatrix[k-1][j][i] != 0:
                        index = int(row)-1
                        WallDB.append(','.join([str(i),str(j),str(k),'',matWall[index],'']))
                    elif row != 0 and uniqueMatrix[k][j][i-1] != 0 and uniqueMatrix[k][j-1][i] != 0 and uniqueMatrix[k-1][j][i] == 0:
                        index = int(row)-1
                        WallDB.append(','.join([str(i),str(j),str(k),'','',matRoof[index]]))

                    # empty cells
                    elif row == 0 and uniqueMatrix[k][j][i-1] != 0 and uniqueMatrix[k][j-1][i] == 0 and uniqueMatrix[k-1][j][i] == 0:
                        index = int(uniqueMatrix[k][j][i-1])-1
                        WallDB.append(','.join([str(i),str(j),str(k),matWall[index],'','']))
                    elif row == 0 and uniqueMatrix[k][j][i-1] == 0 and uniqueMatrix[k][j-1][i] != 0 and uniqueMatrix[k-1][j][i] == 0:
                        index = int(uniqueMatrix[k][j-1][i])-1
                        WallDB.append(','.join([str(i),str(j),str(k),'',matWall[index],'']))
                    elif row == 0 and uniqueMatrix[k][j][i-1] == 0 and uniqueMatrix[k][j-1][i] == 0 and uniqueMatrix[k-1][j][i] != 0:
                        index = int(uniqueMatrix[k-1][j][i])-1
                        WallDB.append(','.join([str(i),str(j),str(k),'','',matRoof[index]]))

                    elif row == 0 and uniqueMatrix[k][j][i-1] != 0 and uniqueMatrix[k][j-1][i] != 0 and uniqueMatrix[k-1][j][i] == 0:
                        index = int(uniqueMatrix[k][j-1][i])-1
                        WallDB.append(','.join([str(i),str(j),str(k),matWall[index],matWall[index],'']))
                    elif row == 0 and uniqueMatrix[k][j][i-1] != 0 and uniqueMatrix[k][j-1][i] == 0 and uniqueMatrix[k-1][j][i] != 0:
                        indexW = int(uniqueMatrix[k][j][i-1])-1
                        indexR = int(uniqueMatrix[k-1][j][i])-1
                        WallDB.append(','.join([str(i),str(j),str(k),matWall[indexW],'',matRoof[indexR]]))
                    elif row == 0 and uniqueMatrix[k][j][i-1] == 0 and uniqueMatrix[k][j-1][i] != 0 and uniqueMatrix[k-1][j][i] != 0:
                        indexW = int(uniqueMatrix[k][j-1][i])-1
                        indexR = int(uniqueMatrix[k-1][j][i])-1
                        WallDB.append(','.join([str(i),str(j),str(k),'',matWall[indexW],matRoof[indexR]]))
                    elif row == 0 and uniqueMatrix[k][j][i-1] != 0 and uniqueMatrix[k][j-1][i] != 0 and uniqueMatrix[k-1][j][i] != 0:
                        indexW = int(uniqueMatrix[k][j-1][i])-1
                        indexR = int(uniqueMatrix[k-1][j][i])-1
                        WallDB.append(','.join([str(i),str(j),str(k),matWall[indexW],matWall[indexW],matRoof[indexR]]))

        WallDBMatrix = '\n'.join(WallDB)

        return WallDBMatrix


    @classmethod
    def hmaxMatrixAndIndexMatrix(cls, buildingMatrix):
        """
            Use the same method for index matrix:
            nested self.grid for indexMatrix
            nested self.buildingHightMatrix for height matrix
        """
        buildings = []
        for bl in buildingMatrix:
            row = []
            for y in zip(*bl):
                maxHeight = []
                for x in zip(*y):
                    total = max(x)
                    if total != 0:
                        total = int(round(total, 1))
                    maxHeight.append(total)
                row.append(maxHeight)
            buildings.append(row)

        return buildings


    @classmethod
    def hminMatrix(cls, buildingMatrix, grid):
        buildings = []
        for bl in buildingMatrix:
            row = []
            for y in zip(*bl):
                minHight = []
                for x in zip(*y):
                    for num in x:
                        if num != 0:
                            if not grid._telescope:
                                num = int(round(num - grid.dimZ/10, 1))
                            else:
                                num = int(round(num - grid.zHeight[0]/2, 1))
                            break
                    minHight.append(num)
                row.append(minHight)
            buildings.append(row)

        return buildings


    @classmethod
    def mergeBuildingMatrix(cls, hmatrix):
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


    def moveBuildingsUp(self, mesh, terrain):

        zAxis = rc.Geometry.Vector3d.ZAxis
        noIntersection = 0.0
        unitBox = 1
        vecZero = rc.Geometry.Vector3d.Zero

        try:
            # first traslation
            center = rc.Geometry.AreaMassProperties.Compute(mesh).Centroid
            r = rc.Geometry.Ray3d(center, zAxis)
            intersec = rc.Geometry.Intersect.Intersection.MeshRay(terrain, r)

            pt = r.PointAt(intersec)

            if (intersec != noIntersection):
                vecCentroid = rc.Geometry.Vector3d(0, 0, pt.Z - center.Z)
                xmoveCentroid = rc.Geometry.Transform.Translation(vecCentroid)
                mesh.Transform(xmoveCentroid);

            # move to terrain
            bBox = mesh.GetBoundingBox(True)
            meshBox = rc.Geometry.Mesh.CreateFromBox(bBox, unitBox, unitBox, unitBox)
            lines = rc.Geometry.Intersect.Intersection.MeshMeshFast(terrain, mesh)
            minBBox = bBox.Min

            # dimension
            start = minBBox.Z;
            end = min([l.From.Z for l in lines])
            vecTerrain = rc.Geometry.Vector3d(0, 0, end - start)
            xmoveTerrain = rc.Geometry.Transform.Translation(vecTerrain)

        except:
            xmoveTerrain = rc.Geometry.Transform.Translation(vecZero)

        mesh.Transform(xmoveTerrain)

        return mesh
