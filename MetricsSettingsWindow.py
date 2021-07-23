# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 17:19:52 2021

@author: lukem
"""

import os
import sys
from PyQt5 import QtWidgets, QtCore, QtGui, uic


class MetricsSettingsWindow(QtWidgets.QMainWindow):
    
    Calibration_Type = QtCore.pyqtSignal(object)
    Calibration_Value = QtCore.pyqtSignal(object)
    
    def __init__(self, CalibrationType, CalibrationValue):
        super() .__init__()
        #Input variables
        self.CalibrationType = CalibrationType
        self.CalibrationValue = CalibrationValue
        #Status variables
        
        
        self.initUI()
        
        
    def initUI(self):
        self.ui = uic.loadUi('uis/metrics_settings.ui', self)
        
        self.doneButton.clicked.connect(self.done)
        self.cancelButton.clicked.connect(self.cancel)
        
        self.calibrationTypeComboBox.addItem('Iris')
        self.calibrationTypeComboBox.addItem('Custom')
        self.calibrationTypeComboBox.setCurrentText(self.CalibrationType)
        self.calibrationTypeComboBox.activated[str].connect(self.changeCalibrationType)
        
        validator = QtGui.QDoubleValidator(self)
        self.irisDiameterLineEdit.setValidator(validator)
        validator = QtGui.QDoubleValidator(self)
        self.calibrationValueLineEdit.setValidator(validator)
        
        
        if self.CalibrationType == 'Iris':
            self.irisDiameterLineEdit.setText(str(self.CalibrationValue))
            self.irisDiameterLineEdit.setEnabled(True)
            self.calibrationValueLineEdit.setEnabled(False)
        else:
            self.calibrationValueLineEdit.setText(str(self.CalibrationValue))
            self.irisDiameterLineEdit.setEnabled(False)
            self.calibrationValueLineEdit.setEnabled(True)
    
            
    def changeCalibrationType(self, CalibrationType):
        self.CalibrationType = CalibrationType
        if self.CalibrationType == 'Iris':
            self.irisDiameterLineEdit.setEnabled(True)
            self.calibrationValueLineEdit.setEnabled(False)
        else:
            self.irisDiameterLineEdit.setEnabled(False)
            self.calibrationValueLineEdit.setEnabled(True)
        
    def done(self):
       if self.CalibrationType == 'Iris':
           try:
               self.CalibrationValue = float(self.irisDiameterLineEdit.text())
               if self.CalibrationValue <= 0:
                   QtWidgets.QMessageBox.information(self, 'Error', 
                            'The value entered is not a proper Iris Diameter', 
                            QtWidgets.QMessageBox.Ok)
           except:
               QtWidgets.QMessageBox.information(self, 'Error', 
                            'No value was entered.\nPlease enter a value before pressing done or press cancel to leave the settings unchanged.', 
                            QtWidgets.QMessageBox.Ok)
               return
       else:
           try:
               self.CalibrationValue = float(self.calibrationValueLineEdit.text())
               if self.CalibrationValue <= 0:
                   QtWidgets.QMessageBox.information(self, 'Error', 
                            'The value entered is not a proper Calibration Value', 
                            QtWidgets.QMessageBox.Ok)
           except:
               QtWidgets.QMessageBox.information(self, 'Error', 
                            'No value was entered.\nPlease enter a value before pressing done or press cancel to leave the settings unchanged.', 
                            QtWidgets.QMessageBox.Ok)
               return
       self.Calibration_Type.emit(self.CalibrationType)
       self.Calibration_Value.emit(self.CalibrationValue)
       self.close()
            
       
    def cancel(self):
        self.close()