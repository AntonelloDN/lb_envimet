"""
This modules provide a class for Envimet Workspace

Classes:
    WorkspaceFolderLB
"""


import os
import time
import socket
import datetime


class WorkspaceFolderLB(object):
    """This class is for WorkspaceFolder
    """

    def __init__(self, workspaceFolder, projectFolderName):
        self.workspaceFolder = workspaceFolder
        self.projectFolderName = projectFolderName
        self.fileNamePrj = socket.gethostname().upper() + '.projects'
        self.iniFileName = 'envimet.ini'
        self.worspaceName = 'workspace.infoX'
        self.projectName = 'project.infoX'
        self.edbFileName = 'projectdatabase.edb'


    def writeWorkspaceFolder(self, mainDirectory):

        # date
        timeTxt = datetime.datetime.now()
        timeTxt = str(timeTxt)[:-7]


        # file folder
        fullFolder = self.workspaceFolder + '\\'+ self.projectFolderName

        if not os.path.exists(fullFolder):
            os.makedirs(fullFolder)


        # PROJECTS
        prjFile = os.path.join(mainDirectory, self.fileNamePrj)

        with open(prjFile, 'w') as f:
            f.write(fullFolder)


        # INI and workspace file
        iniFile = os.path.join(mainDirectory, self.iniFileName)
        workspaceXml = os.path.join(mainDirectory, self.worspaceName)
        projectFileInFolder = os.path.join(fullFolder, self.projectName)
        edbFileInFolder = os.path.join(fullFolder, self.edbFileName)


        with open(iniFile, 'w') as f:
            f.writelines('[projectdir]' + '\n')
            f.writelines('dir' + '=' + self.workspaceFolder)


        with open(workspaceXml, 'w') as f:
            text = ['<ENVI-MET_Datafile>', '<Header>', '<filetype>workspacepointer</filetype>',
                    '<version>6811715</version>', '<revisiondate>{}</revisiondate>'.format(timeTxt),
                    '<remark></remark>', '<encryptionlevel>5150044</encryptionlevel>', '</Header>',
                    '<current_workspace>', r'<absolute_path> {} </absolute_path>'.format(self.workspaceFolder),
                    '<last_active> {} </last_active>'.format(self.projectFolderName), '</current_workspace>', '</ENVI-MET_Datafile>']
            f.write('\n'.join(text))


        with open(projectFileInFolder, 'w') as f:
            text = ['<ENVI-MET_Datafile>', '<Header>', '<filetype>infoX ENVI-met Project Description File</filetype>',
                    '<version>4240697</version>', '<revisiondate>{}</revisiondate>'.format(timeTxt),
                    '<remark></remark>', '<encryptionlevel>5220697</encryptionlevel>', '</Header>',
                    '<project_description>', '<name> {} </name>'.format(self.projectFolderName),
                    '<description>  </description>', '<useProjectDB> 1 </useProjectDB>', '</project_description>', '</ENVI-MET_Datafile>']
            f.write('\n'.join(text))

		if not os.path.isfile(edbFileInFolder):
			with open(edbFileInFolder, 'w') as f:
				text = ['<ENVI-MET_Datafile>', '<Header>', '<filetype>DATA</filetype>',
						'<version>1</version>', '<revisiondate>{}</revisiondate>'.format(timeTxt),
						'<remark>Envi-Data</remark>', '<encryptionlevel>1701377</encryptionlevel>',
						'</Header>', '</ENVI-MET_Datafile>']
				f.write('\n'.join(text))


        return fullFolder
