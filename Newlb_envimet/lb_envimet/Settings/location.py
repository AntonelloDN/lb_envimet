"""
This modules provides location classes.

Classes:
    LocationFromLB
    NewLocation
"""

class LocationFromLB(object):
    """This class read Ladybug Location Data and give you Envimet Location Attributes (Location Name, Latitude, Longitude, Time Zone)
    """

    def __init__(self, location, north = 0):
        self.location = location
        self.north = north

    @property
    def locationAttributes(self):
        # split location string
        locationStr = self.location.split('\n')
        newLocStr = ""

        for line in locationStr:
            if '!' in line:
                line = line.split('!')[0]
                newLocStr  = newLocStr + line.replace(" ", "")
            else:
                newLocStr  = newLocStr + line
        newLocStr = newLocStr.replace(';', "")
        site, locationName, latitude, longitude, timeZone, elevation = newLocStr.split(',')

        # manage timezone
        if float(timeZone) > 0: timeZone = 'UTC' + '+' +str(int(float(timeZone)))
        elif float(timeZone) < 0: timeZone = 'UTC' + '-' +str(int(float(timeZone)))
        else: timeZone = 'GMT'

        # get the results
        return locationName, '{:f}'.format(float(latitude)), '{:f}'.format(float(longitude)), timeZone, self.north


class NewLocation(object):
    """This class create Envimet Location Attributes (Location Name, Latitude, Longitude, Time Zone).
    E.g. Time Zone (+1 or -1)
    """
    def __init__(self, locationName, latitude, longitude, timeZone, north = 0):
        self.locationName = locationName
        self.latitude = latitude
        self.longitude = longitude
        self.timeZone = 'UTC' + timeZone
        self.north = north

        # check latitude and longitude
        try:
            type(float(self.latitude)) and type(float(self.latitude))
        except ValueError, e:
            e = "Please provide a valid float number (es. 41.234)"
            raise ValueError(e)

    def writeLocation(self):
        return self.locationName, self.latitude, self.longitude, self.timeZone
