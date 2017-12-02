"""
This modules provides material classes.

Classes:
    SetMaterials
"""
from random import randint

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


class createSoilMaterial(object):
    def __init__(self, Id, description, versiegelung, ns, nfc, nwilt, matpot, hydro_lf, volumenw, b, waerme_lf, Group):
        self.name = 'SOIL'
        self.id = Id
        self.description = description
        self.versiegelung = versiegelung
        self.ns = ns
        self.nfc = nfc
        self.nwilt = nwilt
        self.matpot = matpot
        self.hydro_lf = hydro_lf
        self.volumenw = volumenw
        self.b = b
        self.waerme_lf = waerme_lf
        self.Group = Group
        self.Color = str(randint(1000000, 9999999))
        self.AddValue1 = '0.00000'
        self.AddValue2 = '0.00000'


class createProfileMaterial(object):
    def __init__(self, Id, description, z0_Length, soilprofil, Albedo, Emiss, ExtraID, Irrigated, Group):
        self.name = 'PROFILE'
        self.id = Id
        self.description = description
        self.z0_Length = z0_Length
        self.soilprofil = soilprofil
        self.Albedo = Albedo
        self.Emiss = Emiss
        self.ExtraID = ExtraID
        self.Irrigated = Irrigated
        self.Group = Group
        self.Color = str(randint(1000000, 9999999))
        self.AddValue1 = '0.00000'
        self.AddValue2 = '0.00000'
