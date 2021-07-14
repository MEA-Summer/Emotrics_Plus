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
    
    def __init__(self, shape, left_pupil, right_pupil, points, CalibrationType, CalibrationValue, file_name):
        super(MetricsWindow, self) .__init__()
        self._shape = shape
        self._lefteye = left_pupil
        self._righteye = right_pupil
        self._points = points
        self._CalibrationType = CalibrationType
        self._CalibrationValue = CalibrationValue
        self._fileName = file_name
        
        self.initUI()
        
        
    def initUI(self):
        self.ui = uic.loadUi('Metrics.ui', self)
        
        #Measurements
        MeasurementsLeft, MeasurementsRight, MeasurementsDeviation, MeasurementsPercentual = get_measurements_from_data(self._shape, self._lefteye, self._righteye, self._points, self._CalibrationType, self._CalibrationValue)
        
        #Standard Dash
        
        
        
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
        
        #Commissure Excursion
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsRight.CommissureExcursion, decimals=2)))
        self.resultTable.setItem(3, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsLeft.CommissureExcursion, decimals=2)))
        self.resultTable.setItem(3, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsDeviation.CommissureExcursion, decimals=2)))
        self.resultTable.setItem(3, 2, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsPercentual.CommissureExcursion, decimals=2)))
        self.resultTable.setItem(3, 3, val)
        
        #Smile Angle
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsRight.SmileAngle, decimals=2)))
        self.resultTable.setItem(4, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsLeft.SmileAngle, decimals=2)))
        self.resultTable.setItem(4, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsDeviation.SmileAngle, decimals=2)))
        self.resultTable.setItem(4, 2, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsPercentual.SmileAngle, decimals=2)))
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
        
        #Commisure Height Deviation
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsDeviation.CommisureHeightDeviation, decimals=2)))
        self.resultTable.setItem(6, 2, val)
        dash = QtWidgets.QTableWidgetItem('-')
        self.resultTable.setItem(6, 0, dash)
        dash = QtWidgets.QTableWidgetItem('-')
        self.resultTable.setItem(6, 1, dash)
        dash = QtWidgets.QTableWidgetItem('-')
        self.resultTable.setItem(6, 3, dash)
        
        #Upper Lip Height Deviation
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsDeviation.UpperLipHeightDeviation, decimals=2)))
        self.resultTable.setItem(7, 2, val)
        dash = QtWidgets.QTableWidgetItem('-')
        self.resultTable.setItem(7, 0, dash)
        dash = QtWidgets.QTableWidgetItem('-')
        self.resultTable.setItem(7, 1, dash)
        dash = QtWidgets.QTableWidgetItem('-')
        self.resultTable.setItem(7, 3, dash)
        
        #Lower Lip Height Deviation
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsDeviation.LowerLipHeightDeviation, decimals=2)))
        self.resultTable.setItem(8, 2, val)
        dash = QtWidgets.QTableWidgetItem('-')
        self.resultTable.setItem(8, 0, dash)
        dash = QtWidgets.QTableWidgetItem('-')
        self.resultTable.setItem(8, 1, dash)
        dash = QtWidgets.QTableWidgetItem('-')
        self.resultTable.setItem(8, 3, dash)
        
        #Dental Show
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsRight.DentalShow, decimals=2)))
        self.resultTable.setItem(9, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsLeft.DentalShow, decimals=2)))
        self.resultTable.setItem(9, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsDeviation.DentalShow, decimals=2)))
        self.resultTable.setItem(9, 2, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsPercentual.DentalShow, decimals=2)))
        self.resultTable.setItem(9, 3, val)
        
        #Dental Show Area
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsRight.DentalShowArea, decimals=2)))
        self.resultTable.setItem(10, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsLeft.DentalShowArea, decimals=2)))
        self.resultTable.setItem(10, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsDeviation.DentalShowArea, decimals=2)))
        self.resultTable.setItem(10, 2, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsPercentual.DentalShowArea, decimals=2)))
        self.resultTable.setItem(10, 3, val)
        
        #Eye Area
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsRight.EyeArea, decimals=2)))
        self.resultTable.setItem(11, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsLeft.EyeArea, decimals=2)))
        self.resultTable.setItem(11, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsDeviation.EyeArea, decimals=2)))
        self.resultTable.setItem(11, 2, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(MeasurementsPercentual.EyeArea, decimals=2)))
        self.resultTable.setItem(11, 3, val)
        
        
        
        
        
        
        
        