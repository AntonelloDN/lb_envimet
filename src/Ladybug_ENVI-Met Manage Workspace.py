# ENVI-Met Manage Workspace
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
Use this component to create a Workspace folder.
-
Connect "folder" output to ENVI-Met Spaces.
-
Provided by Ladybug 0.0.65
    
    Args:
        _workspaceFolder: Main folder where you have to save an Envimet project.
        _projectName: Name of Envimet project folder where you have to save:
        1) EnviMet geometry file (*.INX)
        2) Configuration file (*.SIM)
        ENVImetInstallFolder_: Optional folder path for ENVImet4 installation folder.
    Returns:
        readMe!: ...
        envimetFolder: Envimet project folder. Connect it to "_folder" input of ENVI-Met Spaces
"""

ghenv.Component.Name = "Ladybug_ENVI-Met Manage Workspace"
ghenv.Component.NickName = 'ENVI-MetManageWorkspace'
ghenv.Component.Message = 'VER 0.0.65\nJUL_28_2017'
ghenv.Component.IconDisplayMode = ghenv.Component.IconDisplayMode.application
ghenv.Component.Category = "Ladybug"
ghenv.Component.SubCategory = "7 | WIP"
#compatibleLBVersion = VER 0.0.59\nFEB_01_2015
try: ghenv.Component.AdditionalHelpFromDocStrings = "1"
except: pass


import Grasshopper.Kernel as gh
import sys
import os
##################LB ENVI_MET###################
userPath = os.getenv("APPDATA")
path = os.path.join(userPath, "lb_envimet")
sys.path.append(path)
from envimetStuff import makeMainFolder
################################################


def checkInputs(workspaceFolder):
    if workspaceFolder == None:
        return False
    elif workspaceFolder:
        return True


def findENVI_MET():
    appdata = os.getenv("APPDATA")
    directory = os.path.join(appdata[:3], "ENVImet4\sys.basedata\\")
    
    if ENVImetInstallFolder_:
        directory = os.path.join(ENVImetInstallFolder_, 'sys.basedata\\')
    
    try:
        if os.listdir(directory):
            print("Good to go!")
            return directory
    except:
        w = gh.GH_RuntimeMessageLevel.Warning
        message = "Envimet Main Folder not found!"
        ghenv.Component.AddRuntimeMessage(w, message)
        return -1


def main():
    
    # default value
    if _projectName_ == None: projectFolderName = 'LBDATA'
    else: projectFolderName = _projectName_
    
    
    mainDirectory = findENVI_MET()
    if mainDirectory != -1:
        
        # run envimet core
        myFile = makeMainFolder.WorkspaceFolderLB(_workspaceFolder, projectFolderName)
        fullFolder = myFile.writeWorkspaceFolder(mainDirectory)
        
        return fullFolder


# check and run component
if checkInputs(_workspaceFolder):
    result = main()
    if result != -1:
        envimetFolder = result
else:
    w = gh.GH_RuntimeMessageLevel.Warning
    message = "Please provide _workspaceFolder input."
    ghenv.Component.AddRuntimeMessage(w, message)