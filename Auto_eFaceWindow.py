import numpy as np
from PyQt5 import QtWidgets, QtGui, uic, QtCore
import sys
from Metrics import get_measurements_from_data
from Compute_eFace import *
from PyQt5.QtGui import QDoubleValidator, QValidator

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
        
        
        if self._expression == 'Resting':
            if self._expression == 'Other':
                self.setWindowTitle('Other Auto eFace')
            self.ui = uic.loadUi('uis\Auto_eFace_Resting.ui', self)

            (MeasurementsLeft, MeasurementsRight, 
            MeasurementsDeviation, MeasurementsPercentual) = get_measurements_from_data(
                self._shape, self._lefteye, self._righteye, self._points, 
                self._CalibrationType, self._CalibrationValue, self._reference_side)
            print(f'self._reference_side = {self._reference_side}')
            Resting_Brow, Resting_Palpebral_Fissure, Oral_Commissure_at_Rest, NLF_at_rest = Compute_Resting_eFace(MeasurementsLeft, MeasurementsRight, self._reference_side)
            x = ['Brow Height', 'Palpebral Fissure', 'Oral Commissure', 'Nasolabial Fold Angle']

            y = [Resting_Brow, Resting_Palpebral_Fissure, Oral_Commissure_at_Rest, NLF_at_rest]

            ##############
            """Plotting"""
            ##############
            self.plotWidget.canvas.ax.bar(x, y, color='blue')
            self.plotWidget.canvas.ax.set_xlabel('Parameters')
            self.plotWidget.canvas.ax.set_ylabel('Auto-eFace Score')
            self.plotWidget.canvas.ax.set_title(f'{self._expression} Expression Scores')
            self.plotWidget.canvas.ax.set_ylim(0,200)

            ##############
            """Filling Line Edits"""
            ##############
            validator = DoubleValidator( 0, 200, 1, self)
            self.BHLineEdit.setValidator(validator)
            validator = DoubleValidator( 0, 200, 1, self)
            self.PFLineEdit.setValidator(validator)
            validator = DoubleValidator( 0, 200, 1, self)
            self.OCLineEdit.setValidator(validator)
            validator = DoubleValidator( 0, 200, 1, self)
            self.NLFLineEdit.setValidator(validator)

            self.BHLineEdit.setText(str(Resting_Brow))
            self.PFLineEdit.setText(str(Resting_Palpebral_Fissure))
            self.OCLineEdit.setText(str(Oral_Commissure_at_Rest))
            self.NLFLineEdit.setText(str(NLF_at_rest)) 

            self.BHLineEdit.textChanged.connect(self.updateRestingGraph)
            self.PFLineEdit.textChanged.connect(self.updateRestingGraph)
            self.OCLineEdit.textChanged.connect(self.updateRestingGraph)
            self.NLFLineEdit.textChanged.connect(self.updateRestingGraph)

        
        elif self._expression == 'Brow Raise':
            self.ui = uic.loadUi('uis\Auto_eFace_Brow_Raise.ui', self)

            (MeasurementsLeft, MeasurementsRight, 
            MeasurementsDeviation, MeasurementsPercentual) = get_measurements_from_data(
                self._shape, self._lefteye, self._righteye, self._points, 
                self._CalibrationType, self._CalibrationValue, self._reference_side)
            Resting_Brow = Compute_eFace_BH(MeasurementsLeft, MeasurementsRight, self._reference_side)
            x = ['Brow Height']

            y = [Resting_Brow]

            ##############
            """Plotting"""
            ##############
            self.plotWidget.canvas.ax.bar(x, y, color='blue')
            self.plotWidget.canvas.ax.set_xlabel('Parameters')
            self.plotWidget.canvas.ax.set_ylabel('Auto-eFace Score')
            self.plotWidget.canvas.ax.set_title(f'{self._expression} Expression Scores')
            self.plotWidget.canvas.ax.set_ylim(0,200)

            ##############
            """Filling Line Edits"""
            ##############
            validator = DoubleValidator( 0, 200, 1, self)
            self.BHLineEdit.setValidator(validator)

            self.BHLineEdit.setText(str(Resting_Brow))

            self.BHLineEdit.textChanged.connect(self.updateBRGraph)


        elif self._expression == 'Gentle Eye Closure':
            self.ui = uic.loadUi('uis\Auto_eFace_Gentle_Eye_Closure.ui', self)

            (MeasurementsLeft, MeasurementsRight, 
            MeasurementsDeviation, MeasurementsPercentual) = get_measurements_from_data(
                self._shape, self._lefteye, self._righteye, self._points, 
                self._CalibrationType, self._CalibrationValue, self._reference_side)
            Resting_Brow, Resting_Palpebral_Fissure, Oral_Commissure_at_Rest, NLF_at_rest = Compute_Resting_eFace(MeasurementsLeft, MeasurementsRight, self._reference_side)
            x = ['Palpebral Fissure']

            y = [Resting_Palpebral_Fissure]

            ##############
            """Plotting"""
            ##############
            self.plotWidget.canvas.ax.bar(x, y, color='blue')
            self.plotWidget.canvas.ax.set_xlabel('Parameters')
            self.plotWidget.canvas.ax.set_ylabel('Auto-eFace Score')
            self.plotWidget.canvas.ax.set_title(f'{self._expression} Expression Scores')
            self.plotWidget.canvas.ax.set_ylim(0,200)

            ##############
            """Filling Line Edits"""
            ##############
            validator = DoubleValidator( 0, 200, 1, self)
            self.PFLineEdit.setValidator(validator)
            
            self.PFLineEdit.setText(str(Resting_Palpebral_Fissure))

            self.PFLineEdit.textChanged.connect(self.updateGECGraph)
        

        elif self._expression == 'Tight Eye Closure':
            self.ui = uic.loadUi('uis\Auto_eFace_Tight_Eye_Closure.ui', self)

            (MeasurementsLeft, MeasurementsRight, 
            MeasurementsDeviation, MeasurementsPercentual) = get_measurements_from_data(
                self._shape, self._lefteye, self._righteye, self._points, 
                self._CalibrationType, self._CalibrationValue, self._reference_side)
            Resting_Palpebral_Fissure = Compute_eFace_PF(MeasurementsLeft, MeasurementsRight, self._reference_side)
            NLF_at_rest = Compute_eFace_NLF(MeasurementsLeft, MeasurementsRight, self._reference_side)
            x = ['Palpebral Fissure', 'Nasolabial Fold Angle']

            y = [Resting_Palpebral_Fissure, NLF_at_rest]

            ##############
            """Plotting"""
            ##############
            self.plotWidget.canvas.ax.bar(x, y, color='blue')
            self.plotWidget.canvas.ax.set_xlabel('Parameters')
            self.plotWidget.canvas.ax.set_ylabel('Auto-eFace Score')
            self.plotWidget.canvas.ax.set_title(f'{self._expression} Expression Scores')
            self.plotWidget.canvas.ax.set_ylim(0,200)

            ##############
            """Filling Line Edits"""
            ##############
            validator = DoubleValidator( 0, 200, 1, self)
            self.PFLineEdit.setValidator(validator)
            validator = DoubleValidator( 0, 200, 1, self)
            self.NLFLineEdit.setValidator(validator)

            self.PFLineEdit.setText(str(Resting_Palpebral_Fissure))
            self.NLFLineEdit.setText(str(NLF_at_rest)) 

            self.PFLineEdit.textChanged.connect(self.updateTECGraph)
            self.NLFLineEdit.textChanged.connect(self.updateTECGraph)

        
        elif self._expression == 'Big Smile':
            self.ui = uic.loadUi('uis\Auto_eFace_Big_Smile.ui', self)

            (MeasurementsLeft, MeasurementsRight, 
            MeasurementsDeviation, MeasurementsPercentual) = get_measurements_from_data(
                self._shape, self._lefteye, self._righteye, self._points, 
                self._CalibrationType, self._CalibrationValue, self._reference_side)
            Oral_Commissure_at_Rest = Compute_eFace_OC(MeasurementsLeft, MeasurementsRight, self._reference_side)
            NLF_at_rest = Compute_eFace_NLF(MeasurementsLeft, MeasurementsRight, self._reference_side)
            x = ['Oral Commissure', 'Nasolabial Fold Angle']

            y = [Oral_Commissure_at_Rest, NLF_at_rest]

            ##############
            """Plotting"""
            ##############
            self.plotWidget.canvas.ax.bar(x, y, color='blue')
            self.plotWidget.canvas.ax.set_xlabel('Parameters')
            self.plotWidget.canvas.ax.set_ylabel('Auto-eFace Score')
            self.plotWidget.canvas.ax.set_title(f'{self._expression} Expression Scores')
            self.plotWidget.canvas.ax.set_ylim(0,200)

            ##############
            """Filling Line Edits"""
            ##############
            validator = DoubleValidator( 0, 200, 1, self)
            self.OCLineEdit.setValidator(validator)
            validator = DoubleValidator( 0, 200, 1, self)
            self.NLFLineEdit.setValidator(validator)

            self.OCLineEdit.setText(str(Oral_Commissure_at_Rest))
            self.NLFLineEdit.setText(str(NLF_at_rest)) 

            self.OCLineEdit.textChanged.connect(self.updateBSGraph)
            self.NLFLineEdit.textChanged.connect(self.updateBSGraph)

        
        elif self._expression == '"eeeek"':
            self.ui = uic.loadUi('uis\Auto_eFace_eee.ui', self)

            (MeasurementsLeft, MeasurementsRight, 
            MeasurementsDeviation, MeasurementsPercentual) = get_measurements_from_data(
                self._shape, self._lefteye, self._righteye, self._points, 
                self._CalibrationType, self._CalibrationValue, self._reference_side)
            Oral_Commissure_at_Rest = Compute_eFace_OC(MeasurementsLeft, MeasurementsRight, self._reference_side)
            NLF_at_rest = Compute_eFace_NLF(MeasurementsLeft, MeasurementsRight, self._reference_side)
            x = ['Oral Commissure', 'Nasolabial Fold Angle']

            y = [Oral_Commissure_at_Rest, NLF_at_rest]

            ##############
            """Plotting"""
            ##############
            self.plotWidget.canvas.ax.bar(x, y, color='blue')
            self.plotWidget.canvas.ax.set_xlabel('Parameters')
            self.plotWidget.canvas.ax.set_ylabel('Auto-eFace Score')
            self.plotWidget.canvas.ax.set_title(f'{self._expression} Expression Scores')
            self.plotWidget.canvas.ax.set_ylim(0,200)

            ##############
            """Filling Line Edits"""
            ##############
            validator = DoubleValidator( 0, 200, 1, self)
            self.OCLineEdit.setValidator(validator)
            validator = DoubleValidator( 0, 200, 1, self)
            self.NLFLineEdit.setValidator(validator)

            self.OCLineEdit.setText(str(Oral_Commissure_at_Rest))
            self.NLFLineEdit.setText(str(NLF_at_rest)) 

            self.OCLineEdit.textChanged.connect(self.updateEeeekGraph)
            self.NLFLineEdit.textChanged.connect(self.updateEeeekGraph)

        
        elif self._expression == '"ooooo"':
            self.ui = uic.loadUi('uis\Auto_eFace_ooo.ui', self)

            (MeasurementsLeft, MeasurementsRight, 
            MeasurementsDeviation, MeasurementsPercentual) = get_measurements_from_data(
                self._shape, self._lefteye, self._righteye, self._points, 
                self._CalibrationType, self._CalibrationValue, self._reference_side)
            Resting_Palpebral_Fissure = Compute_eFace_PF(MeasurementsLeft, MeasurementsRight, self._reference_side)
            x = ['Ocular Synkinesis']

            y = [Resting_Palpebral_Fissure]

            ##############
            """Plotting"""
            ##############
            self.plotWidget.canvas.ax.bar(x, y, color='blue')
            self.plotWidget.canvas.ax.set_xlabel('Parameters')
            self.plotWidget.canvas.ax.set_ylabel('Auto-eFace Score')
            self.plotWidget.canvas.ax.set_title(f'{self._expression} Expression Scores')
            self.plotWidget.canvas.ax.set_ylim(0,200)

            ##############
            """Filling Line Edits"""
            ##############
            validator = DoubleValidator( 0, 200, 1, self)
            self.PFLineEdit.setValidator(validator)

            self.PFLineEdit.setText(str(Resting_Palpebral_Fissure))

            self.PFLineEdit.textChanged.connect(self.updateOooooGraph)


    def updateRestingGraph(self, text):
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

        x = ['Brow Height', 'Palpebral Fissure', 'Oral Commissure', 'Nasolabial Fold Angle']
        y = [Resting_Brow, Resting_Palpebral_Fissure, Oral_Commissure_at_Rest, NLF_at_rest]

        self.plotWidget.canvas.ax.clear()
        self.plotWidget.canvas.ax.bar(x, y, color='blue')
        self.plotWidget.canvas.ax.set_xlabel('Parameters')
        self.plotWidget.canvas.ax.set_ylabel('Auto-eFace Score')
        self.plotWidget.canvas.ax.set_title(f'{self._expression} Expression Scores')
        self.plotWidget.canvas.ax.set_ylim(0,200)
        self.plotWidget.canvas.draw()

    
    def updateBRGraph(self, text):
        try:
            Resting_Brow = float(self.BHLineEdit.text())
        except:
            Resting_Brow = 0

        x = ['Brow Height']
        y = [Resting_Brow]

        self.plotWidget.canvas.ax.clear()
        self.plotWidget.canvas.ax.bar(x, y, color='blue')
        self.plotWidget.canvas.ax.set_xlabel('Parameters')
        self.plotWidget.canvas.ax.set_ylabel('Auto-eFace Score')
        self.plotWidget.canvas.ax.set_title(f'{self._expression} Expression Scores')
        self.plotWidget.canvas.ax.set_ylim(0,200)
        self.plotWidget.canvas.draw()

    
    def updateGECGraph(self, text):
        try:
            Resting_Palpebral_Fissure = float(self.PFLineEdit.text())
        except:
            Resting_Palpebral_Fissure = 0

        x = ['Palpebral Fissure']
        y = [Resting_Palpebral_Fissure]

        self.plotWidget.canvas.ax.clear()
        self.plotWidget.canvas.ax.bar(x, y, color='blue')
        self.plotWidget.canvas.ax.set_xlabel('Parameters')
        self.plotWidget.canvas.ax.set_ylabel('Auto-eFace Score')
        self.plotWidget.canvas.ax.set_title(f'{self._expression} Expression Scores')
        self.plotWidget.canvas.ax.set_ylim(0,200)
        self.plotWidget.canvas.draw()


    def updateTECGraph(self, text):
        try:
            Resting_Palpebral_Fissure = float(self.PFLineEdit.text())
        except:
            Resting_Palpebral_Fissure = 0
        try:
            NLF_at_rest = float(self.NLFLineEdit.text())
        except:
            NLF_at_rest = 0

        x = ['Palpebral Fissure', 'Nasolabial Fold Angle']
        y = [Resting_Palpebral_Fissure, NLF_at_rest]

        self.plotWidget.canvas.ax.clear()
        self.plotWidget.canvas.ax.bar(x, y, color='blue')
        self.plotWidget.canvas.ax.set_xlabel('Parameters')
        self.plotWidget.canvas.ax.set_ylabel('Auto-eFace Score')
        self.plotWidget.canvas.ax.set_title(f'{self._expression} Expression Scores')
        self.plotWidget.canvas.ax.set_ylim(0,200)
        self.plotWidget.canvas.draw()


    def updateBSGraph(self, text):
        try:
            Oral_Commissure_at_Rest = float(self.OCLineEdit.text())
        except:
            Oral_Commissure_at_Rest = 0
        try:
            NLF_at_rest = float(self.NLFLineEdit.text())
        except:
            NLF_at_rest = 0

        x = ['Oral Commissure', 'Nasolabial Fold Angle']
        y = [Oral_Commissure_at_Rest, NLF_at_rest]

        self.plotWidget.canvas.ax.clear()
        self.plotWidget.canvas.ax.bar(x, y, color='blue')
        self.plotWidget.canvas.ax.set_xlabel('Parameters')
        self.plotWidget.canvas.ax.set_ylabel('Auto-eFace Score')
        self.plotWidget.canvas.ax.set_title(f'{self._expression} Expression Scores')
        self.plotWidget.canvas.ax.set_ylim(0,200)
        self.plotWidget.canvas.draw()


    def updateEeeekGraph(self, text):
        try:
            Oral_Commissure_at_Rest = float(self.OCLineEdit.text())
        except:
            Oral_Commissure_at_Rest = 0
        try:
            NLF_at_rest = float(self.NLFLineEdit.text())
        except:
            NLF_at_rest = 0

        x = ['Oral Commissure', 'Nasolabial Fold Angle']
        y = [Oral_Commissure_at_Rest, NLF_at_rest]

        self.plotWidget.canvas.ax.clear()
        self.plotWidget.canvas.ax.bar(x, y, color='blue')
        self.plotWidget.canvas.ax.set_xlabel('Parameters')
        self.plotWidget.canvas.ax.set_ylabel('Auto-eFace Score')
        self.plotWidget.canvas.ax.set_title(f'{self._expression} Expression Scores')
        self.plotWidget.canvas.ax.set_ylim(0,200)
        self.plotWidget.canvas.draw()

    
    def updateOooooGraph(self, text):
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

        x = ['Brow Height', 'Palpebral Fissure', 'Oral Commissure', 'Nasolabial Fold Angle']
        y = [Resting_Brow, Resting_Palpebral_Fissure, Oral_Commissure_at_Rest, NLF_at_rest]

        self.plotWidget.canvas.ax.clear()
        self.plotWidget.canvas.ax.bar(x, y, color='blue')
        self.plotWidget.canvas.ax.set_xlabel('Parameters')
        self.plotWidget.canvas.ax.set_ylabel('Auto-eFace Score')
        self.plotWidget.canvas.ax.set_title(f'{self._expression} Expression Scores')
        self.plotWidget.canvas.ax.set_ylim(0,200)
        self.plotWidget.canvas.draw()

    
