import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from torch._C import has_openmp

from Compute_eFace import *
from Patient import Patient


class ReportCardWindow(QtWidgets.QMainWindow):
    
    def __init__(self, Patient):
        super() .__init__()
        #Sets input to variables
        self._Patient = Patient 
        #Finding eFace Values to be Shown on Line Edits
        (self._score_brow_rest, self._score_PalpebralFissure_rest, self._score_OralCommissure_rest, self._NLF_at_rest,
            self._BrowRaise, self._GentleEyeClosure, self._FullEyeClosure, self._OralCommissureWithSmile, self._LowerLipEEE,
            self._OcularSynkinesis, self._StaticScore, self._DynamicScore, self._SynkinesisScore, self._Total_Score) = Compute_eFace(self._Patient)

        self.initUI()
        
    def initUI(self):
        self.ui = uic.loadUi('uis\Auto_eFace.ui', self)
        ##############
        """Setting Line Edits"""
        ##############
        self.BHLineEdit.setText(str(self._score_brow_rest))
        self.PFLineEdit.setText(str(self._score_PalpebralFissure_rest))
        self.OCLineEdit.setText(str(self._score_OralCommissure_rest))
        self.NLFLineEdit.setText(str(self._NLF_at_rest))
        self.BRLineEdit.setText(str(self._BrowRaise))
        self.GECLineEdit.setText(str(self._GentleEyeClosure))
        self.TECLineEdit.setText(str(self._FullEyeClosure))
        self.ORMLineEdit.setText(str(self._OralCommissureWithSmile))
        self.LLMLineEdit.setText(str(self._LowerLipEEE))
        self.OSLineEdit.setText(str(self._OcularSynkinesis)) 
        self.SSLineEdit.setText(str(self._StaticScore))
        self.DSLineEdit.setText(str(self._DynamicScore)) 
        self.SySLineEdit.setText(str(self._SynkinesisScore)) 
        self.TSLineEdit.setText(str(self._Total_Score))
