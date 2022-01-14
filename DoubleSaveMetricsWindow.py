import os
import sys

import numpy as np
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QComboBox, QDialog, QFileDialog, QGridLayout,
                             QGroupBox, QLabel, QLineEdit, QPushButton)

from Metrics import *

"""
This window will ask for some additional information and then save the facial measurements in a xls document. 
It will also save a txt file with the position of landmarks and eyes
it has an additional functionality where you can add results to an existing xls document by adding and additional row with the information of the current photo
"""

class MyLineEdit(QLineEdit):
    #I created a custom LineEdit object that will clear its content when selected
    #is used for the Patient ID which is initialized by default to the current date
    def __init__(self, parent=None):
        super(MyLineEdit, self).__init__(parent)

    def mousePressEvent(self, event):
        self.clear()   

        
class DoubleSaveMetricsWindow(QDialog):
    def __init__(self, parent=None, file_name = None, MeasurementsLeft = None, MeasurementsRight = None, MeasurementsDeviation = None, MeasurementsPercentual = None, file_name2 = None, MeasurementsLeft2 = None, MeasurementsRight2 = None, MeasurementsDeviation2 = None, MeasurementsPercentual2 = None):
        super().__init__(parent)
        
        self._NewFile = True    #This variable defines if the user is 
                                #trying to save results in a new file or to a
                                #append results to an existing file
                                
        self._name_of_file = file_name  #this variable stores the name of the 
                                        #file, it won't be modified during 
                                        #execution                        
                                
        self._file_name = file_name     #this variable stores the name of the 
                                        #file to be displayed. It will be 
                                        #modified during execution 
        filename, file_extension = os.path.splitext(self._file_name) 
        delimiter = os.path.sep
        temp=filename.split(delimiter)
        photo_location = temp[0:-1]
        photo_location = delimiter.join(photo_location)
        photo_name=temp[-1]
        
        #measurements
        self._MeasurementsLeft = MeasurementsLeft
        self._MeasurementsRight = MeasurementsRight
        self._MeasurementsDeviation = MeasurementsDeviation
        self._MeasurementsPercentual = MeasurementsPercentual
        
        self._file_name = photo_name  #path + file name
        self._photo_location = photo_location
        self._ID = photo_name #unique identifier
        self._prevspost = '' #pre-treatment vs post-treatment
        self._surgery = '' #type of surgery
        self._expression = '' #type of expression
        self._other = '' #additional comments
        self._file_to_save = '' #file to add data 


        #Photo 2 Variables
        self._name_of_file2 = file_name2  #this variable stores the name of the 
                                        #file, it won't be modified during 
                                        #execution                        
                                
        self._file_name2 = file_name2    #this variable stores the name of the 
                                        #file to be displayed. It will be 
                                        #modified during execution 
        filename2, file_extension2 = os.path.splitext(self._file_name2) 
        delimiter = os.path.sep
        temp2=filename2.split(delimiter)
        photo_location2 = temp2[0:-1]
        photo_location2 = delimiter.join(photo_location2)
        photo_name2=temp2[-1]
        
        #measurements
        self._MeasurementsLeft2 = MeasurementsLeft2
        self._MeasurementsRight2 = MeasurementsRight2
        self._MeasurementsDeviation2 = MeasurementsDeviation2
        self._MeasurementsPercentual2 = MeasurementsPercentual2
        
        self._file_name2 = photo_name2  #path + file name
        self._photo_location2 = photo_location2
        self._ID2 = photo_name2 #unique identifier
        self._prevspost2 = '' #pre-treatment vs post-treatment
        self._surgery2 = '' #type of surgery
        self._expression2 = '' #type of expression
        self._other2 = '' #additional comments

        self.getOneSideComparison()

        self.initUI()
        
    def initUI(self):
        
        self.setWindowTitle('Save')
        if os.name == 'posix': #is a mac or linux
            scriptDir = os.path.dirname(sys.argv[0])
        else: #is a  windows 
            scriptDir = os.getcwd()
            
        self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'include' +os.path.sep +'icon_color'+ os.path.sep + 'save_icon.ico'))
        
        self.main_Widget = QtWidgets.QWidget(self)
        
        spacerh = QtWidgets.QWidget(self)
        spacerh.setFixedSize(10,0)
        
        spacerv = QtWidgets.QWidget(self)
        spacerv.setFixedSize(0,10)
        
        
        
        
        
  
        file = QLabel('File Name:')
        self._file = QLineEdit(self)
        self._file.setText(self._file_name)
        
        self.SelectFolderButton = QPushButton('Select &Folder', self)
        self.SelectFolderButton.setFixedWidth(150)
        self.SelectFolderButton.clicked.connect(self.SelectFolder)
        self._SelectFolder = QLineEdit(self)
        self._SelectFolder.setText(self._photo_location) 
        self._SelectFolder.setFixedWidth(350)
        
        
        NewFileBox = QGroupBox('Create new File')
        NewFileBoxLayout = QGridLayout()
        NewFileBoxLayout.addWidget(file,0,0)
        NewFileBoxLayout.addWidget(spacerh,0,1)
        NewFileBoxLayout.addWidget(self._file,0,2)
        NewFileBoxLayout.addWidget(spacerv,1,0)
        NewFileBoxLayout.addWidget(self.SelectFolderButton,2,0)
        NewFileBoxLayout.addWidget(self._SelectFolder,2,2)
        NewFileBox.setLayout(NewFileBoxLayout)
        
        
        SelectFileButton = QPushButton('&Select File', self)
        SelectFileButton.setFixedWidth(150)
        SelectFileButton.clicked.connect(self.SelectFile)       
        self._SelectFile = QLineEdit(self)
        self._SelectFile.setText(self._file_to_save) 
        
        
        AppendFileBox = QGroupBox('Append to Existing File')
        AppendFileBoxLayout = QGridLayout()
        AppendFileBoxLayout.addWidget(SelectFileButton,0,0)
        AppendFileBoxLayout.addWidget(spacerh,0,1)
        AppendFileBoxLayout.addWidget(self._SelectFile,0,2)
        AppendFileBox.setLayout(AppendFileBoxLayout)
        
        
        Identifier = QLabel('Photo Identifier:')
        Identifier.setFixedWidth(120)
        self._Identifier = QLineEdit(self)
        self._Identifier.setText(self._ID)
        
        PrevsPost = QLabel('Pre or Post Procedure:')
        self._PrevsPost = QComboBox()
        self._PrevsPost.setFixedWidth(110)
        self._PrevsPost.addItem('')
        self._PrevsPost.addItem('Pre - Procedure')
        self._PrevsPost.addItem('Post - Procedure')


        SurgeryType = QLabel('Procedure:')
        self._SurgeryType = QLineEdit(self)
        self._SurgeryType.setText(self._surgery)
        
        ExpressionType = QLabel('Expression:')
        self._ExpressionType = QLineEdit(self)
        self._ExpressionType.setText(self._expression)
        
        AddtitionalComments = QLabel('Addtitional Comments:')
        self._AddtitionalComments = QLineEdit(self)
        self._AddtitionalComments.setText(self._other)       
        
        AdditionalInformationBox = QGroupBox('Optional Information')
        AdditionalInformationBoxLayout = QGridLayout()
        
        AdditionalInformationBoxLayout.addWidget(Identifier,0,0)
        AdditionalInformationBoxLayout.addWidget(spacerh,0,1)
        AdditionalInformationBoxLayout.addWidget(self._Identifier,0,2)
        
        AdditionalInformationBoxLayout.addWidget(spacerv,1,0)
        
        AdditionalInformationBoxLayout.addWidget(PrevsPost,2,0)
        AdditionalInformationBoxLayout.addWidget(self._PrevsPost,2,2)
        
        #AdditionalInformationBoxLayout.addWidget(spacerv,3,0) 
        
        AdditionalInformationBoxLayout.addWidget(SurgeryType,4,0)
        AdditionalInformationBoxLayout.addWidget(self._SurgeryType,4,2)
        
        #AdditionalInformationBoxLayout.addWidget(spacerv,5,0) 

        AdditionalInformationBoxLayout.addWidget(ExpressionType,6,0)
        AdditionalInformationBoxLayout.addWidget(self._ExpressionType,6,2)
        
        #AdditionalInformationBoxLayout.addWidget(spacerv,7,0)         

        AdditionalInformationBoxLayout.addWidget(AddtitionalComments,8,0)
        AdditionalInformationBoxLayout.addWidget(self._AddtitionalComments,8,2)    
        
        AdditionalInformationBox.setLayout(AdditionalInformationBoxLayout)
        
        
        
        SaveButton = QPushButton('&Save', self)
        SaveButton.setFixedWidth(150)
        SaveButton.clicked.connect(self.Save)
        
        CancelButton = QPushButton('&Cancel', self)
        CancelButton.setFixedWidth(150)
        CancelButton.clicked.connect(self.Cancel)
        
        
        ButtonBox = QGroupBox('')
        ButtonBoxLayout = QGridLayout()
        ButtonBoxLayout.addWidget(SaveButton,0,0,QtCore.Qt.AlignCenter)
        ButtonBoxLayout.addWidget(spacerh,0,1)
        ButtonBoxLayout.addWidget(CancelButton,0,2,QtCore.Qt.AlignCenter)
        ButtonBox.setLayout(ButtonBoxLayout)
        ButtonBox.setStyleSheet("QGroupBox {  border: 0px solid gray;}");
        
        layout = QGridLayout()

        layout.addWidget(NewFileBox,0,0,2,2)
        
        layout.addWidget(spacerv,1,0)
        
        layout.addWidget(AppendFileBox,2,0,1,2)
               
        
        layout.addWidget(AdditionalInformationBox,4,0,8,2)        
        
        layout.addWidget(ButtonBox,17,0,1,2)
        
        self.setLayout(layout)
        
        #self.show()

    def getOneSideComparison(self):
        self._MeasurementLeftComparison = FaceMeasurementsSide()
        self._MeasurementRightComparison = FaceMeasurementsSide()
        self._MeasurementLeftPercentComparison = FaceMeasurementsSide()
        self._MeasurementRightPercentComparison = FaceMeasurementsSide()

        #Left Side Comparison
        self._MeasurementLeftComparison.BrowHeight = abs(self._MeasurementsLeft2.BrowHeight - self._MeasurementsLeft.BrowHeight)
        self._MeasurementLeftComparison.MarginalReflexDistance1 = abs(self._MeasurementsLeft2.MarginalReflexDistance1 - self._MeasurementsLeft.MarginalReflexDistance1)
        self._MeasurementLeftComparison.MarginalReflexDistance2 = abs(self._MeasurementsLeft2.MarginalReflexDistance2 - self._MeasurementsLeft.MarginalReflexDistance2)
        self._MeasurementLeftComparison.PalpebralFissureHeight = abs(self._MeasurementsLeft2.PalpebralFissureHeight - self._MeasurementsLeft.PalpebralFissureHeight)
        self._MeasurementLeftComparison.EyeArea = abs(self._MeasurementsLeft2.EyeArea - self._MeasurementsLeft.EyeArea)
        self._MeasurementLeftComparison.NLF_angle = abs(self._MeasurementsLeft2.NLF_angle - self._MeasurementsLeft.NLF_angle)
        self._MeasurementLeftComparison.UpperLipSlope = abs(self._MeasurementsLeft2.UpperLipSlope - self._MeasurementsLeft.UpperLipSlope)
        self._MeasurementLeftComparison.CommisureHeight = abs(self._MeasurementsLeft2.CommisureHeight - self._MeasurementsLeft.CommisureHeight)
        self._MeasurementLeftComparison.InterlabialDistance = abs(self._MeasurementsLeft2.InterlabialDistance - self._MeasurementsLeft.InterlabialDistance)
        self._MeasurementLeftComparison.InterlabialArea_of_the_Hemiface = abs(self._MeasurementsLeft2.InterlabialArea_of_the_Hemiface - self._MeasurementsLeft.InterlabialArea_of_the_Hemiface)
        self._MeasurementLeftComparison.CommissurePosition = abs(self._MeasurementsLeft2.CommissurePosition - self._MeasurementsLeft.CommissurePosition)
        self._MeasurementLeftComparison.LowerLipHeight = abs(self._MeasurementsLeft2.LowerLipHeight - self._MeasurementsLeft.LowerLipHeight)

        #Right Side Comparison
        self._MeasurementRightComparison.BrowHeight = abs(self._MeasurementsRight2.BrowHeight - self._MeasurementsRight.BrowHeight)
        self._MeasurementRightComparison.MarginalReflexDistance1 = abs(self._MeasurementsRight2.MarginalReflexDistance1 - self._MeasurementsRight.MarginalReflexDistance1)
        self._MeasurementRightComparison.MarginalReflexDistance2 = abs(self._MeasurementsRight2.MarginalReflexDistance2 - self._MeasurementsRight.MarginalReflexDistance2)
        self._MeasurementRightComparison.PalpebralFissureHeight = abs(self._MeasurementsRight2.PalpebralFissureHeight - self._MeasurementsRight.PalpebralFissureHeight)
        self._MeasurementRightComparison.EyeArea = abs(self._MeasurementsRight2.EyeArea - self._MeasurementsRight.EyeArea)
        self._MeasurementRightComparison.NLF_angle = abs(self._MeasurementsRight2.NLF_angle - self._MeasurementsRight.NLF_angle)
        self._MeasurementRightComparison.UpperLipSlope = abs(self._MeasurementsRight2.UpperLipSlope - self._MeasurementsRight.UpperLipSlope)
        self._MeasurementRightComparison.CommisureHeight = abs(self._MeasurementsRight2.CommisureHeight - self._MeasurementsRight.CommisureHeight)
        self._MeasurementRightComparison.InterlabialDistance = abs(self._MeasurementsRight2.InterlabialDistance - self._MeasurementsRight.InterlabialDistance)
        self._MeasurementRightComparison.InterlabialArea_of_the_Hemiface = abs(self._MeasurementsRight2.InterlabialArea_of_the_Hemiface - self._MeasurementsRight.InterlabialArea_of_the_Hemiface)
        self._MeasurementRightComparison.CommissurePosition = abs(self._MeasurementsRight2.CommissurePosition - self._MeasurementsRight.CommissurePosition)
        self._MeasurementRightComparison.LowerLipHeight = abs(self._MeasurementsRight2.LowerLipHeight - self._MeasurementsRight.LowerLipHeight)


        #Left Side Percent Comparison
        #BrowHeight
        self._MeasurementLeftPercentComparison.BrowHeight = abs(self._MeasurementsLeft2.BrowHeight - self._MeasurementsLeft.BrowHeight)*100/self._MeasurementsLeft.BrowHeight
        #MarginalReflexDistance1
        if self._MeasurementsLeft.MarginalReflexDistance1 > 0:
            self._MeasurementLeftPercentComparison.MarginalReflexDistance1 = abs(self._MeasurementsLeft2.MarginalReflexDistance1 - self._MeasurementsLeft.MarginalReflexDistance1)*100/self._MeasurementsLeft.MarginalReflexDistance1
        else:
            self._MeasurementLeftPercentComparison.MarginalReflexDistance1 = 0
        #MarginalReflexDistance2
        if self._MeasurementsLeft.MarginalReflexDistance2 > 0:
            self._MeasurementLeftPercentComparison.MarginalReflexDistance2 = abs(self._MeasurementsLeft2.MarginalReflexDistance2 - self._MeasurementsLeft.MarginalReflexDistance2)*100/self._MeasurementsLeft.MarginalReflexDistance2
        else:
            self._MeasurementLeftPercentComparison.MarginalReflexDistance2 = 0
        #PalpebralFissureHeight
        if self._MeasurementsLeft.PalpebralFissureHeight > 0:
            self._MeasurementLeftPercentComparison.PalpebralFissureHeight = abs(self._MeasurementsLeft2.PalpebralFissureHeight - self._MeasurementsLeft.PalpebralFissureHeight)*100/self._MeasurementsLeft.PalpebralFissureHeight
        else:
            self._MeasurementLeftPercentComparison.PalpebralFissureHeight = 0
        #EyeArea
        if self._MeasurementsLeft.EyeArea > 0:
            self._MeasurementLeftPercentComparison.EyeArea = abs(self._MeasurementsLeft2.EyeArea - self._MeasurementsLeft.EyeArea)*100/self._MeasurementsLeft.EyeArea
        else:
            self._MeasurementLeftPercentComparison.EyeArea = 0
        #NLF_angle
        if self._MeasurementsLeft.NLF_angle > 0:
            self._MeasurementLeftPercentComparison.NLF_angle = abs(self._MeasurementsLeft2.NLF_angle - self._MeasurementsLeft.NLF_angle)*100/self._MeasurementsLeft.NLF_angle
        else:
            self._MeasurementLeftPercentComparison.NLF_angle = 0
        #UpperLipSlope
        if self._MeasurementsLeft.UpperLipSlope > 0:
            self._MeasurementLeftPercentComparison.UpperLipSlope = abs(self._MeasurementsLeft2.UpperLipSlope - self._MeasurementsLeft.UpperLipSlope)*100/self._MeasurementsLeft.UpperLipSlope
        else:
            self._MeasurementLeftPercentComparison.UpperLipSlope = 0
        #CommisureHeight
        if self._MeasurementsLeft.CommisureHeight > 0:    
            self._MeasurementLeftPercentComparison.CommisureHeight = abs(self._MeasurementsLeft2.CommisureHeight - self._MeasurementsLeft.CommisureHeight)*100/self._MeasurementsLeft.CommisureHeight
        else:
            self._MeasurementLeftPercentComparison.CommisureHeight = 0
        #InterlabialDistance
        if self._MeasurementsLeft.InterlabialDistance > 0:
            self._MeasurementLeftPercentComparison.InterlabialDistance = abs(self._MeasurementsLeft2.InterlabialDistance - self._MeasurementsLeft.InterlabialDistance)*100/self._MeasurementsLeft.InterlabialDistance
        else:
            self._MeasurementLeftPercentComparison.InterlabialDistance = 0
        #InterlabialArea_of_the_Hemiface
        if self._MeasurementsLeft.InterlabialArea_of_the_Hemiface > 0:
            self._MeasurementLeftPercentComparison.InterlabialArea_of_the_Hemiface = abs(self._MeasurementsLeft2.InterlabialArea_of_the_Hemiface - self._MeasurementsLeft.InterlabialArea_of_the_Hemiface)*100/self._MeasurementsLeft.InterlabialArea_of_the_Hemiface
        else:
            self._MeasurementLeftPercentComparison.InterlabialArea_of_the_Hemiface = 0
        #CommissurePosition
        self._MeasurementLeftPercentComparison.CommissurePosition = abs(self._MeasurementsLeft2.CommissurePosition - self._MeasurementsLeft.CommissurePosition)*100/self._MeasurementsLeft.CommissurePosition
        #LowerLipHeight
        self._MeasurementLeftPercentComparison.LowerLipHeight = abs(self._MeasurementsLeft2.LowerLipHeight - self._MeasurementsLeft.LowerLipHeight)*100/self._MeasurementsLeft.LowerLipHeight


        #Right Side Percent Comparison
        #BrowHeight
        self._MeasurementRightPercentComparison.BrowHeight = abs(self._MeasurementsRight2.BrowHeight - self._MeasurementsRight.BrowHeight)*100/self._MeasurementsRight.BrowHeight
        #MarginalReflexDistance1
        if self._MeasurementsRight.MarginalReflexDistance1 > 0:
            self._MeasurementRightPercentComparison.MarginalReflexDistance1 = abs(self._MeasurementsRight2.MarginalReflexDistance1 - self._MeasurementsRight.MarginalReflexDistance1)*100/self._MeasurementsRight.MarginalReflexDistance1
        else:
            self._MeasurementRightPercentComparison.MarginalReflexDistance1 = 0
        #MarginalReflexDistance2
        if self._MeasurementsRight.MarginalReflexDistance2 > 0:
            self._MeasurementRightPercentComparison.MarginalReflexDistance2 = abs(self._MeasurementsRight2.MarginalReflexDistance2 - self._MeasurementsRight.MarginalReflexDistance2)*100/self._MeasurementsRight.MarginalReflexDistance2
        else:
            self._MeasurementRightPercentComparison.MarginalReflexDistance2 = 0
        #PalpebralFissureHeight
        if self._MeasurementsRight.PalpebralFissureHeight > 0:
            self._MeasurementRightPercentComparison.PalpebralFissureHeight = abs(self._MeasurementsRight2.PalpebralFissureHeight - self._MeasurementsRight.PalpebralFissureHeight)*100/self._MeasurementsRight.PalpebralFissureHeight
        else:
            self._MeasurementRightPercentComparison.PalpebralFissureHeight = 0
        #EyeArea
        if self._MeasurementsRight.EyeArea > 0:
            self._MeasurementRightPercentComparison.EyeArea = abs(self._MeasurementsRight2.EyeArea - self._MeasurementsRight.EyeArea)*100/self._MeasurementsRight.EyeArea
        else:
            self._MeasurementRightPercentComparison.EyeArea = 0
        #NLF_angle
        if self._MeasurementsRight.NLF_angle > 0:
            self._MeasurementRightPercentComparison.NLF_angle = abs(self._MeasurementsRight2.NLF_angle - self._MeasurementsRight.NLF_angle)*100/self._MeasurementsRight.NLF_angle
        else:
            self._MeasurementRightPercentComparison.NLF_angle = 0
        #UpperLipSlope
        if self._MeasurementsRight.UpperLipSlope > 0:
            self._MeasurementRightPercentComparison.UpperLipSlope = abs(self._MeasurementsRight2.UpperLipSlope - self._MeasurementsRight.UpperLipSlope)*100/self._MeasurementsRight.UpperLipSlope
        else:
            self._MeasurementRightPercentComparison.UpperLipSlope = 0
        #CommisureHeight
        if self._MeasurementsRight.CommisureHeight > 0:    
            self._MeasurementRightPercentComparison.CommisureHeight = abs(self._MeasurementsRight2.CommisureHeight - self._MeasurementsRight.CommisureHeight)*100/self._MeasurementsRight.CommisureHeight
        else:
            self._MeasurementRightPercentComparison.CommisureHeight = 0
        #InterlabialDistance
        if self._MeasurementsRight.InterlabialDistance > 0:
            self._MeasurementRightPercentComparison.InterlabialDistance = abs(self._MeasurementsRight2.InterlabialDistance - self._MeasurementsRight.InterlabialDistance)*100/self._MeasurementsRight.InterlabialDistance
        else:
            self._MeasurementRightPercentComparison.InterlabialDistance = 0
        #InterlabialArea_of_the_Hemiface
        if self._MeasurementsRight.InterlabialArea_of_the_Hemiface > 0:
            self._MeasurementRightPercentComparison.InterlabialArea_of_the_Hemiface = abs(self._MeasurementsRight2.InterlabialArea_of_the_Hemiface - self._MeasurementsRight.InterlabialArea_of_the_Hemiface)*100/self._MeasurementsRight.InterlabialArea_of_the_Hemiface
        else:
            self._MeasurementRightPercentComparison.InterlabialArea_of_the_Hemiface = 0
        #CommissurePosition
        self._MeasurementRightPercentComparison.CommissurePosition = abs(self._MeasurementsRight2.CommissurePosition - self._MeasurementsRight.CommissurePosition)*100/self._MeasurementsRight.CommissurePosition
        #LowerLipHeight
        self._MeasurementRightPercentComparison.LowerLipHeight = abs(self._MeasurementsRight2.LowerLipHeight - self._MeasurementsRight.LowerLipHeight)*100/self._MeasurementsRight.LowerLipHeight



    def Cancel(self):
        self.close()  

        
    def SelectFolder(self):
        name = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select directory')
        
        if not name:
            pass
        else:
            
            if not self._SelectFolder.isEnabled():        
                self._file.setEnabled(True)
                self._SelectFolder.setEnabled(True)
                self._SelectFile.setText('') 
                
                filename, file_extension = os.path.splitext(self._name_of_file) 
                delimiter = os.path.sep
                temp=filename.split(delimiter)
                photo_name=temp[-1]
                self._file.setText(photo_name)

            name = os.path.normpath(name)
            self._photo_location = name
            self._SelectFolder.setText(self._photo_location)                        
            self._NewFile = True  #a new file will be created
            self.update()
        
    def SelectFile(self):
        name,_ = QtWidgets.QFileDialog.getOpenFileName(
                self,'Load File',
                '',"Excel Spreadsheet  (*.xls *.xlsx)")
        
        if not name:
            pass
        else:
            name = os.path.normpath(name)
            delimiter = os.path.sep
            filename, file_extension = os.path.splitext(name)           
            temp=filename.split(delimiter)
            photo_location = temp[0:-1]
            photo_location = delimiter.join(photo_location)
            photo_name=temp[-1]
            
            self._file_name = photo_name
            
            self._file.setText(self._file_name)
            self._file.setEnabled(False)
            
            
            

            self._photo_location = photo_location
            self._SelectFolder.setText(self._photo_location) 
            self._SelectFolder.setEnabled(False)
            #self.SelectFolderButton.setEnabled(False)
            
            self._file_to_save = name
            self._SelectFile.setText(self._file_to_save) 
            self._NewFile = False  #data will be appended to an exisiting file
            self.update()


            
    def Save(self):
        
        #Creates Fill for first sheet
        number_of_measurements = 12
        Columns = ['Right','Left','Deviation (absolute)','Deviation (percent)']
        Columns = Columns * number_of_measurements
        
        Columns.insert(0,'')
        Columns.insert(0,'')
        Columns.insert(0,'')
        Columns.insert(0,'')
        
        Columns.append('')
        
        temp = ['Brow Height', 'Marginal Reflex Distance 1', 'Marginal Reflex Distance 2', 
            'Palpebral Fissure Height', 'Eye Area', 'NLF Angle',
            'Upper Lip Slope', 'Commisure Height', 'Interlabial Distance',
            'Interlabial Area of the Hemiface','Commissure Position','Lower Lip Height']
        number_of_repetitions=4
        Header = [item for item in temp for i in range(number_of_repetitions)]
        
        Header.insert(0,'Expression')
        Header.insert(0,'Procedure')
        Header.insert(0,'Pre vs Post Procedure')
        Header.insert(0,'Unique Identifier')
        
        Header.append('Additional Comments')
        
        #measurements
        elements = ['BH', 'MRD1', 'MRD2', 'PFH', 'EA', 'NA', 'ULS', 'CH', 'ID', 'IAH', 'CP', 'LLH']
        BH = np.array([[self._MeasurementsRight.BrowHeight,self._MeasurementsLeft.BrowHeight,self._MeasurementsDeviation.BrowHeight,self._MeasurementsPercentual.BrowHeight]],dtype=object)
        MRD1 = np.array([[self._MeasurementsRight.MarginalReflexDistance1, self._MeasurementsLeft.MarginalReflexDistance1,self._MeasurementsDeviation.MarginalReflexDistance1,self._MeasurementsPercentual.MarginalReflexDistance1]], dtype=object)
        MRD2 = np.array([[self._MeasurementsRight.MarginalReflexDistance2, self._MeasurementsLeft.MarginalReflexDistance2,self._MeasurementsDeviation.MarginalReflexDistance2,self._MeasurementsPercentual.MarginalReflexDistance2]],dtype=object)
        PFH = np.array([[self._MeasurementsRight.PalpebralFissureHeight, self._MeasurementsLeft.PalpebralFissureHeight,self._MeasurementsDeviation.PalpebralFissureHeight,self._MeasurementsPercentual.PalpebralFissureHeight]],dtype=object)
        EA = np.array([[self._MeasurementsRight.EyeArea, self._MeasurementsLeft.EyeArea,self._MeasurementsDeviation.EyeArea,self._MeasurementsPercentual.EyeArea]],dtype=object)
        NA = np.array([[self._MeasurementsRight.NLF_angle, self._MeasurementsLeft.NLF_angle,self._MeasurementsDeviation.NLF_angle,0]],dtype=object)
        ULS = np.array([[self._MeasurementsRight.UpperLipSlope, self._MeasurementsLeft.UpperLipSlope,self._MeasurementsDeviation.UpperLipSlope,0]],dtype=object)
        CH = np.array([[self._MeasurementsRight.CommisureHeight, self._MeasurementsLeft.CommisureHeight,self._MeasurementsDeviation.CommisureHeight,0]],dtype=object)
        ID = np.array([[self._MeasurementsRight.InterlabialDistance, self._MeasurementsLeft.InterlabialDistance,self._MeasurementsDeviation.InterlabialDistance,0]],dtype=object)
        IAH = np.array([[self._MeasurementsRight.InterlabialArea_of_the_Hemiface,self._MeasurementsLeft.InterlabialArea_of_the_Hemiface,self._MeasurementsDeviation.InterlabialArea_of_the_Hemiface,0]],dtype=object)
        CP = np.array([[self._MeasurementsRight.CommissurePosition,self._MeasurementsLeft.CommissurePosition,self._MeasurementsDeviation.CommissurePosition,0]],dtype=object)
        LLH = np.array([[self._MeasurementsRight.LowerLipHeight,self._MeasurementsLeft.LowerLipHeight,self._MeasurementsDeviation.LowerLipHeight,0]],dtype=object)
        
        UI = np.array([[self._Identifier.text()]],dtype = object)
        PvsP = np.array([[str(self._PrevsPost.currentText())]],dtype = object)
        PC = np.array([[self._SurgeryType.text()]],dtype = object)
        EX = np.array([[self._ExpressionType.text()]],dtype = object)
        AD = np.array([[self._AddtitionalComments.text()]],dtype = object)

        fill= UI
        fill= np.append(fill, PvsP, axis = 1)
        fill= np.append(fill, PC, axis = 1)
        fill= np.append(fill, EX, axis = 1)
        for i in elements:
                fill = np.append(fill, eval(i), axis = 1)
        
        fill= np.append(fill, AD, axis = 1)

        #Creates Fill for second sheet
        number_of_measurements = 12
        Columns2 = ['Right','Left','Deviation (absolute)','Deviation (percent)']
        Columns2 = Columns2 * number_of_measurements
        
        Columns2.insert(0,'')
        Columns2.insert(0,'')
        Columns2.insert(0,'')
        Columns2.insert(0,'')
        
        Columns2.append('')
        
        temp2 = ['Brow Height', 'Marginal Reflex Distance 1', 'Marginal Reflex Distance 2', 
            'Palpebral Fissure Height', 'Eye Area', 'NLF Angle',
            'Upper Lip Slope', 'Commisure Height', 'Interlabial Distance',
            'Interlabial Area of the Hemiface','Commissure Position','Lower Lip Height']
        number_of_repetitions=4
        Header2 = [item for item in temp2 for i in range(number_of_repetitions)]
        
        Header2.insert(0,'Expression')
        Header2.insert(0,'Procedure')
        Header2.insert(0,'Pre vs Post Procedure')
        Header2.insert(0,'Unique Identifier')
        
        Header2.append('Additional Comments')
        
        #measurements
        elements = ['BH', 'MRD1', 'MRD2', 'PFH', 'EA', 'NA', 'ULS', 'CH', 'ID', 'IAH', 'CP', 'LLH']
        BH = np.array([[self._MeasurementsRight2.BrowHeight,self._MeasurementsLeft2.BrowHeight,self._MeasurementsDeviation2.BrowHeight,self._MeasurementsPercentual2.BrowHeight]],dtype=object)
        MRD1 = np.array([[self._MeasurementsRight2.MarginalReflexDistance1, self._MeasurementsLeft2.MarginalReflexDistance1,self._MeasurementsDeviation2.MarginalReflexDistance1,self._MeasurementsPercentual2.MarginalReflexDistance1]], dtype=object)
        MRD2 = np.array([[self._MeasurementsRight2.MarginalReflexDistance2, self._MeasurementsLeft2.MarginalReflexDistance2,self._MeasurementsDeviation2.MarginalReflexDistance2,self._MeasurementsPercentual2.MarginalReflexDistance2]],dtype=object)
        PFH = np.array([[self._MeasurementsRight2.PalpebralFissureHeight, self._MeasurementsLeft2.PalpebralFissureHeight,self._MeasurementsDeviation2.PalpebralFissureHeight,self._MeasurementsPercentual2.PalpebralFissureHeight]],dtype=object)
        EA = np.array([[self._MeasurementsRight2.EyeArea, self._MeasurementsLeft2.EyeArea,self._MeasurementsDeviation2.EyeArea,self._MeasurementsPercentual2.EyeArea]],dtype=object)
        NA = np.array([[self._MeasurementsRight2.NLF_angle, self._MeasurementsLeft2.NLF_angle,self._MeasurementsDeviation2.NLF_angle,0]],dtype=object)
        ULS = np.array([[self._MeasurementsRight2.UpperLipSlope, self._MeasurementsLeft2.UpperLipSlope,self._MeasurementsDeviation2.UpperLipSlope,0]],dtype=object)
        CH = np.array([[self._MeasurementsRight2.CommisureHeight, self._MeasurementsLeft2.CommisureHeight,self._MeasurementsDeviation2.CommisureHeight,0]],dtype=object)
        ID = np.array([[self._MeasurementsRight2.InterlabialDistance, self._MeasurementsLeft2.InterlabialDistance,self._MeasurementsDeviation2.InterlabialDistance,0]],dtype=object)
        IAH = np.array([[self._MeasurementsRight2.InterlabialArea_of_the_Hemiface,self._MeasurementsLeft2.InterlabialArea_of_the_Hemiface,self._MeasurementsDeviation2.InterlabialArea_of_the_Hemiface,0]],dtype=object)
        CP = np.array([[self._MeasurementsRight2.CommissurePosition,self._MeasurementsLeft2.CommissurePosition,self._MeasurementsDeviation2.CommissurePosition,0]],dtype=object)
        LLH = np.array([[self._MeasurementsRight2.LowerLipHeight,self._MeasurementsLeft2.LowerLipHeight,self._MeasurementsDeviation2.LowerLipHeight,0]],dtype=object)
        
        UI = np.array([[self._Identifier.text()]],dtype = object)
        PvsP = np.array([[str(self._PrevsPost.currentText())]],dtype = object)
        PC = np.array([[self._SurgeryType.text()]],dtype = object)
        EX = np.array([[self._ExpressionType.text()]],dtype = object)
        AD = np.array([[self._AddtitionalComments.text()]],dtype = object)

        fill2= UI
        fill2= np.append(fill2, PvsP, axis = 1)
        fill2= np.append(fill2, PC, axis = 1)
        fill2= np.append(fill2, EX, axis = 1)
        for i in elements:
                fill2 = np.append(fill2, eval(i), axis = 1)
        
        fill2= np.append(fill2, AD, axis = 1)

         #Creates Fill for Third sheet
        number_of_measurements = 12
        Columns3 = ['Right Absolute Difference', 'Right Percent Difference', 'Left Absolute Difference', 'Left Percent Difference''Left']
        Columns3 = Columns3 * number_of_measurements
        
        Columns3.insert(0,'')
        Columns3.insert(0,'')
        Columns3.insert(0,'')
        Columns3.insert(0,'')
        
        Columns3.append('')
        
        temp3 = ['Brow Height', 'Marginal Reflex Distance 1', 'Marginal Reflex Distance 2', 
            'Palpebral Fissure Height', 'Eye Area', 'NLF Angle',
            'Upper Lip Slope', 'Commisure Height', 'Interlabial Distance',
            'Interlabial Area of the Hemiface','Commissure Position','Lower Lip Height']
        number_of_repetitions=4
        Header3 = [item for item in temp3 for i in range(number_of_repetitions)]
        
        Header3.insert(0,'Expression')
        Header3.insert(0,'Procedure')
        Header3.insert(0,'Pre vs Post Procedure')
        Header3.insert(0,'Unique Identifier')
        
        Header3.append('Additional Comments')
        
        #measurements
        elements = ['BH', 'MRD1', 'MRD2', 'PFH', 'EA', 'NA', 'ULS', 'CH', 'ID', 'IAH', 'CP', 'LLH']
        BH = np.array([[self._MeasurementRightComparison.BrowHeight,self._MeasurementRightPercentComparison.BrowHeight,self._MeasurementLeftPercentComparison.BrowHeight,self._MeasurementLeftPercentComparison.BrowHeight]],dtype=object)
        MRD1 = np.array([[self._MeasurementRightComparison.MarginalReflexDistance1, self._MeasurementRightPercentComparison.MarginalReflexDistance1,self._MeasurementLeftPercentComparison.MarginalReflexDistance1,self._MeasurementLeftPercentComparison.MarginalReflexDistance1]], dtype=object)
        MRD2 = np.array([[self._MeasurementRightComparison.MarginalReflexDistance2, self._MeasurementRightPercentComparison.MarginalReflexDistance2,self._MeasurementLeftPercentComparison.MarginalReflexDistance2,self._MeasurementLeftPercentComparison.MarginalReflexDistance2]],dtype=object)
        PFH = np.array([[self._MeasurementRightComparison.PalpebralFissureHeight, self._MeasurementRightPercentComparison.PalpebralFissureHeight,self._MeasurementLeftPercentComparison.PalpebralFissureHeight,self._MeasurementLeftPercentComparison.PalpebralFissureHeight]],dtype=object)
        EA = np.array([[self._MeasurementRightComparison.EyeArea, self._MeasurementRightPercentComparison.EyeArea,self._MeasurementLeftPercentComparison.EyeArea,self._MeasurementLeftPercentComparison.EyeArea]],dtype=object)
        NA = np.array([[self._MeasurementRightComparison.NLF_angle, 0,self._MeasurementLeftPercentComparison.NLF_angle, 0]],dtype=object)
        ULS = np.array([[self._MeasurementRightComparison.UpperLipSlope, 0, self._MeasurementLeftPercentComparison.UpperLipSlope, 0]],dtype=object)
        CH = np.array([[self._MeasurementRightComparison.CommisureHeight, 0, self._MeasurementLeftPercentComparison.CommisureHeight, 0]],dtype=object)
        ID = np.array([[self._MeasurementRightComparison.InterlabialDistance, 0, self._MeasurementLeftPercentComparison.InterlabialDistance, 0]],dtype=object)
        IAH = np.array([[self._MeasurementRightComparison.InterlabialArea_of_the_Hemiface, 0, self._MeasurementLeftPercentComparison.InterlabialArea_of_the_Hemiface, 0]],dtype=object)
        CP = np.array([[self._MeasurementRightComparison.CommissurePosition, 0, self._MeasurementLeftPercentComparison.CommissurePosition, 0]],dtype=object)
        LLH = np.array([[self._MeasurementRightComparison.LowerLipHeight, 0, self._MeasurementLeftPercentComparison.LowerLipHeight, 0]],dtype=object)
        
        UI = np.array([[self._Identifier.text()]],dtype = object)
        PvsP = np.array([[str(self._PrevsPost.currentText())]],dtype = object)
        PC = np.array([[self._SurgeryType.text()]],dtype = object)
        EX = np.array([[self._ExpressionType.text()]],dtype = object)
        AD = np.array([[self._AddtitionalComments.text()]],dtype = object)

        fill3= UI
        fill3= np.append(fill3, PvsP, axis = 1)
        fill3= np.append(fill3, PC, axis = 1)
        fill3= np.append(fill3, EX, axis = 1)
        for i in elements:
                fill3 = np.append(fill3, eval(i), axis = 1)
        
        fill3= np.append(fill3, AD, axis = 1)
        
        if self._NewFile: #the user wants to create a new file
            #Sheet 1 Data           
            filename, file_extension = os.path.splitext(self._name_of_file ) 
            delimiter = os.path.sep
            temp=filename.split(delimiter)
            photo_name=temp[-1] + file_extension
            file_no_ext = os.path.join(str(self._SelectFolder.text()),str(self._file.text()))  
            xlsxfilename = file_no_ext+'.xlsx'
            Index = [photo_name]
            #create data frame using data
            df = pd.DataFrame(fill, index = Index, columns = Columns)
            df.columns = pd.MultiIndex.from_tuples(list(zip(Header,df.columns)))

            #Sheet 2 Data
            filename2, file_extension2 = os.path.splitext(self._name_of_file2 ) 
            delimiter2 = os.path.sep
            temp2=filename2.split(delimiter2)
            photo_name2=temp[-1] + file_extension2
            Index2 = [photo_name2]
            #create data frame using data
            df2 = pd.DataFrame(fill2, index = Index2, columns = Columns2)
            df2.columns = pd.MultiIndex.from_tuples(list(zip(Header2,df2.columns)))

            #Sheet 3 Data
            Index3 = [photo_name] #reuse first photo as index
            #create data frame using data
            df3 = pd.DataFrame(fill3, index = Index3, columns = Columns3)
            df3.columns = pd.MultiIndex.from_tuples(list(zip(Header3,df3.columns)))

            #write data frame to an excel file
            if os.path.isfile(xlsxfilename):
                overwriteQuestion = QtWidgets.QMessageBox
                overwriteBox = overwriteQuestion.question(self, 'File Already exist', 
                    'File already exist.\nWould you like to write over existing file?', 
                    overwriteQuestion.Yes | overwriteQuestion.No) 
                if overwriteBox == overwriteQuestion.Yes:
                    try:
                        os.remove(xlsxfilename)
                        with pd.ExcelWriter(xlsxfilename, engine='xlsxwriter') as writer:
                            df.to_excel(writer, sheet_name='Sheet1', index = True)
                            df2.to_excel(writer, sheet_name='Sheet2', index = True)
                            df3.to_excel(writer, sheet_name='Sheet3', index = True)
                        # #adjust the size of each column to fit the text
                        # worksheet = writer.sheets['Sheet1']
                        # for i in range(0, 55):
                        #     worksheet.autoFitColumn(i,0,2)

                        writer.save()
                        self.close()
                    except Exception as e:
                        QtWidgets.QMessageBox.information(self, 'Error', 
                            f'Error in saving metrics.\nMake sure the existing file is closed\nto allow new file to be saved.',#\nError message: {e}', 
                            QtWidgets.QMessageBox.Ok)
            else:
                try:
                    with pd.ExcelWriter(xlsxfilename, engine='xlsxwriter') as writer:
                            df.to_excel(writer, sheet_name='Sheet1', index = True)
                            df2.to_excel(writer, sheet_name='Sheet2', index = True)
                            df3.to_excel(writer, sheet_name='Sheet3', index = True)
                    # #adjust the size of each column to fit the text
                    # worksheet = writer.sheets['Sheet1']
                    # for i in range(0, 55):
                    #     worksheet.autoFitColumn(i,0,2)

                    writer.save()
                    self.close()
                except Exception as e:
                    QtWidgets.QMessageBox.information(self, 'Error', 
                            f'Error in saving metrics.',#\nError Message: {e}', 
                            QtWidgets.QMessageBox.Ok)
                    
        else: #the user wants to append to an existing file
            
            try:
                #Sheet 1
                filename, file_extension = os.path.splitext(self._name_of_file ) 
                delimiter = os.path.sep
                temp=filename.split(delimiter)
                photo_name=temp[-1] + file_extension
                #create data frame with new ata
                Index = [photo_name]
                df = pd.DataFrame(fill, index = Index, columns = Columns)
                df.columns = pd.MultiIndex.from_tuples(list(zip(Header,df.columns)))
                #load data from file and arrange its columns to fit the template
                old_df = pd.read_excel(str(self._SelectFile.text()), sheet_name="Sheet1",header=[0, 1], index_col=0, engine='openpyxl')
                old_df.columns = pd.MultiIndex.from_tuples(df.columns)
                #concatenate old and new data frame
                Frames = [old_df, df]
                results = pd.concat(Frames, axis=0)
                

                #Sheet 2
                filename2, file_extension2 = os.path.splitext(self._name_of_file ) 
                delimiter2 = os.path.sep
                temp2=filename2.split(delimiter2)
                photo_name2=temp2[-1] + file_extension2
                #create data frame with new ata
                Index2 = [photo_name2]
                df2 = pd.DataFrame(fill2, index = Index2, columns = Columns2)
                df2.columns = pd.MultiIndex.from_tuples(list(zip(Header2,df2.columns)))
                #load data from file and arrange its columns to fit the template
                old_df2 = pd.read_excel(str(self._SelectFile.text()), sheet_name="Sheet2",header=[0, 1], index_col=0, engine='openpyxl')
                old_df2.columns = pd.MultiIndex.from_tuples(df2.columns)
                #concatenate old and new data frame
                Frames2 = [old_df2, df2]
                results2 = pd.concat(Frames2, axis=0)
                

                #Sheet 3
                #create data frame with new ata
                Index = [photo_name]
                df3 = pd.DataFrame(fill3, index = Index, columns = Columns3)
                df3.columns = pd.MultiIndex.from_tuples(list(zip(Header3,df3.columns)))
                #load data from file and arrange its columns to fit the template
                old_df3 = pd.read_excel(str(self._SelectFile.text()), sheet_name="Sheet3",header=[0, 1], index_col=0, engine='openpyxl')
                old_df3.columns = pd.MultiIndex.from_tuples(df3.columns)
                #concatenate old and new data frame
                Frames3 = [old_df3, df3]
                results3 = pd.concat(Frames3, axis=0)

                #write results in selected file
                with pd.ExcelWriter(str(self._SelectFile.text()), engine='xlsxwriter') as writer:
                            results.to_excel(writer, sheet_name='Sheet1', index = True)
                            results2.to_excel(writer, sheet_name='Sheet2', index = True)
                            results3.to_excel(writer, sheet_name='Sheet3', index = True)
               
                writer.save()
                self.close() 

            except Exception as e:
                        QtWidgets.QMessageBox.information(self, 'Error', 
                            f'Error in saving metrics.\nMake sure the existing file is closed\nto allow new file to be saved.',#\nError message: {e}', 
                            QtWidgets.QMessageBox.Ok)
            
        