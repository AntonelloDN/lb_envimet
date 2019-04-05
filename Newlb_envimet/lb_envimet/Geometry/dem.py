import Rhino as rc
import collections
import scriptcontext as sc


class Dem(object):

    def __init__(self, geometry):
        self.geometry = self.__creteBrepTerrain(geometry)
        self._heightMatrix = []
        self._matrix = []

    def getHeightsMatrix(self):
        return self._heightMatrix

    heights = property(fget=getHeightsMatrix)


    def __creteBrepTerrain(self, geometry):
        finalMesh = rc.Geometry.Mesh()

        arrayCrv1 = geometry.GetOutlines(rc.Geometry.Plane.WorldXY)
        arrayCrv2 = geometry.GetNakedEdges()

        baseMesh = rc.Geometry.Mesh.CreateFromClosedPolyline(arrayCrv1[0])

        crv1 = arrayCrv1[0].ToNurbsCurve()
        crv2 = arrayCrv2[0].ToNurbsCurve()

        if not rc.Geometry.Curve.DoDirectionsMatch(crv1, crv2):
            crv1.Reverse()

        # reset seam
        param = 0
        crv1.ClosestPoint(crv2.PointAtStart, param)
        crv1.ChangeClosedCurveSeam(param)

        curves = [crv1, crv2]

        sideGeo = rc.Geometry.Brep.CreateFromLoft(curves, rc.Geometry.Point3d.Unset, rc.Geometry.Point3d.Unset, rc.Geometry.LoftType.Normal, False)[0]
        default_mesh_params = rc.Geometry.MeshingParameters.QualityRenderMesh
        sideGeoMesh = rc.Geometry.Mesh.CreateFromBrep(sideGeo, default_mesh_params)[0]


        finalMesh.Append(sideGeoMesh)
        finalMesh.Append(geometry)
        finalMesh.Append(baseMesh)

        if finalMesh.IsClosed:
            return finalMesh
        else:
            raise ValueError ("Please, provide a valid surface.")


    def createVoxMatrixDem(self, terrainPoints, grid):

        terrainflagMatrix = ""

        self._matrix, self._heightMatrix = grid.base3DMatrix(0),  grid.base3DMatrix(0)

        for i, pt in enumerate(terrainPoints):
            valX = round(((pt.X - grid.minX) / grid.dimX), 0)
            valY = round(((pt.Y - grid.minY) / grid.dimY), 0)
            valZ = grid.castingPrecision(grid.zHeight, pt.Z)

            valX = int(valX)
            valY = int(valY)
            valZ = int(valZ)

            # layer, column, item
            self._heightMatrix [valZ][valY][valX] = pt.Z
            self._matrix[valZ][valY][valX] = 1
            terrainflagMatrix += "{0},{1},{2},1.00000\n".format(valX, valY, valZ)

        return terrainflagMatrix
