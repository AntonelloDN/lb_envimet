# ENVI-Met Start Date
#
# Ladybug: A Plugin for Environmental Analysis (GPL) started by Mostapha Sadeghipour Roudsari
# 
# This file is part of Ladybug.
# 
# Copyright (c) 2013-2018, Antonello Di Nunzio <antonellodinunzio@gmail.com> 
# Ladybug is free software; you can redistribute it and/or modify 
# it under the terms of the GNU General Public License as published 
# by the Free Software Foundation; either version 3 of the License, 
# or (at your option) any later version. 
# 
# Ladybug is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Ladybug; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>


"""
Create the start date of the SIM file.
-
The SIM file is the configuration file for a simulation in ENVI_MET.
-
Provided by Ladybug 0.0.65
    
    Args:
        _year_: A number that represents the year.
        _month_: A number between 1 and 12 that represents the month of the year.
        _day_: A number between 1 and 31 that represents the day of the year.
        _hour_: A number between 1 and 23 that represents the hour of the day.
        _minutes_: A number between 1 and 59 that represents the minutes.
        _seconds_: A number between 1 and 59 that represents the seconds.
    Returns:
        readMe!: ...
        date: Complete timestamp that lb_envimet uses for settings.
"""

ghenv.Component.Name = "Ladybug_ENVI-Met Start Date"
ghenv.Component.NickName = 'ENVI-MetStartDate'
ghenv.Component.Message = 'VER 0.0.65\nJUL_28_2017'
ghenv.Component.IconDisplayMode = ghenv.Component.IconDisplayMode.application
ghenv.Component.Category = "Ladybug"
ghenv.Component.SubCategory = "7 | WIP"
#compatibleLBVersion = VER 0.0.59\nFEB_01_2015
try: ghenv.Component.AdditionalHelpFromDocStrings = "1"
except: pass

from datetime import datetime
import Grasshopper.Kernel as gh

if _year_: year = _year_
else: year = 2017
if _month_: month = _month_
else: month = 6
if _day_: day = _day_
else: day = 23
if _hour_: hour = _hour_
else: hour = 7
if _minutes_: minutes = _minutes_
else: minutes = 0
if _seconds_: seconds = _seconds_
else: seconds = 0

try:
    date = datetime(year, month, day, hour, minutes, seconds)
except ValueError, e:
    w = gh.GH_RuntimeMessageLevel.Warning
    ghenv.Component.AddRuntimeMessage(w, str(e))