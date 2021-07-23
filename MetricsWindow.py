# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 13:00:27 2021

@author: lukem
"""


import os
import sys
import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore, uic
from Metrics import get_measurements_from_data

class MetricsWindow(QtWidgets.QMainWindow):
    
    def __init__(self, shape, left_pupil, right_pupil, points, CalibrationType, CalibrationValue, reference_side, file_name):
        super() .__init__()
        self._shape = shape
        self._lefteye = left_pupil
        self._righteye = right_pupil
        self._points = points
        self._CalibrationType = CalibrationType
        self._CalibrationValue = CalibrationValue
        self._reference_side = reference_side
        self._fileName = file_name
        
        self.initUI()
        
        
    def initUI(self):
        self.ui = uic.loadUi('uis/Metrics_Single.ui', self)
        
        #Measurements
        MeasurementsLeft, MeasurementsRight, MeasurementsDeviation, MeasurementsPercentual = get_measurements_from_data(self._shape, self._lefteye, self._righteye, self._points, self._CalibrationType, self._CalibrationValue, self._reference_side)
        
        
        #Brow Height
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsRight.BrowHeight, decimals=2)))
        self.resultTable.setItem(0, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsLeft.BrowHeight, decimals=2)))
        self.resultTable.setItem(0, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsDeviation.BrowHeight, decimals=2)))
        self.resultTable.setItem(0, 2, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsPercentual.BrowHeight, decimals=2)))
        self.resultTable.setItem(0, 3, val)
        
        #Marginal Reflex Distance 1
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsRight.MarginalReflexDistance1, decimals=2)))
        self.resultTable.setItem(1, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsLeft.MarginalReflexDistance1, decimals=2)))
        self.resultTable.setItem(1, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsDeviation.MarginalReflexDistance1, decimals=2)))
        self.resultTable.setItem(1, 2, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsPercentual.MarginalReflexDistance1, decimals=2)))
        self.resultTable.setItem(1, 3, val)
        
        #Marginal Reflex Distance 2
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsRight.MarginalReflexDistance2, decimals=2)))
        self.resultTable.setItem(2, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsLeft.MarginalReflexDistance2, decimals=2)))
        self.resultTable.setItem(2, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsDeviation.MarginalReflexDistance2, decimals=2)))
        self.resultTable.setItem(2, 2, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsPercentual.MarginalReflexDistance2, decimals=2)))
        self.resultTable.setItem(2, 3, val)
        
        #Palpebral Fissure Height
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsRight.PalpebralFissureHeight, decimals=2)))
        self.resultTable.setItem(3, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsLeft.PalpebralFissureHeight, decimals=2)))
        self.resultTable.setItem(3, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsDeviation.PalpebralFissureHeight, decimals=2)))
        self.resultTable.setItem(3, 2, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsPercentual.PalpebralFissureHeight, decimals=2)))
        self.resultTable.setItem(3, 3, val)
        
        #Eye Area
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsRight.EyeArea, decimals=2)))
        self.resultTable.setItem(4, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsLeft.EyeArea, decimals=2)))
        self.resultTable.setItem(4, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsDeviation.EyeArea, decimals=2)))
        self.resultTable.setItem(4, 2, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsPercentual.EyeArea, decimals=2)))
        self.resultTable.setItem(4, 3, val)
        
        #NLF Angle
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsRight.NLF_angle, decimals=2)))
        self.resultTable.setItem(5, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsLeft.NLF_angle, decimals=2)))
        self.resultTable.setItem(5, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsDeviation.NLF_angle, decimals=2)))
        self.resultTable.setItem(5, 2, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsPercentual.NLF_angle, decimals=2)))
        self.resultTable.setItem(5, 3, val)
        
        #Upper Lip Slope
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsRight.UpperLipSlope, decimals=2)))
        self.resultTable.setItem(6, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsLeft.UpperLipSlope, decimals=2)))
        self.resultTable.setItem(6, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsDeviation.UpperLipSlope, decimals=2)))
        self.resultTable.setItem(6, 2, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsPercentual.UpperLipSlope, decimals=2)))
        self.resultTable.setItem(6, 3, val)
        
        #Commisure Height
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsRight.CommisureHeight, decimals=2)))
        self.resultTable.setItem(7, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsLeft.CommisureHeight, decimals=2)))
        self.resultTable.setItem(7, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsDeviation.CommisureHeight, decimals=2)))
        self.resultTable.setItem(7, 2, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsPercentual.CommisureHeight, decimals=2)))
        self.resultTable.setItem(7, 3, val)
        
        #Dental Show
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsRight.InterlabialDistance, decimals=2)))
        self.resultTable.setItem(8, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsLeft.InterlabialDistance, decimals=2)))
        self.resultTable.setItem(8, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsDeviation.InterlabialDistance, decimals=2)))
        self.resultTable.setItem(8, 2, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsPercentual.InterlabialDistance, decimals=2)))
        self.resultTable.setItem(8, 3, val)
        
        #Dental Show Area
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsRight.InterlabialArea_of_the_Hemiface, decimals=2)))
        self.resultTable.setItem(9, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsLeft.InterlabialArea_of_the_Hemiface, decimals=2)))
        self.resultTable.setItem(9, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsDeviation.InterlabialArea_of_the_Hemiface, decimals=2)))
        self.resultTable.setItem(9, 2, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsPercentual.InterlabialArea_of_the_Hemiface, decimals=2)))
        self.resultTable.setItem(9, 3, val)
        
        #Commissure Position
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsRight.CommissurePosition, decimals=2)))
        self.resultTable.setItem(10, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsLeft.CommissurePosition, decimals=2)))
        self.resultTable.setItem(10, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsDeviation.CommissurePosition, decimals=2)))
        self.resultTable.setItem(10, 2, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsPercentual.CommissurePosition, decimals=2)))
        self.resultTable.setItem(10, 3, val)
        
        #Lower Lip Height Deviation
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsRight.LowerLipHeight, decimals=2)))
        self.resultTable.setItem(11, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsLeft.LowerLipHeight, decimals=2)))
        self.resultTable.setItem(11, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsDeviation.LowerLipHeight, decimals=2)))
        self.resultTable.setItem(11, 2, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsPercentual.LowerLipHeight, decimals=2)))
        self.resultTable.setItem(11, 3, val)
        
        #Set up Column headers to show which side is which
        if self._reference_side == 'Left':
            self.resultTable.horizontalHeaderItem(0).setText('Queried (Affected)\nRight Side')
            self.resultTable.horizontalHeaderItem(1).setText('Reference ("Normal")\nLeft Side')
        elif self._reference_side == 'Right':
            self.resultTable.horizontalHeaderItem(0).setText('Reference ("Normal")\nRight Side')
            self.resultTable.horizontalHeaderItem(1).setText('Queried (Affected)\nLeft Side')
        
        #Connecting the selection method to the show the example photos
        # pixmap = QtGui.QPixmap('./Metrics/Default.jpg')
        # self.metricsLabel.setPhoto(pixmap)
        # self.metricsLabel.update_view()
        self.resultTable.selectionModel().selectionChanged.connect(self.get_new_selection)
        
         
    def get_new_selection(self, selected, deselected):
        """This function is for when the user selects a item on the table 
        which will show a picture of an example"""
        for i in selected.indexes():
            if i.row() == 0:
                pixmap = QtGui.QPixmap('./Metrics/Brow_Height.jpg')
                self.metricsLabel.setPhoto(pixmap)
                self.metricsLabel.update_view()
            elif i.row() == 1:
                pixmap = QtGui.QPixmap('./Metrics/Marginal_Reflex_Distance_1.jpg')
                self.metricsLabel.setPhoto(pixmap)
                self.metricsLabel.update_view()
            elif i.row() == 2:
                pixmap = QtGui.QPixmap('./Metrics/Marginal_Reflex_Distance_2.jpg')
                self.metricsLabel.setPhoto(pixmap)
                self.metricsLabel.update_view()
            elif i.row() == 3:
                pixmap = QtGui.QPixmap('./Metrics/palpebral_fissure_width.jpg')
                self.metricsLabel.setPhoto(pixmap)
                self.metricsLabel.update_view()
            elif i.row() == 4:
                pixmap = QtGui.QPixmap('./Metrics/Eye_Area.jpg')
                self.metricsLabel.setPhoto(pixmap)
                self.metricsLabel.update_view()
            elif i.row() == 5:
                pixmap = QtGui.QPixmap('./Metrics/Nasolabial_Fold_Angle.jpg')
                self.metricsLabel.setPhoto(pixmap)
                self.metricsLabel.update_view()
            elif i.row() == 6:
                pixmap = QtGui.QPixmap('./Metrics/upper_lip_slope.jpg')
                self.metricsLabel.setPhoto(pixmap)
                self.metricsLabel.update_view()
            elif i.row() == 7:
                pixmap = QtGui.QPixmap('./Metrics/commissure_height.jpg')
                self.metricsLabel.setPhoto(pixmap)
                self.metricsLabel.update_view()
            elif i.row() == 8:
                pixmap = QtGui.QPixmap('./Metrics/interlabial_distance.jpg')
                self.metricsLabel.setPhoto(pixmap)
                self.metricsLabel.update_view()
            elif i.row() == 9:
                pixmap = QtGui.QPixmap('./Metrics/interlabial_area_of_the_hemiface.jpg')
                self.metricsLabel.setPhoto(pixmap)
                self.metricsLabel.update_view()
            elif i.row() == 10:
                pixmap = QtGui.QPixmap('./Metrics/commissure_position.jpg')
                self.metricsLabel.setPhoto(pixmap)
                self.metricsLabel.update_view()
            elif i.row() == 11:
                pixmap = QtGui.QPixmap('./Metrics/lower_lip_height.jpg')
                self.metricsLabel.setPhoto(pixmap)
                self.metricsLabel.update_view()
            
        
        
        
        