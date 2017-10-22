"""
This modules is for settings
"""


class mainSettings(object):
    """This class is for the main Setting.
    """
    def __init__(self, projectName, fileName, SIMname, startSimulation, startSimulationTime, totalTime, windSpeed, windDirection, roughness, initialTemperature, specificHumidity, relativeHumidity, outputIntervalMainFile, outputIntervalText, includeNestingGrids):
	self.projectName = projectName
	self.fileName = fileName
	self.SIMname = SIMname
	self.startSimulation = startSimulation
	self.startSimulationTime = startSimulationTime
	self.totalTime = totalTime
	self.windSpeed = windSpeed
	self.windDirection = windDirection
	self.roughness = roughness
	self.initialTemperature = initialTemperature
	self.specificHumidity = specificHumidity
	self.relativeHumidity = relativeHumidity
	self.outputIntervalMainFile = outputIntervalMainFile
	self.outputIntervalText = outputIntervalText
	self.includeNestingGrids = includeNestingGrids

    @property
    def mainSettingsText(self):
	mainDataText = """%---- ENVI-met V4 main configuration file --------------------------
%---- generated with ProjectWizard  ----------------------------------
Fileversion                                  =4.0
JobID                                        =Simulation
% Main data .........................................................
Name for Simulation (Text):                  =Simulation {0}
Area Input File to be used                   ={1}
Filebase name for Output (Text):             ={2}
Output Directory:                            =
Start Simulation at Day (DD.MM.YYYY):        ={3}
Start Simulation at Time (HH:MM:SS):         ={4}
Total Simulation Time in Hours:              ={5}
Wind Speed in 10 m ab. Ground [m/s]          ={6}
Wind Direction (0:N..90:E..180:S..270:W..)   ={7}
Roughness Length z0 at Reference Point [m]   ={8}
Initial Temperature Atmosphere [K]           ={9}
Specific Humidity in 2500 m [g Water/kg air] ={10}
Relative Humidity in 2m [%]                  ={11}
% End main data .....................................................
[OUTPUTTIMING]_____________________________________
Output interval main files (min)              ={12}
Output interval text output files (min)          ={13}
Include Nesting Grids in Output (0:n,1:y)        ={14}""".format(self.projectName, self.fileName, self.SIMname, self.startSimulation, self.startSimulationTime, self.totalTime, self.windSpeed, self.windDirection, self.roughness, self.initialTemperature, self.specificHumidity, self.relativeHumidity, self.outputIntervalMainFile, self.outputIntervalText, self.includeNestingGrids)

        return mainDataText


class solarAdjustSettings(object):

    def __init__(self, value):
	self.value = value

    @property
    def solarAdjustSettingsText(self):
	solarAdjText = """[SOLARADJUST] _____________________________________
Factor of shortwave adjustment (0.5 to 1.5) ={}""".format(self.value)

        return solarAdjText


class cloudSettings(object):
    def __init__(self, lowValue, middleValue, highValue):
	self.lowValue = lowValue
	self.middleValue = middleValue
	self.highValue = highValue

    @property
    def cloudSettingsText(self):
	cloudText = """[CLOUDS] _____________________________________
Fraction of LOW clouds (x/8)                ={0}
Fraction of MIDDLE clouds (x/8)             ={1}
Fraction of HIGH clouds (x/8)               ={2}""".format(self.lowValue, self.middleValue, self.highValue)

        return cloudText


class timingSettings(object):
    def __init__(self, dataSurface, wind, radiation, plant):
	self.dataSurface = dataSurface
	self.wind = wind
	self.radiation = radiation
	self.plant = plant

    @property
    def timingSettingsText(self):
	timingText = """[TIMING]_____________________________________
Update Surface Data each  ? sec              ={0}
Update Wind field each ? sec                 ={1}
Update Radiation and Shadows each ? sec      ={2}
Update Plant Data each ? sec                 ={3}""".format(self.dataSurface, self.wind, self.radiation, self.plant)

        return timingText


class timestepsSettings(object):
    def __init__(self, sunheightDelta0, sunheightDelta1, timeStepInterval1, timeStepInterval2, timeStepInterval3):
	self.sunheightDelta0 = sunheightDelta0
	self.sunheightDelta1 = sunheightDelta1
	self.timeStepInterval1 = timeStepInterval1
	self.timeStepInterval2 = timeStepInterval2
	self.timeStepInterval3 = timeStepInterval3

    @property
    def timestepsSettingsText(self):
	timestepsText = """[TIMESTEPS] ____________________________________
Sun height for switching dt(0) -> dt(1)       ={0}
Sun height for switching dt(1) -> dt(2)       ={1}
Time step (s) for interval 1 dt(0)            ={2}
Time step (s) for interval 2 dt(1)            ={3}
Time step (s) for interval 3 dt(2)            ={4}""".format(self.sunheightDelta0, self.sunheightDelta1, self.timeStepInterval1, self.timeStepInterval2, self.timeStepInterval3)

        return timestepsText


class soilDataSettings(object):
    def __init__(self, initialTempUpperLayer, initialTempMiddleLayer, initialTempDeepLayer, RHupperLayer, RHmiddleLayer, RHdeepLayer):
	self.initialTempUpperLayer = initialTempUpperLayer
	self.initialTempMiddleLayer = initialTempMiddleLayer
	self.initialTempDeepLayer = initialTempDeepLayer
	self.RHupperLayer = RHupperLayer
	self.RHmiddleLayer = RHmiddleLayer
	self.RHdeepLayer = RHdeepLayer

    @property
    def soilDataSettingsText(self):
	soilDataText = """[SOILDATA] ______________________________________
Initial Temperature Upper Layer (0-20 cm)   [K]={0}
Initial Temperature Middle Layer (20-50 cm) [K]={1}
Initial Temperature Deep Layer (below 50 cm)[K]={2}
Relative Humidity Upper Layer (0-20 cm)        ={3}
Relative Humidity Middle Layer (20-50 cm)      ={4}
Relative Humidity Deep Layer (below 50 cm)     ={5}""".format(self.initialTempUpperLayer, self.initialTempMiddleLayer, self.initialTempDeepLayer, self.RHupperLayer, self.RHmiddleLayer, self.RHdeepLayer)

        return soilDataText



class plantModelSettings(object):
    def __init__(self, stomata, CO2concentration):
	self.stomata = stomata
	self.CO2concentration = CO2concentration

    @property
    def plantModelSettingsText(self):
	plantModelText = """[PLANTMODEL] _______________________________________
Stomata res. approach (1:Deardorff, 2:A-gs)  ={0}
Background CO2 concentration [ppm]           ={1}""".format(self.stomata, self.CO2concentration)

        return plantModelText


class simpleForceSettings(object):
    def __init__(self, dryBulbTemperature, relativeHumidity):
	self.dryBulbTemperature = dryBulbTemperature
	self.relativeHumidity = relativeHumidity

    @property
    def simpleForceSettingsText(self):

	lines1 = "[SIMPLEFORCE] _____________________________________"
	lines2 = []
	for i in range(len(self.dryBulbTemperature)):
		line = "Hour {0}h [Temp, rH] = {1}, {2}".format("%02d" % i, self.dryBulbTemperature[i] + 273.15, self.relativeHumidity[i])
		lines2.append(line)

	lines2 = '\n'.join(lines2)

	simpleForceText = lines1 + '\n' + lines2

	return simpleForceText
