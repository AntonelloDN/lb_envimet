# ENVI-Met Layer Profile Material
#
# Ladybug: A Plugin for Environmental Analysis (GPL) started by Mostapha Sadeghipour Roudsari
# 
# This file is part of Ladybug.
# 
# Copyright (c) 2013-2017, Antonello Di Nunzio <antonellodinunzio@gmail.com> 
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
This component let you create layers that you need for profile materials.
-
Provided by Ladybug 0.0.64
    
    Args:
        _layer1_ : from 0cm to 1cm under.
        _layer2_ : from 1cm to 2cm under.
        _layer3_ : from 2cm to 3cm under.
        _layer4_ : from 3cm to 4cm under.
        _layer5_ : from 4cm to 6cm under.
        _layer6_ : from 6cm to 8cm under.
        _layer7_ : from 8cm to 10cm under.
        _layer8_ : from 10cm to 20cm under.
        _layer9_ : from 20cm to 30cm under.
        _layer10_ : from 30cm to 40cm under.
        _layer11_ : from 40cm to 50cm under.
        _layer12_ : from 50cm to 100cm under.
        _layer13_ : from 100cm to 150cm under.
        _layer14_ : from 150cm to 200cm under.
        _layer15_ : from 200cm to 250cm under.
        _layer16_ : from 250cm to 300cm under.
        _layer17_ : from 300cm to 350cm under.
        _layer18_ : from 350cm to 400cm under.
        _layer19_ : from 400cm to 450cm under.
    Returns:
        readMe!: ...
        profileId: ENVI-Met soil ID of User Material. Connect it to "Ladybug_ENVI-Met Soil".
"""

ghenv.Component.Name = "Ladybug_ENVI-Met Layer Profile Material"
ghenv.Component.NickName = 'ENVI-MetLayerProfileMaterial'
ghenv.Component.Message = 'VER 0.0.64\nFEB_26_2017'
ghenv.Component.IconDisplayMode = ghenv.Component.IconDisplayMode.application
ghenv.Component.Category = "Ladybug"
ghenv.Component.SubCategory = "7 | WIP"
#compatibleLBVersion = VER 0.0.62\nJUN_07_2016
try: ghenv.Component.AdditionalHelpFromDocStrings = "1"
except: pass



if not _layer1_:
    _layer1_ = "LE"
if not _layer2_:
    _layer2_ = "LE"
if not _layer3_:
    _layer3_ = "LE"
if not _layer4_:
    _layer4_ = "LE"
if not _layer5_:
    _layer5_ = "LE"
if not _layer6_:
    _layer6_ = "LE"
if not _layer7_:
    _layer7_ = "LE"
if not _layer8_:
    _layer8_ = "LE"
if not _layer9_:
    _layer9_ = "LE"
if not _layer10_:
    _layer10_ = "LE"
if not _layer11_:
    _layer11_ = "LE"
if not _layer12_:
    _layer12_ = "LE"
if not _layer13_:
    _layer13_ = "LE"
if not _layer14_:
    _layer14_ = "LE"
if not _layer15_:
    _layer15_ = "LE"
if not _layer16_:
    _layer16_ = "LE"
if not _layer17_:
    _layer17_ = "LE"
if not _layer18_:
    _layer18_ = "LE"
if not _layer19_:
    _layer19_ = "LE"

layers = [_layer1_,_layer2_,_layer3_,_layer4_,_layer5_,_layer6_,_layer7_,_layer8_,_layer9_,_layer10_,_layer11_,_layer12_,_layer13_,_layer14_,_layer15_,_layer16_,_layer17_,_layer18_,_layer19_]