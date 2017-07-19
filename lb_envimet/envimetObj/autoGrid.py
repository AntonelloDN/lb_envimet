# Abraham Yezioro <ayez@ar.technion.ac.il>, Antonello Di Nunzio  <antonellodinunzio@gmail.com>


import Rhino as rc
import scriptcontext as sc

class setGrid(object):

    def __init__(self, ENVImetVersion, telescope=None):
        self.nestingGrids  = 0
        self.zGrids = 15
        self.dimX = 3.0
        self.dimY = 3.0
        self.dimZ = 3.0
        self.startTelescopeHeight = 5.0
        self.extLeftXgrid = 2
        self.extRightXgrid = 2
        self.extUpYgrid = 2
        self.extDownYgrid = 2
        self.telescope = telescope

        # set Envimet maxZGrid
        if ENVImetVersion == 0: maxZGrid = 40
        elif ENVImetVersion == 1: maxZGrid = 35
        elif ENVImetVersion == 2: maxZGrid = 25

        # set telescope
        if self.telescope == None:
            self.zGrids += 4


    def gZmethod(self, buildings):
        distLeft    = self.extLeftXgrid  * self.dimX
        distRight   = self.extRightXgrid * self.dimX
        distUp      = self.extUpYgrid    * self.dimY
        distDown    = self.extDownYgrid  * self.dimY

        minX = minY        = 10000000
        maxX = maxY = maxZ = -10000000
        for iBuild in buildings:
            BB1 = iBuild.GetBoundingBox(True)
            if minX > BB1.Min.X: minX = BB1.Min.X
            if maxX < BB1.Max.X: maxX = BB1.Max.X
            if minY > BB1.Min.Y: minY = BB1.Min.Y
            if maxY < BB1.Max.Y: maxY = BB1.Max.Y
            if maxZ < BB1.Max.Z: maxZ = BB1.Max.Z

        #Geometry BoundingBox limits NETO
        minX = minX - distLeft
        minY = minY - distDown
        maxX = maxX + distRight
        maxY = maxY + distUp
        reqHeight = maxZ * 2                # Required height -- Twice the heighest building

        domX = maxX - minX
        domY = maxY - minY
        numX = int(domX / self.dimX)
        numY = int(domY / self.dimY)

        maxX = minX + (numX * self.dimX)      # Reccalculate maxX/Y just for the bounding box fit the grid size/length
        maxY = minY + (numY * self.dimY)

        dimZ = self.dimZ
        gZ = []
        firstGrid = dimZ / 5
        for i in range(0, int(self.zGrids) + 1):
            if self.telescope == None:
                if i <= 5:  # In ENVImet the lowest cell is splitted into 5 sub-cells
                    if i == 0:
                        grid = 0
                    elif i == 1:
                        grid = firstGrid / 2
                    else:
                        grid = (i * firstGrid) - (firstGrid / 2)
                else:
                    grid = ((i - 4) * dimZ) - (dimZ / 2)
                gZ.append(grid)
            else:   # For Telescope vertical grid calculation
                if i == 0:
                    grid = 0
                elif i == 1 or grid <= self.startTelescopeHeight:
                    grid = (i * dimZ) - (dimZ / 2)
                else:
                    g1 = grid
                    gz = dimZ
                    dimZ = dimZ + (dimZ * self.telescope/ 100 )
                    grid = grid + (dimZ + gz) / 2
                gZ.append(grid)

        return numX, numY, gZ, minX, minY, maxX, maxY



    def buildingGrid(self, flag, buildings, numX, numY, gZ, minX, minY):

        buildingFlagAndNr, nestedLayers = [], []
        # XY Grid
        for index, building in enumerate(buildings):
            layers = []
            for k in range(1, len(gZ)):
                columns = []
                for j in range(numY + 1):
                    rows = []
                    for i in range(numX + 1):
                        point = rc.Geometry.Point3d((i * self.dimX) + minX, (j * self.dimY) + minY, gZ[k])

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
