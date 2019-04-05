import Rhino as rc
import collections
import scriptcontext as sc


class Object2d(object):

    def __init__(self, geometry, material, name):
        self.geometry = geometry
        self.material = material
        self.name = name


    def create2DMatrixPerObj(self, grid, index):

    	pts = []
    	doubleHight = 2

    	matrix = []
    	for j in range(grid.numY + 1):
    		row = []
    		for i in range(grid.numX + 1):
    			point = rc.Geometry.Point3d((i * grid.dimX) + grid.minX, (j * grid.dimY) + grid.minY, grid.zHeight[0])
    			ray = rc.Geometry.Ray3d(point, rc.Geometry.Vector3d.ZAxis)

    			plane = rc.Geometry.Plane(rc.Geometry.Point3d(0, 0, grid.zHeight[0]), rc.Geometry.Vector3d.ZAxis)
    			xprj = rc.Geometry.Transform.PlanarProjection(plane)
    			self.geometry.Transform(xprj)

    			intersection = rc.Geometry.Intersect.Intersection.MeshRay(self.geometry, ray)
    			if intersection != -1.0:
    			    #row.append(self.material)
    			    row.append(index)
    			else:
    			    row.append(0)

    		matrix.append(row)

    	return matrix


    @classmethod
    def merge2dMatrix(cls, nestedMatrix, materials, baseMaterial):
        # because index start from 1
        start = 1

        mergeMatrix = []
        for m in zip(*nestedMatrix):
            row = []
            for l in zip(*m):
                num = max(l)
                mat = baseMaterial
                if num != 0:
                    mat = materials[num - start]

                row.append(mat)
            mergeMatrix.append(row)

        return mergeMatrix
