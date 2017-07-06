"""
This modules provides material classes.

Classes:
    SetMaterials
"""

class SetMaterials(object):

    def __init__(self, geometry, idMat, defaultMat, flag=0, name=None , baseMat=''):
        self.geometry = geometry
        self.idMat = idMat
        self.defaultMat = defaultMat
        self.flag = flag
        self.name = name
        self.baseMat = baseMat

    @property
    def makeAttributeTuple(self):

        # default materials
        if len(self.idMat) != len(self.geometry) and self.idMat != []:
            dataMat = [self.defaultMat]*len(self.geometry)
        elif len(self.idMat) == 0:
            dataMat = [self.defaultMat]*len(self.geometry)
        else:
            dataMat = self.idMat

        objWithMat = [(geo, mat, self.flag) for geo, mat in zip(self.geometry, dataMat)]

        return objWithMat

    @staticmethod
    def createMaterialListForBuildings(wallMaterial, roofMaterial, buildings, commonWallMaterial, commonRoofMaterial):
        materials = []
        if len(wallMaterial) == len(roofMaterial) == len(buildings):
            materials= [[w, r] for w, r in zip(wallMaterial, roofMaterial)]
        elif not roofMaterial and len(wallMaterial) == len(buildings):
            materials= [[w, commonRoofMaterial] for w in wallMaterial]
        elif len(roofMaterial) == len(buildings) and not wallMaterial:
            materials = [[commonWallMaterial, r] for r in roofMaterial]
        else:
            materials = []

        return materials
