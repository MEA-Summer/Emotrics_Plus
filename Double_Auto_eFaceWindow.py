import sys

import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtGui import QDoubleValidator, QValidator
from torch._C import has_openmp

from Compute_eFace import *
from MplWidget import MplWidget
from Patient import Patient


class DoubleValidator(QDoubleValidator):
    def __init__(self, *__args):
        super().__init__(*__args)

    def validate(self, p_str, p_int):

        if not p_str:
            return QValidator.Intermediate, p_str, p_int

        if p_str != '.':
            if self.bottom() <= float(p_str) <= self.top():
                return QValidator.Acceptable, p_str, p_int
            else:
                return QValidator.Invalid, p_str, p_int
        else:
            return QValidator.Invalid, p_str, p_int

class Double_Auto_eFaceWindow(QtWidgets.QMainWindow):
    
    def __init__(self, shape, left_pupil, right_pupil, points, shape2, left_pupil2, right_pupil2, points2, CalibrationType, CalibrationValue, reference_side, expression):
        super() .__init__()
        #Sets input to variables
        self._Patient = Patient()
        self._Patient._Resting._shape = shape
        self._Patient._Resting._lefteye = left_pupil
        self._Patient._Resting._righteye = right_pupil
        self._Patient._Resting._points = points
        self._shape2 = shape2
        self._lefteye2 = left_pupil2
        self._righteye2 = right_pupil2
        self._points2 = points2
        self._Patient._CalibrationType = CalibrationType
        self._Patient._CalibrationValue = CalibrationValue
        self._Patient._reference_side = reference_side
        self._expression = expression


        self.initUI()
        
        
    def initUI(self):
        if self._expression == 'Brow Raise':
            self.ui = uic.loadUi('uis\Auto_eFace_Brow_Raise.ui', self)
            self.get_Patient()
            Brow_Raise = get_brow_raise(self._Patient)
            x = ['Brow Raise']
            y = [Brow_Raise]
            ##############
            """Setting Line Edits Functions"""
            ##############
            validator = DoubleValidator( 0, 100, 1, self)
            self.BHLineEdit.setValidator(validator)
            self.BHLineEdit.setText(str(Brow_Raise))
            self.BHLineEdit.textChanged.connect(self.updateBRGraph)

        elif self._expression == 'Gentle Eye Closure':
            self.ui = uic.loadUi('uis\Auto_eFace_Gentle_Eye_Closure_Double.ui', self)
            self.get_Patient()
            Gentle_Eye_Closure = get_GEC(self._Patient)
            x = ['Gentle Eye Closure']
            y = [Gentle_Eye_Closure]
            ##############
            """Setting Line Edits Functions"""
            ##############
            validator = DoubleValidator( 0, 100, 1, self)
            self.PFLineEdit.setValidator(validator)
            self.PFLineEdit.setText(str(Gentle_Eye_Closure))
            self.PFLineEdit.textChanged.connect(self.updateGECGraph)
        
        elif self._expression == 'Tight Eye Closure':
            self.ui = uic.loadUi('uis\Auto_eFace_Tight_Eye_Closure_Double.ui', self)
            self.get_Patient()
            Tight_Eye_Closure = get_TEC(self._Patient)
            x = ['Tight Eye Closure']
            y = [Tight_Eye_Closure]
            ##############
            """Setting Line Edits Functions"""
            ##############
            validator = DoubleValidator( 0, 100, 1, self)
            self.PFLineEdit.setValidator(validator)
            self.PFLineEdit.setText(str(Tight_Eye_Closure))
            self.PFLineEdit.textChanged.connect(self.updateTECGraph)

        elif self._expression == 'Big Smile':
            self.ui = uic.loadUi('uis\Auto_eFace_Big_Smile_Double.ui', self)
            self.get_Patient()
            Oral_Commissure = get_OCM(self._Patient)
            x = ['Oral Commissure Movement with Smile']
            y = [Oral_Commissure]
            ##############
            """Setting Line Edits Functions"""
            ##############
            validator = DoubleValidator( 0, 100, 1, self)
            self.OCLineEdit.setValidator(validator)
            self.OCLineEdit.setText(str(Oral_Commissure)) 
            self.OCLineEdit.textChanged.connect(self.updateBSGraph)

        ##############
        """Plotting"""
        ##############
        self.plot_Data(x, y)


    def plot_Data(self, x, y):
        self.plotWidget.canvas.ax.bar(x, y, color='blue')
        self.plotWidget.canvas.ax.set_xlabel('Parameters')
        self.plotWidget.canvas.ax.set_ylabel('Auto-eFace Score')
        self.plotWidget.canvas.ax.set_title(f'{self._expression} Expression Scores')
        self.plotWidget.canvas.ax.set_ylim(0,100)


    def get_Patient(self):
        """This function collects the info need to find the dynamic parameters"""
        if self._expression == 'Brow Raise': 
            #Brow Raise
            self._Patient._Brow_Raise._shape = self._shape2
            self._Patient._Brow_Raise._lefteye = self._lefteye2
            self._Patient._Brow_Raise._righteye = self._righteye2
            self._Patient._Brow_Raise._points = self._points2
        elif self._expression == 'Gentle Eye Closure': 
            #Gentle Eye Closure
            self._Patient._Gentle_Eye_Closure._shape = self._shape2
            self._Patient._Gentle_Eye_Closure._lefteye = self._lefteye2
            self._Patient._Gentle_Eye_Closure._righteye = self._righteye2
            self._Patient._Gentle_Eye_Closure._points = self._points2
        elif self._expression == 'Tight Eye Closure': 
            #Tight Eye Closure
            self._Patient._Tight_Eye_Closure._shape = self._shape2
            self._Patient._Tight_Eye_Closure._lefteye = self._lefteye2
            self._Patient._Tight_Eye_Closure._righteye = self._righteye2
            self._Patient._Tight_Eye_Closure._points = self._points2
        elif self._expression == 'Big Smile': 
            #Brow Raise
            self._Patient._Big_Smile._shape = self._shape2
            self._Patient._Big_Smile._lefteye = self._lefteye2
            self._Patient._Big_Smile._righteye = self._righteye2
            self._Patient._Big_Smile._points = self._points2

    
    def updateBRGraph(self, text):
        """This function is call for updating the graph when any LineEdit is changed
        if the expression for the photo is 'Brow Raise'
        
        Scores shown: Brow Raise"""
        #Collects Scores from LineEdits
        try:
            Brow_Raise = float(self.BHLineEdit.text())
        except:
            Brow_Raise = 0

        #Creates array of score so it can be plotted
        x = ['Brow Raise']
        y = [Brow_Raise]

        #Plots Data
        self.plotWidget.canvas.ax.clear()
        self.plot_Data(x, y)
        self.plotWidget.canvas.draw()

    
    def updateGECGraph(self, text):
        """This function is call for updating the graph when any LineEdit is changed
        if the expression for the photo is 'GEC' (Gentle Eye Closure)
        
        Scores shown: Gentle Eye Closure"""
        #Collects Scores from LineEdits
        try:
            Gentle_Eye_Closure = float(self.PFLineEdit.text())
        except:
            Gentle_Eye_Closure = 0

        #Creates array of score so it can be plotted
        x = ['Gentle Eye Closure']
        y = [Gentle_Eye_Closure]

        #Plots Data
        self.plotWidget.canvas.ax.clear()
        self.plot_Data(x, y)
        self.plotWidget.canvas.draw()


    def updateTECGraph(self, text):
        """This function is call for updating the graph when any LineEdit is changed
        if the expression for the photo is 'TEC' (Tight Eye Closure)
        
        Scores shown: Tight Eye Closure"""
        #Collects Scores from LineEdits
        try:
            Tight_Eye_Closure = float(self.PFLineEdit.text())
        except:
            Tight_Eye_Closure = 0
        

        #Creates array of score so it can be plotted
        x = ['Tight Eye Closure']
        y = [Tight_Eye_Closure]

        #Plots Data
        self.plotWidget.canvas.ax.clear()
        self.plot_Data(x, y)
        self.plotWidget.canvas.draw()


    def updateBSGraph(self, text):
        """This function is call for updating the graph when any LineEdit is changed
        if the expression for the photo is 'Big Smile' 
        
        Scores shown: Oral Commissure Movement with Smile"""
        #Collects Scores from LineEdits
        try:
            Oral_Commissure = float(self.OCLineEdit.text())
        except:
            Oral_Commissure = 0

        #Creates array of score so it can be plotted
        x = ['Oral Commissure Movement with Smile']
        y = [Oral_Commissure]

        #Plots Data
        self.plotWidget.canvas.ax.clear()
        self.plot_Data(x, y)
        self.plotWidget.canvas.draw()


    