import Rhino as rc
import collections
import scriptcontext as sc
from copy import deepcopy


class SingleWall(object):

    def __init__(self, geometry, material):
        self.geometry = geometry
        self.material = material


    def __generateMinValueZ(self, zNumbers):

        def diffArrayZdir(num, zNumbers):
            newArr = [abs(num - n) for n in zNumbers]
            return newArr.index(min(newArr))

        bboxGeo = self.geometry.GetBoundingBox(True)
        # take min point
        minPoint = bboxGeo.Min
        zValueGeo = minPoint.Z

        return diffArrayZdir(zValueGeo, zNumbers)


    def simpleWallStringCalcZdir(self, grid):

        contentXml = ""
        for i in range(0, grid.numX + 1):
            for j in range(0, grid.numY + 1):

                point = rc.Geometry.Point3d((i * grid.dimX) + grid.minX, (j * grid.dimY) + grid.minY, 0)
                ln = rc.Geometry.Line(point, rc.Geometry.Vector3d.ZAxis, grid.dimX * 2)

                # projection
                projection = rc.Geometry.Transform.PlanarProjection(rc.Geometry.Plane.WorldXY)
                modShading = deepcopy(self.geometry)
                modShading.Transform(projection)

                if rc.Geometry.Intersect.Intersection.MeshLine(modShading, ln)[0]:
                    contentXml += "{0},{1},{2},{3},{4},{5}\n".format(i, j, self.__generateMinValueZ(grid.zHeight), "", "", self.material)

        return contentXml
