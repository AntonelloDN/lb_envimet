import Rhino as rc
import collections
import scriptcontext as sc


class Plant3d(object):

    def __init__(self, geometry, material):
        self.geometry = geometry

        idAndDescription = material.split(',')
        self.materialId = idAndDescription[0]
        self.materialDescrition = idAndDescription[1]


    def threeDimensionalPlants(self, grid):
        nestedMatrix = []
        unit = 1

        curves = [c for c in self.geometry.DuplicateEdgeCurves()]
        closedCrv = [crv for crv in rc.Geometry.Curve.JoinCurves(curves)][0]

        for j in range(grid.numY + unit):
            for i in range(grid.numX + unit):
                point = rc.Geometry.Point3d((i * grid.dimX) + grid.minX, (j * grid.dimY) + grid.minY, grid.zHeight[0])
                if rc.Geometry.Curve.Contains(closedCrv, point, rc.Geometry.Plane.WorldXY, sc.doc.ModelAbsoluteTolerance) == rc.Geometry.PointContainment.Inside:
                    nestedMatrix.append([str(i + unit), str(j + unit),'0', self.materialId, self.materialDescrition, '0'])

        return nestedMatrix
