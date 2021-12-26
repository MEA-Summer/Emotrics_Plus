import sys

import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtGui import QDoubleValidator, QValidator
from torch._C import has_openmp

from Compute_eFace import *
from Metrics import get_measurements_from_data
from MplWidget import MplWidget


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

class Auto_eFaceWindow(QtWidgets.QMainWindow):
    
    def __init__(self, shape, left_pupil, right_pupil, points, CalibrationType, CalibrationValue, reference_side, file_name, expression):
        super() .__init__()
        #Sets input to variables
        self._shape = shape
        self._lefteye = left_pupil
        self._righteye = right_pupil
        self._points = points
        self._CalibrationType = CalibrationType
        self._CalibrationValue = CalibrationValue
        self._reference_side = reference_side
        self._fileName = file_name
        self._expression = expression


        self.initUI()
        
        
    def initUI(self):
        #Collect Measurement
        (MeasurementsLeft, MeasurementsRight, 
        MeasurementsDeviation, MeasurementsPercentual) = get_measurements_from_data(
            self._shape, self._lefteye, self._righteye, self._points, 
            self._CalibrationType, self._CalibrationValue, self._reference_side)
        #Get all 4 parameters
        Resting_Brow, Resting_Palpebral_Fissure, Oral_Commissure_at_Rest, NLF_at_rest = Compute_Static_eFace(MeasurementsLeft, MeasurementsRight, self._reference_side)
        #Set true if graph contains parameter
        has_BH = False
        has_PF = False
        has_OC = False
        has_NLF = False

        if self._expression == 'Resting':
            self.ui = uic.loadUi('uis\Auto_eFace_Resting.ui', self)
            x = ['Brow Height', 'Palpebral Fissure', 'Oral Commissure', 'Nasolabial Fold Angle']
            y = [Resting_Brow, Resting_Palpebral_Fissure, Oral_Commissure_at_Rest, NLF_at_rest]
            ##############
            """Setting Line Edits Functions"""
            ##############
            has_BH = True
            self.BHLineEdit.textChanged.connect(self.updateRestingGraph)
            has_PF = True
            self.PFLineEdit.textChanged.connect(self.updateRestingGraph)
            has_OC = True
            self.OCLineEdit.textChanged.connect(self.updateRestingGraph)
            has_NLF = True
            self.NLFLineEdit.textChanged.connect(self.updateRestingGraph)

        elif self._expression == 'Brow Raise':
            self.ui = uic.loadUi('uis\Auto_eFace_Brow_Raise.ui', self)
            x = ['Brow Height']
            y = [Resting_Brow]
            ##############
            """Setting Line Edits Functions"""
            ##############
            has_BH = True
            self.BHLineEdit.textChanged.connect(self.updateBRGraph)

        elif self._expression == 'Gentle Eye Closure':
            self.ui = uic.loadUi('uis\Auto_eFace_Gentle_Eye_Closure.ui', self)
            x = ['Palpebral Fissure']
            y = [Resting_Palpebral_Fissure]
            ##############
            """Setting Line Edits Functions"""
            ##############
            has_PF = True
            self.PFLineEdit.textChanged.connect(self.updateGECGraph)
        
        elif self._expression == 'Tight Eye Closure':
            self.ui = uic.loadUi('uis\Auto_eFace_Tight_Eye_Closure.ui', self)
            x = ['Palpebral Fissure', 'Nasolabial Fold Angle']
            y = [Resting_Palpebral_Fissure, NLF_at_rest]
            ##############
            """Setting Line Edits Functions"""
            ##############
            has_PF = True 
            self.PFLineEdit.textChanged.connect(self.updateTECGraph)
            has_NLF =True
            self.NLFLineEdit.textChanged.connect(self.updateTECGraph)

        elif self._expression == 'Big Smile':
            self.ui = uic.loadUi('uis\Auto_eFace_Big_Smile.ui', self)
            x = ['Nasolabial Fold Angle']
            y = [NLF_at_rest]
            ##############
            """Setting Line Edits Functions"""
            ##############
            has_NLF = True
            self.NLFLineEdit.textChanged.connect(self.updateBSGraph)

        elif self._expression == '"eeeek"':
            self.ui = uic.loadUi('uis\Auto_eFace_eee.ui', self)
            x = ['Oral Commissure', 'Nasolabial Fold Angle']
            y = [Oral_Commissure_at_Rest, NLF_at_rest]
            ##############
            """Setting Line Edits Functions"""
            ##############
            has_OC = True
            self.OCLineEdit.textChanged.connect(self.updateEeeekGraph)
            has_NLF = True
            self.NLFLineEdit.textChanged.connect(self.updateEeeekGraph)

        elif self._expression == '"ooooo"':
            self.ui = uic.loadUi('uis\Auto_eFace_ooo.ui', self)

            score_PalpebralFissure_rest = 100 - abs(100-Resting_Palpebral_Fissure)
            x = ['Ocular Synkinesis']
            y = [score_PalpebralFissure_rest]
            ##############
            """Setting Line Edits Functions"""
            ##############
            #Since "ooooo" is a special case, it is set different than others
            validator = DoubleValidator(0, 100, 1, self)
            self.PFLineEdit.setValidator(validator)
            self.PFLineEdit.setText(str(score_PalpebralFissure_rest))
            self.PFLineEdit.textChanged.connect(self.updateOooooGraph)

        ##############
        """Plotting"""
        ##############
        self.plotWidget.canvas.ax.bar(x, y, color='blue')
        self.plotWidget.canvas.ax.set_xlabel('Parameters')
        self.plotWidget.canvas.ax.set_ylabel('Auto-eFace Score')
        self.plotWidget.canvas.ax.set_title(f'{self._expression} Expression Scores')
        if self._expression == '"ooooo"':
            self.plotWidget.canvas.ax.set_ylim(0,100)
        else:
            self.plotWidget.canvas.ax.set_ylim(0,200)

        ##############
        """Filling Line Edits"""
        ##############
        if has_BH == True:
            validator = DoubleValidator( 0, 200, 1, self)
            self.BHLineEdit.setValidator(validator)
            self.BHLineEdit.setText(str(Resting_Brow))
        if has_PF == True:
            validator = DoubleValidator( 0, 200, 1, self)
            self.PFLineEdit.setValidator(validator)
            self.PFLineEdit.setText(str(Resting_Palpebral_Fissure))
        if has_OC == True:
            validator = DoubleValidator( 0, 200, 1, self)
            self.OCLineEdit.setValidator(validator)
            self.OCLineEdit.setText(str(Oral_Commissure_at_Rest))
        if has_NLF:
            validator = DoubleValidator( 0, 200, 1, self)
            self.NLFLineEdit.setValidator(validator)
            self.NLFLineEdit.setText(str(NLF_at_rest)) 




    def updateRestingGraph(self, text):
        """This function is call for updating the graph when any LineEdit is changed
        if the expression for the photo is 'Resting'
        
        Scores shown: Brow Height, Palpebral Fissure Width, Oral Commisure, Nasolabial Fold (NLF)"""
        #Collects Scores from LineEdits
        try:
            Resting_Brow = float(self.BHLineEdit.text())
        except:
            Resting_Brow = 0
        try:
            Resting_Palpebral_Fissure = float(self.PFLineEdit.text())
        except:
            Resting_Palpebral_Fissure = 0
        try:
            Oral_Commissure_at_Rest = float(self.OCLineEdit.text())
        except:
            Oral_Commissure_at_Rest = 0
        try:
            NLF_at_rest = float(self.NLFLineEdit.text())
        except:
            NLF_at_rest = 0

        #Creates array of score so it can be plotted
        x = ['Brow Height', 'Palpebral Fissure', 'Oral Commissure', 'Nasolabial Fold Angle']
        y = [Resting_Brow, Resting_Palpebral_Fissure, Oral_Commissure_at_Rest, NLF_at_rest]

        #Plots Data
        self.plotWidget.canvas.ax.clear()
        self.plotWidget.canvas.ax.bar(x, y, color='blue')
        self.plotWidget.canvas.ax.set_xlabel('Parameters')
        self.plotWidget.canvas.ax.set_ylabel('Auto-eFace Score')
        self.plotWidget.canvas.ax.set_title(f'{self._expression} Expression Scores')
        self.plotWidget.canvas.ax.set_ylim(0,200)
        self.plotWidget.canvas.draw()

    
    def updateBRGraph(self, text):
        """This function is call for updating the graph when any LineEdit is changed
        if the expression for the photo is 'Brow Raise'
        
        Scores shown: Brow Height"""
        #Collects Scores from LineEdits
        try:
            Brow_Height = float(self.BHLineEdit.text())
        except:
            Brow_Height = 0

        #Creates array of score so it can be plotted
        x = ['Brow Height']
        y = [Brow_Height]

        #Plots Data
        self.plotWidget.canvas.ax.clear()
        self.plotWidget.canvas.ax.bar(x, y, color='blue')
        self.plotWidget.canvas.ax.set_xlabel('Parameters')
        self.plotWidget.canvas.ax.set_ylabel('Auto-eFace Score')
        self.plotWidget.canvas.ax.set_title(f'{self._expression} Expression Scores')
        self.plotWidget.canvas.ax.set_ylim(0,200)
        self.plotWidget.canvas.draw()

    
    def updateGECGraph(self, text):
        """This function is call for updating the graph when any LineEdit is changed
        if the expression for the photo is 'GEC' (Gentle Eye Closure)
        
        Scores shown: Palpebral Fissure Width"""
        #Collects Scores from LineEdits
        try:
            Palpebral_Fissure = float(self.PFLineEdit.text())
        except:
            Palpebral_Fissure = 0

        #Creates array of score so it can be plotted
        x = ['Palpebral Fissure']
        y = [Palpebral_Fissure]

        #Plots Data
        self.plotWidget.canvas.ax.clear()
        self.plotWidget.canvas.ax.bar(x, y, color='blue')
        self.plotWidget.canvas.ax.set_xlabel('Parameters')
        self.plotWidget.canvas.ax.set_ylabel('Auto-eFace Score')
        self.plotWidget.canvas.ax.set_title(f'{self._expression} Expression Scores')
        self.plotWidget.canvas.ax.set_ylim(0,200)
        self.plotWidget.canvas.draw()


    def updateTECGraph(self, text):
        """This function is call for updating the graph when any LineEdit is changed
        if the expression for the photo is 'TEC' (Tight Eye Closure)
        
        Scores shown: Palpebral Fissure Width, Nasolabial Fold (NLF)"""
        #Collects Scores from LineEdits
        try:
            Palpebral_Fissure = float(self.PFLineEdit.text())
        except:
            Palpebral_Fissure = 0
        try:
            NLF = float(self.NLFLineEdit.text())
        except:
            NLF = 0

        #Creates array of score so it can be plotted
        x = ['Palpebral Fissure', 'Nasolabial Fold Angle']
        y = [Palpebral_Fissure, NLF]

        #Plots Data
        self.plotWidget.canvas.ax.clear()
        self.plotWidget.canvas.ax.bar(x, y, color='blue')
        self.plotWidget.canvas.ax.set_xlabel('Parameters')
        self.plotWidget.canvas.ax.set_ylabel('Auto-eFace Score')
        self.plotWidget.canvas.ax.set_title(f'{self._expression} Expression Scores')
        self.plotWidget.canvas.ax.set_ylim(0,200)
        self.plotWidget.canvas.draw()


    def updateBSGraph(self, text):
        """This function is call for updating the graph when any LineEdit is changed
        if the expression for the photo is 'Big Smile' 
        
        Scores shown: Nasolabial Fold (NLF)"""
        #Collects Scores from LineEdits
        try:
            NLF = float(self.NLFLineEdit.text())
        except:
            NLF = 0

        #Creates array of score so it can be plotted
        x = ['Nasolabial Fold Angle']
        y = [NLF]

        #Plots Data
        self.plotWidget.canvas.ax.clear()
        self.plotWidget.canvas.ax.bar(x, y, color='blue')
        self.plotWidget.canvas.ax.set_xlabel('Parameters')
        self.plotWidget.canvas.ax.set_ylabel('Auto-eFace Score')
        self.plotWidget.canvas.ax.set_title(f'{self._expression} Expression Scores')
        self.plotWidget.canvas.ax.set_ylim(0,200)
        self.plotWidget.canvas.draw()


    def updateEeeekGraph(self, text):
        """This function is call for updating the graph when any LineEdit is changed
        if the expression for the photo is '"eeeek"' 
        
        Scores shown: Oral Commisure, Nasolabial Fold (NLF)"""
        #Collects Scores from LineEdits
        try:
            Oral_Commissure = float(self.OCLineEdit.text())
        except:
            Oral_Commissure = 0
        try:
            NLF = float(self.NLFLineEdit.text())
        except:
            NLF = 0

        #Creates array of score so it can be plotted
        x = ['Oral Commissure', 'Nasolabial Fold Angle']
        y = [Oral_Commissure, NLF]

        #Plots Data
        self.plotWidget.canvas.ax.clear()
        self.plotWidget.canvas.ax.bar(x, y, color='blue')
        self.plotWidget.canvas.ax.set_xlabel('Parameters')
        self.plotWidget.canvas.ax.set_ylabel('Auto-eFace Score')
        self.plotWidget.canvas.ax.set_title(f'{self._expression} Expression Scores')
        self.plotWidget.canvas.ax.set_ylim(0,200)
        self.plotWidget.canvas.draw()

    
    def updateOooooGraph(self, text):
        """This function is call for updating the graph when any LineEdit is changed
        if the expression for the photo is '"ooooo"' 

        Scores shown: Ocular Synkinesis"""
        #Collects Scores from LineEdits
        try:
            Ocular_Synkinesis = float(self.PFLineEdit.text())
        except:
            Ocular_Synkinesis = 0

        #Creates array of score so it can be plotted
        x = ['Ocular Synkinesis']
        y = [Ocular_Synkinesis]

        #Plots Data
        self.plotWidget.canvas.ax.clear()
        self.plotWidget.canvas.ax.bar(x, y, color='blue')
        self.plotWidget.canvas.ax.set_xlabel('Parameters')
        self.plotWidget.canvas.ax.set_ylabel('Auto-eFace Score')
        self.plotWidget.canvas.ax.set_title(f'{self._expression} Expression Scores')
        self.plotWidget.canvas.ax.set_ylim(0,100)
        self.plotWidget.canvas.draw()

    
