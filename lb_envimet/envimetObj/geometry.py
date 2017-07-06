"""
This modules provides some geometry capabilities.

Classes:
    BrepStuff
    terrainGeometry
"""

import Rhino as rc
import scriptcontext as sc

class buildingGeometry(object):
    """This class contain some building geometry utilities.
    """

    def __init__(self, objects):
        self.objects = objects


    def fromBrepToMesh(self):
        # from breps to meshes
        meshes = []
        for item in self.objects:
            bulkMesh = rc.Geometry.Mesh()
            if item.IsSolid:
                meshSrf = rc.Geometry.Mesh.CreateFromBrep(item, rc.Geometry.MeshingParameters.Coarse)
                for mesh in meshSrf:
                    bulkMesh.Append(mesh)
                meshes.append(bulkMesh)

        return meshes



class terrainGeometry(object):
    """This class create terrain meshes.
    """

    def __init__(self, terrain):
        self.terrain = terrain
        self.name = 'Terrain' # this is because terrain does not have material


    def creteBrepTerrain(self):
        terrainToPrj = rc.Geometry.Brep.Duplicate(self.terrain)
        prj = rc.Geometry.Transform.PlanarProjection(rc.Geometry.Plane.WorldXY)
        terrainToPrj.Transform(prj)

        # create 'solid'
        borderCrvUp = [crv for crv in self.terrain.DuplicateEdgeCurves()]
        borderCrvDown = [crv for crv in terrainToPrj.DuplicateEdgeCurves()]
        borderCrvUp = rc.Geometry.Curve.JoinCurves(borderCrvUp)[0]
        borderCrvDown = rc.Geometry.Curve.JoinCurves(borderCrvDown)[0]

        terrainBrep = rc.Geometry.Brep.CreateFromLoft([borderCrvUp, borderCrvDown], rc.Geometry.Point3d.Unset, rc.Geometry.Point3d.Unset, rc.Geometry.LoftType.Straight, False)
        terrainBrep = rc.Geometry.Brep.JoinBreps([self.terrain, terrainBrep[0], terrainToPrj], sc.doc.ModelAbsoluteTolerance)[0]

        # create terrain mesh
        if terrainBrep.IsSolid:
            meshTerrain = rc.Geometry.Mesh()
            meshSrf = rc.Geometry.Mesh.CreateFromBrep(terrainBrep, rc.Geometry.MeshingParameters.Coarse)
            for m in meshSrf:
                meshTerrain.Append(m)

            return meshTerrain
        else: return None
