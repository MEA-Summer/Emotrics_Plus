import numpy as np
from PyQt5 import QtWidgets, QtGui, uic
from Metrics import get_measurements_from_data, FaceMeasurementsSide, FaceMeasurementsDeviation
from MetricsDisplay import MetricsDisplay

class MetricsDoubleWindow(QtWidgets.QMainWindow):
    
    def __init__(self, shape1, left_pupil1, right_pupil1, points1, shape2, left_pupil2, right_pupil2, points2, CalibrationType, CalibrationValue, reference_side, task):
        super() .__init__()
        #Photo 1
        self._shape1 = shape1
        self._lefteye1 = left_pupil1
        self._righteye1 = right_pupil1
        self._points1 = points1

        self._MeasurementsLeft1 = None
        self._MeasurementsRight1 = None
        self._MeasurementsDeviation1 = None
        self._MeasurementsPercentual1 = None
        #Photo 2
        self._shape2 = shape2
        self._lefteye2 = left_pupil2
        self._righteye2 = right_pupil2
        self._points2 = points2
        self._MeasurementsLeft2 = None
        self._MeasurementsRight2 = None
        self._MeasurementsDeviation2 = None
        self._MeasurementsPercentual2 = None

        #Patient/Setting Info
        self._CalibrationType = CalibrationType
        self._CalibrationValue = CalibrationValue
        self._reference_side = reference_side
        self._task = task
        
        #Measurements
        #One Side
        self._MeasurementLeftComparison = None
        self._MeasurementRightComparison = None
        self._MeasurementLeftPercentComparison = None
        self._MeasurementRightPercentComparison = None
        #Two Side
        self._MeasurementStateComparison = None
        self._MeasurementStatePercentComparison = None

        self.initUI()
        
        
    def initUI(self):
        self.ui = uic.loadUi('uis\Metrics_Double.ui', self)
        
        #Measurements
        self._MeasurementsLeft1, self._MeasurementsRight1, self._MeasurementsDeviation1, self._MeasurementsPercentual1 = get_measurements_from_data(self._shape1, self._lefteye1, self._righteye1, self._points1, self._CalibrationType, self._CalibrationValue, self._reference_side)
        self._MeasurementsLeft2, self._MeasurementsRight2, self._MeasurementsDeviation2, self._MeasurementsPercentual2 = get_measurements_from_data(self._shape2, self._lefteye2, self._righteye2, self._points2, self._CalibrationType, self._CalibrationValue, self._reference_side)
        
        #One Side Comparison
        self.getOneSideComparison()

        #Two Side Comparison
        self.getTwoSideComparison()

        #Set Tab names
        if self._task == 'Pre-Op vs Post-Op':
            self.tabWidget.setTabText(0, 'Pre-Op State Photograph')
            self.tabWidget.setTabText(1, 'Post-Op State Photograph')
        if self._task == 'Resting vs Expression':
            self.tabWidget.setTabText(0, 'Resting State Photograph')
            self.tabWidget.setTabText(1, 'Expression State Photograph')


        #####################
        #Measurements 1
        #####################
        
        #Brow Height
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsRight1.BrowHeight, decimals=2)) if str(np.round(self._MeasurementsRight1.BrowHeight, decimals=2)) != '0' else '-')
        self.photo1Table.setItem(0, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsLeft1.BrowHeight, decimals=2)) if str(np.round(self._MeasurementsLeft1.BrowHeight, decimals=2)) != '0' else '-')
        self.photo1Table.setItem(0, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsDeviation1.BrowHeight, decimals=2)) if str(np.round(self._MeasurementsDeviation1.BrowHeight, decimals=2)) != '0' else '-')
        self.photo1Table.setItem(0, 2, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsPercentual1.BrowHeight, decimals=2)) if str(np.round(self._MeasurementsPercentual1.BrowHeight, decimals=2)) != '0' else '-')
        self.photo1Table.setItem(0, 3, val)
        
        #Marginal Reflex Distance 1
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsRight1.MarginalReflexDistance1, decimals=2)) if str(np.round(self._MeasurementsRight1.MarginalReflexDistance1, decimals=2)) != '0' else '-')
        self.photo1Table.setItem(1, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsLeft1.MarginalReflexDistance1, decimals=2)) if str(np.round(self._MeasurementsLeft1.MarginalReflexDistance1, decimals=2)) != '0' else '-')
        self.photo1Table.setItem(1, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsDeviation1.MarginalReflexDistance1, decimals=2)) if str(np.round(self._MeasurementsDeviation1.MarginalReflexDistance1, decimals=2)) != '0' else '-')
        self.photo1Table.setItem(1, 2, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsPercentual1.MarginalReflexDistance1, decimals=2)) if str(np.round(self._MeasurementsPercentual1.MarginalReflexDistance1, decimals=2)) != '0' else '-')
        self.photo1Table.setItem(1, 3, val)
        
        #Marginal Reflex Distance 2
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsRight1.MarginalReflexDistance2, decimals=2)) if str(np.round(self._MeasurementsRight1.MarginalReflexDistance2, decimals=2)) != '0' else '-')
        self.photo1Table.setItem(2, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsLeft1.MarginalReflexDistance2, decimals=2)) if str(np.round(self._MeasurementsLeft1.MarginalReflexDistance2, decimals=2)) != '0' else '-')
        self.photo1Table.setItem(2, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsDeviation1.MarginalReflexDistance2, decimals=2)) if str(np.round(self._MeasurementsDeviation1.MarginalReflexDistance2, decimals=2)) != '0' else '-')
        self.photo1Table.setItem(2, 2, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsPercentual1.MarginalReflexDistance2, decimals=2)) if str(np.round(self._MeasurementsPercentual1.MarginalReflexDistance2, decimals=2)) != '0' else '-')
        self.photo1Table.setItem(2, 3, val)
        
        #Palpebral Fissure Height
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsRight1.PalpebralFissureHeight, decimals=2)) if str(np.round(self._MeasurementsRight1.PalpebralFissureHeight, decimals=2)) != '0' else '-')
        self.photo1Table.setItem(3, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsLeft1.PalpebralFissureHeight, decimals=2)) if str(np.round(self._MeasurementsLeft1.PalpebralFissureHeight, decimals=2)) != '0' else '-')
        self.photo1Table.setItem(3, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsDeviation1.PalpebralFissureHeight, decimals=2)) if str(np.round(self._MeasurementsDeviation1.PalpebralFissureHeight, decimals=2)) != '0' else '-')
        self.photo1Table.setItem(3, 2, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsPercentual1.PalpebralFissureHeight, decimals=2)) if str(np.round(self._MeasurementsPercentual1.PalpebralFissureHeight, decimals=2)) != '0' else '-')
        self.photo1Table.setItem(3, 3, val)
        
        #Eye Area
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsRight1.EyeArea, decimals=2)) if str(np.round(self._MeasurementsRight1.EyeArea, decimals=2)) != '0' else '-')
        self.photo1Table.setItem(4, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsLeft1.EyeArea, decimals=2)) if str(np.round(self._MeasurementsLeft1.EyeArea, decimals=2)) != '0' else '-')
        self.photo1Table.setItem(4, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsDeviation1.EyeArea, decimals=2)) if str(np.round(self._MeasurementRightComparison.LowerLipHeight, decimals=2)) != '0' else '-')
        self.photo1Table.setItem(4, 2, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsPercentual1.EyeArea, decimals=2)) if str(np.round(self._MeasurementsPercentual1.EyeArea, decimals=2)) != '0' else '-')
        self.photo1Table.setItem(4, 3, val)
        
        #NLF Angle
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsRight1.NLF_angle, decimals=2)) if str(np.round(self._MeasurementsRight1.NLF_angle, decimals=2)) != '0' else '-')
        self.photo1Table.setItem(5, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsLeft1.NLF_angle, decimals=2)) if str(np.round(self._MeasurementsLeft1.NLF_angle, decimals=2)) != '0' else '-')
        self.photo1Table.setItem(5, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsDeviation1.NLF_angle, decimals=2)) if str(np.round(self._MeasurementsDeviation1.NLF_angle, decimals=2)) != '0' else '-')
        self.photo1Table.setItem(5, 2, val)
        val = QtWidgets.QTableWidgetItem('-')
        self.photo1Table.setItem(5, 3, val)
        
        #Upper Lip Slope
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsRight1.UpperLipSlope, decimals=2)) if str(np.round(self._MeasurementsRight1.UpperLipSlope, decimals=2)) != '0' else '-')
        self.photo1Table.setItem(6, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsLeft1.UpperLipSlope, decimals=2)) if str(np.round(self._MeasurementsLeft1.UpperLipSlope, decimals=2)) != '0' else '-')
        self.photo1Table.setItem(6, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsDeviation1.UpperLipSlope, decimals=2)) if str(np.round(self._MeasurementsDeviation1.UpperLipSlope, decimals=2)) != '0' else '-')
        self.photo1Table.setItem(6, 2, val)
        val = QtWidgets.QTableWidgetItem('-')
        self.photo1Table.setItem(6, 3, val)
        
        #Commisure Height
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsRight1.CommisureHeight, decimals=2)) if str(np.round(self._MeasurementsRight1.CommisureHeight, decimals=2)) != '0' else '-')
        self.photo1Table.setItem(7, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsLeft1.CommisureHeight, decimals=2)) if str(np.round(self._MeasurementsLeft1.CommisureHeight, decimals=2)) != '0' else '-')
        self.photo1Table.setItem(7, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsDeviation1.CommisureHeight, decimals=2)) if str(np.round(self._MeasurementsDeviation1.CommisureHeight, decimals=2)) != '0' else '-')
        self.photo1Table.setItem(7, 2, val)
        val = QtWidgets.QTableWidgetItem('-')
        self.photo1Table.setItem(7, 3, val)
        
        #Dental Show
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsRight1.InterlabialDistance, decimals=2)) if str(np.round(self._MeasurementsRight1.InterlabialDistance, decimals=2)) != '0' else '-')
        self.photo1Table.setItem(8, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsLeft1.InterlabialDistance, decimals=2)) if str(np.round(self._MeasurementsLeft1.InterlabialDistance, decimals=2)) != '0' else '-')
        self.photo1Table.setItem(8, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsDeviation1.InterlabialDistance, decimals=2)) if str(np.round(self._MeasurementsDeviation1.InterlabialDistance, decimals=2)) != '0' else '-')
        self.photo1Table.setItem(8, 2, val)
        val = QtWidgets.QTableWidgetItem('-')
        self.photo1Table.setItem(8, 3, val)
        
        #Dental Show Area
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsRight1.InterlabialArea_of_the_Hemiface, decimals=2)) if str(np.round(self._MeasurementsRight1.InterlabialArea_of_the_Hemiface, decimals=2)) != '0' else '-')
        self.photo1Table.setItem(9, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsLeft1.InterlabialArea_of_the_Hemiface, decimals=2)) if str(np.round(self._MeasurementsLeft1.InterlabialArea_of_the_Hemiface, decimals=2)) != '0' else '-')
        self.photo1Table.setItem(9, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsDeviation1.InterlabialArea_of_the_Hemiface, decimals=2)) if str(np.round(self._MeasurementsDeviation1.InterlabialArea_of_the_Hemiface, decimals=2)) != '0' else '-')
        self.photo1Table.setItem(9, 2, val)
        val = QtWidgets.QTableWidgetItem('-')
        self.photo1Table.setItem(9, 3, val)
        
        #Commissure Position
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsRight1.CommissurePosition, decimals=2)) if str(np.round(self._MeasurementsRight1.CommissurePosition, decimals=2)) != '0' else '-')
        self.photo1Table.setItem(10, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsLeft1.CommissurePosition, decimals=2)) if str(np.round(self._MeasurementsLeft1.CommissurePosition, decimals=2)) != '0' else '-')
        self.photo1Table.setItem(10, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsDeviation1.CommissurePosition, decimals=2)) if str(np.round(self._MeasurementsDeviation1.CommissurePosition, decimals=2)) != '0' else '-')
        self.photo1Table.setItem(10, 2, val)
        val = QtWidgets.QTableWidgetItem('-')
        self.photo1Table.setItem(10, 3, val)
        
        #Lower Lip Height Deviation
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsRight1.LowerLipHeight, decimals=2)) if str(np.round(self._MeasurementsRight1.LowerLipHeight, decimals=2)) != '0' else '-')
        self.photo1Table.setItem(11, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsLeft1.LowerLipHeight, decimals=2)) if str(np.round(self._MeasurementsLeft1.LowerLipHeight, decimals=2)) != '0' else '-')
        self.photo1Table.setItem(11, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsDeviation1.LowerLipHeight, decimals=2)) if str(np.round(self._MeasurementsDeviation1.LowerLipHeight, decimals=2)) != '0' else '-')
        self.photo1Table.setItem(11, 2, val)
        val = QtWidgets.QTableWidgetItem('-')
        self.photo1Table.setItem(11, 3, val)
        
        #Set up Column headers to show which side is which
        if self._reference_side == 'Left':
            self.photo1Table.horizontalHeaderItem(0).setText('"Affected"\nRight Side')
            self.photo1Table.horizontalHeaderItem(1).setText('Normal\nLeft Side')
        elif self._reference_side == 'Right':
            self.photo1Table.horizontalHeaderItem(0).setText('Normal\nRight Side')
            self.photo1Table.horizontalHeaderItem(1).setText('"Affected"\nLeft Side')
        
        # Connecting the selection method to the show the example photos
        pixmap = QtGui.QPixmap('./Metrics/Default.jpg')
        self.metricsLabel1.setPhoto(pixmap)
        self.metricsLabel1.update_view()

        #Set up Table
        header = self.photo1Table.horizontalHeader()       
        header.setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        header = self.photo1Table.verticalHeader()       
        header.setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.photo1Table.selectionModel().selectionChanged.connect(self.get_new_selection1)

        #####################
        #Measurements 2
        #####################
        
        #Brow Height
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsRight2.BrowHeight, decimals=2)) if str(np.round(self._MeasurementsRight2.BrowHeight, decimals=2)) != '0' else '-')
        self.photo2Table.setItem(0, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsLeft2.BrowHeight, decimals=2)) if str(np.round(self._MeasurementsLeft2.BrowHeight, decimals=2)) != '0' else '-')
        self.photo2Table.setItem(0, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsDeviation2.BrowHeight, decimals=2)) if str(np.round(self._MeasurementsDeviation2.BrowHeight, decimals=2)) != '0' else '-')
        self.photo2Table.setItem(0, 2, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsPercentual2.BrowHeight, decimals=2)) if str(np.round(self._MeasurementsPercentual2.BrowHeight, decimals=2)) != '0' else '-')
        self.photo2Table.setItem(0, 3, val)
        
        #Marginal Reflex Distance 1
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsRight2.MarginalReflexDistance1, decimals=2)) if str(np.round(self._MeasurementsRight2.MarginalReflexDistance1, decimals=2)) != '0' else '-')
        self.photo2Table.setItem(1, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsLeft2.MarginalReflexDistance1, decimals=2)) if str(np.round(self._MeasurementsLeft2.MarginalReflexDistance1, decimals=2)) != '0' else '-')
        self.photo2Table.setItem(1, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsDeviation2.MarginalReflexDistance1, decimals=2)) if str(np.round(self._MeasurementsDeviation2.MarginalReflexDistance1, decimals=2)) != '0' else '-')
        self.photo2Table.setItem(1, 2, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsPercentual2.MarginalReflexDistance1, decimals=2)) if str(np.round(self._MeasurementsPercentual2.MarginalReflexDistance1, decimals=2)) != '0' else '-')
        self.photo2Table.setItem(1, 3, val)
        
        #Marginal Reflex Distance 2
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsRight2.MarginalReflexDistance2, decimals=2)) if str(np.round(self._MeasurementsRight2.MarginalReflexDistance2, decimals=2)) != '0' else '-')
        self.photo2Table.setItem(2, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsLeft2.MarginalReflexDistance2, decimals=2)) if str(np.round(self._MeasurementsLeft2.MarginalReflexDistance2, decimals=2)) != '0' else '-')
        self.photo2Table.setItem(2, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsDeviation2.MarginalReflexDistance2, decimals=2)) if str(np.round(self._MeasurementsDeviation2.MarginalReflexDistance2, decimals=2)) != '0' else '-')
        self.photo2Table.setItem(2, 2, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsPercentual2.MarginalReflexDistance2, decimals=2)) if str(np.round(self._MeasurementsPercentual2.MarginalReflexDistance2, decimals=2)) != '0' else '-')
        self.photo2Table.setItem(2, 3, val)
        
        #Palpebral Fissure Height
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsRight2.PalpebralFissureHeight, decimals=2)) if str(np.round(self._MeasurementsRight2.PalpebralFissureHeight, decimals=2)) != '0' else '-')
        self.photo2Table.setItem(3, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsLeft2.PalpebralFissureHeight, decimals=2)) if str(np.round(self._MeasurementsLeft2.PalpebralFissureHeight, decimals=2)) != '0' else '-')
        self.photo2Table.setItem(3, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsDeviation2.PalpebralFissureHeight, decimals=2)) if str(np.round(self._MeasurementsDeviation2.PalpebralFissureHeight, decimals=2)) != '0' else '-')
        self.photo2Table.setItem(3, 2, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsPercentual2.PalpebralFissureHeight, decimals=2)) if str(np.round(self._MeasurementsPercentual2.PalpebralFissureHeight, decimals=2)) != '0' else '-')
        self.photo2Table.setItem(3, 3, val)
        
        #Eye Area
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsRight2.EyeArea, decimals=2)) if str(np.round(self._MeasurementsRight2.EyeArea, decimals=2)) != '0' else '-')
        self.photo2Table.setItem(4, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsLeft2.EyeArea, decimals=2)) if str(np.round(self._MeasurementsLeft2.EyeArea, decimals=2)) != '0' else '-')
        self.photo2Table.setItem(4, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsDeviation2.EyeArea, decimals=2)) if str(np.round(self._MeasurementsDeviation2.EyeArea, decimals=2)) != '0' else '-')
        self.photo2Table.setItem(4, 2, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsPercentual2.EyeArea, decimals=2)) if str(np.round(self._MeasurementsPercentual2.EyeArea, decimals=2)) != '0' else '-')
        self.photo2Table.setItem(4, 3, val)
        
        #NLF Angle
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsRight2.NLF_angle, decimals=2)) if str(np.round(self._MeasurementsRight2.NLF_angle, decimals=2)) != '0' else '-')
        self.photo2Table.setItem(5, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsLeft2.NLF_angle, decimals=2)) if str(np.round(self._MeasurementsLeft2.NLF_angle, decimals=2)) != '0' else '-')
        self.photo2Table.setItem(5, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsDeviation2.NLF_angle, decimals=2)) if str(np.round(self._MeasurementsDeviation2.NLF_angle, decimals=2)) != '0' else '-')
        self.photo2Table.setItem(5, 2, val)
        val = QtWidgets.QTableWidgetItem('-')
        self.photo2Table.setItem(5, 3, val)
        
        #Upper Lip Slope
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsRight2.UpperLipSlope, decimals=2)) if str(np.round(self._MeasurementsRight2.UpperLipSlope, decimals=2)) != '0' else '-')
        self.photo2Table.setItem(6, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsLeft2.UpperLipSlope, decimals=2)) if str(np.round(self._MeasurementsLeft2.UpperLipSlope, decimals=2)) != '0' else '-')
        self.photo2Table.setItem(6, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsDeviation2.UpperLipSlope, decimals=2)) if str(np.round(self._MeasurementsDeviation2.UpperLipSlope, decimals=2)) != '0' else '-')
        self.photo2Table.setItem(6, 2, val)
        val = QtWidgets.QTableWidgetItem('-')
        self.photo2Table.setItem(6, 3, val)
        
        #Commisure Height
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsRight2.CommisureHeight, decimals=2)) if str(np.round(self._MeasurementsRight2.CommisureHeight, decimals=2)) != '0' else '-')
        self.photo2Table.setItem(7, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsLeft2.CommisureHeight, decimals=2)) if str(np.round(self._MeasurementsLeft2.CommisureHeight, decimals=2)) != '0' else '-')
        self.photo2Table.setItem(7, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsDeviation2.CommisureHeight, decimals=2)) if str(np.round(self._MeasurementsDeviation2.CommisureHeight, decimals=2)) != '0' else '-')
        self.photo2Table.setItem(7, 2, val)
        val = QtWidgets.QTableWidgetItem('-')
        self.photo2Table.setItem(7, 3, val)
        
        #Dental Show
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsRight2.InterlabialDistance, decimals=2)) if str(np.round(self._MeasurementsRight2.InterlabialDistance, decimals=2)) != '0' else '-')
        self.photo2Table.setItem(8, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsLeft2.InterlabialDistance, decimals=2)) if str(np.round(self._MeasurementsLeft2.InterlabialDistance, decimals=2)) != '0' else '-')
        self.photo2Table.setItem(8, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsDeviation2.InterlabialDistance, decimals=2)) if str(np.round(self._MeasurementsDeviation2.InterlabialDistance, decimals=2)) != '0' else '-')
        self.photo2Table.setItem(8, 2, val)
        val = QtWidgets.QTableWidgetItem('-')
        self.photo2Table.setItem(8, 3, val)
        
        #Dental Show Area
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsRight2.InterlabialArea_of_the_Hemiface, decimals=2)) if str(np.round(self._MeasurementsRight2.InterlabialArea_of_the_Hemiface, decimals=2)) != '0' else '-')
        self.photo2Table.setItem(9, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsLeft2.InterlabialArea_of_the_Hemiface, decimals=2)) if str(np.round(self._MeasurementsLeft2.InterlabialArea_of_the_Hemiface, decimals=2)) != '0' else '-')
        self.photo2Table.setItem(9, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsDeviation2.InterlabialArea_of_the_Hemiface, decimals=2)) if str(np.round(self._MeasurementsDeviation2.InterlabialArea_of_the_Hemiface, decimals=2)) != '0' else '-')
        self.photo2Table.setItem(9, 2, val)
        val = QtWidgets.QTableWidgetItem('-')
        self.photo2Table.setItem(9, 3, val)
        
        #Commissure Position
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsRight2.CommissurePosition, decimals=2)) if str(np.round(self._MeasurementsRight2.CommissurePosition, decimals=2)) != '0' else '-')
        self.photo2Table.setItem(10, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsLeft2.CommissurePosition, decimals=2)) if str(np.round(self._MeasurementsLeft2.CommissurePosition, decimals=2)) != '0' else '-')
        self.photo2Table.setItem(10, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsDeviation2.CommissurePosition, decimals=2)) if str(np.round(self._MeasurementsDeviation2.CommissurePosition, decimals=2)) != '0' else '-')
        self.photo2Table.setItem(10, 2, val)
        val = QtWidgets.QTableWidgetItem('-')
        self.photo2Table.setItem(10, 3, val)
        
        #Lower Lip Height Deviation
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsRight2.LowerLipHeight, decimals=2)) if str(np.round(self._MeasurementsRight2.LowerLipHeight, decimals=2)) != '0' else '-')
        self.photo2Table.setItem(11, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsLeft2.LowerLipHeight, decimals=2)) if str(np.round(self._MeasurementsLeft2.LowerLipHeight, decimals=2)) != '0' else '-')
        self.photo2Table.setItem(11, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementsDeviation2.LowerLipHeight, decimals=2)) if str(np.round(self._MeasurementsDeviation2.LowerLipHeight, decimals=2)) != '0' else '-')
        self.photo2Table.setItem(11, 2, val)
        val = QtWidgets.QTableWidgetItem('-')
        self.photo2Table.setItem(11, 3, val)
        
        #Set up Column headers to show which side is which
        if self._reference_side == 'Left':
            self.photo2Table.horizontalHeaderItem(0).setText('"Affected"\nRight Side')
            self.photo2Table.horizontalHeaderItem(1).setText('Normal\nLeft Side')
        elif self._reference_side == 'Right':
            self.photo2Table.horizontalHeaderItem(0).setText('Normal\nRight Side')
            self.photo2Table.horizontalHeaderItem(1).setText('"Affected"\nLeft Side')
        
        #Connecting the selection method to the show the example photos
        pixmap = QtGui.QPixmap('./Metrics/Default.jpg')
        self.metricsLabel2.setPhoto(pixmap)
        self.metricsLabel2.update_view()

        #Set up Table
        header = self.photo2Table.horizontalHeader()       
        header.setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        header = self.photo2Table.verticalHeader()       
        header.setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.photo2Table.selectionModel().selectionChanged.connect(self.get_new_selection2)
        
        #####################
        #Measurements 3
        #####################
        
        #Brow Height
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementRightComparison.BrowHeight, decimals=2)) if str(np.round(self._MeasurementRightComparison.BrowHeight, decimals=2)) != '0' else '-')
        self.sideTable.setItem(0, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementRightPercentComparison.BrowHeight, decimals=2)) if str(np.round(self._MeasurementRightPercentComparison.BrowHeight, decimals=2)) != '0' else '-')
        self.sideTable.setItem(0, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementLeftComparison.BrowHeight, decimals=2)) if str(np.round(self._MeasurementLeftComparison.BrowHeight, decimals=2)) != '0' else '-')
        self.sideTable.setItem(0, 2, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementLeftPercentComparison.BrowHeight, decimals=2)) if str(np.round(self._MeasurementLeftPercentComparison.BrowHeight, decimals=2)) != '0' else '-')
        self.sideTable.setItem(0, 3, val)
        
        #Marginal Reflex Distance 1
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementRightComparison.MarginalReflexDistance1, decimals=2)) if str(np.round(self._MeasurementRightComparison.MarginalReflexDistance1, decimals=2)) != '0' else '-')
        self.sideTable.setItem(1, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementRightPercentComparison.MarginalReflexDistance1, decimals=2)) if str(np.round(self._MeasurementRightPercentComparison.MarginalReflexDistance1, decimals=2)) != '0' else '-')
        self.sideTable.setItem(1, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementLeftComparison.MarginalReflexDistance1, decimals=2)) if str(np.round(self._MeasurementLeftComparison.MarginalReflexDistance1, decimals=2)) != '0' else '-')
        self.sideTable.setItem(1, 2, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementLeftPercentComparison.MarginalReflexDistance1, decimals=2)) if str(np.round(self._MeasurementLeftPercentComparison.MarginalReflexDistance1, decimals=2)) != '0' else '-')
        self.sideTable.setItem(1, 3, val)
        
        #Marginal Reflex Distance 2
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementRightComparison.MarginalReflexDistance2, decimals=2)) if str(np.round(self._MeasurementRightComparison.MarginalReflexDistance2, decimals=2)) != '0' else '-')
        self.sideTable.setItem(2, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementRightPercentComparison.MarginalReflexDistance2, decimals=2)) if str(np.round(self._MeasurementRightPercentComparison.MarginalReflexDistance2, decimals=2)) != '0' else '-')
        self.sideTable.setItem(2, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementLeftComparison.MarginalReflexDistance2, decimals=2)) if str(np.round(self._MeasurementLeftComparison.MarginalReflexDistance2, decimals=2)) != '0' else '-')
        self.sideTable.setItem(2, 2, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementLeftPercentComparison.MarginalReflexDistance2, decimals=2)) if str(np.round(self._MeasurementLeftPercentComparison.MarginalReflexDistance2, decimals=2)) != '0' else '-')
        self.sideTable.setItem(2, 3, val)
        
        #Palpebral Fissure Height
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementRightComparison.PalpebralFissureHeight, decimals=2)) if str(np.round(self._MeasurementRightComparison.PalpebralFissureHeight, decimals=2)) != '0' else '-')
        self.sideTable.setItem(3, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementRightPercentComparison.PalpebralFissureHeight, decimals=2)) if str(np.round(self._MeasurementRightPercentComparison.PalpebralFissureHeight, decimals=2)) != '0' else '-')
        self.sideTable.setItem(3, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementLeftComparison.PalpebralFissureHeight, decimals=2)) if str(np.round(self._MeasurementLeftComparison.PalpebralFissureHeight, decimals=2)) != '0' else '-')
        self.sideTable.setItem(3, 2, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementLeftPercentComparison.PalpebralFissureHeight, decimals=2)) if str(np.round(self._MeasurementLeftPercentComparison.PalpebralFissureHeight, decimals=2)) != '0' else '-')
        self.sideTable.setItem(3, 3, val)
        
        #Eye Area
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementRightComparison.EyeArea, decimals=2)) if str(np.round(self._MeasurementRightComparison.EyeArea, decimals=2)) != '0' else '-')
        self.sideTable.setItem(4, 0, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementRightPercentComparison.EyeArea, decimals=2)) if str(np.round(self._MeasurementRightPercentComparison.EyeArea, decimals=2)) != '0' else '-')
        self.sideTable.setItem(4, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementLeftComparison.EyeArea, decimals=2)) if str(np.round(self._MeasurementLeftComparison.EyeArea, decimals=2)) != '0' else '-')
        self.sideTable.setItem(4, 2, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementLeftPercentComparison.EyeArea, decimals=2)) if str(np.round(self._MeasurementLeftPercentComparison.EyeArea, decimals=2)) != '0' else '-')
        self.sideTable.setItem(4, 3, val)
        
        #NLF Angle
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementRightComparison.NLF_angle, decimals=2)) if str(np.round(self._MeasurementRightComparison.NLF_angle, decimals=2)) != '0' else '-')
        self.sideTable.setItem(5, 0, val)
        val = QtWidgets.QTableWidgetItem('-')
        self.sideTable.setItem(5, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementLeftComparison.NLF_angle, decimals=2)) if str(np.round(self._MeasurementLeftComparison.NLF_angle, decimals=2)) != '0' else '-')
        self.sideTable.setItem(5, 2, val)
        val = QtWidgets.QTableWidgetItem('-')
        self.sideTable.setItem(5, 3, val)
        
        #Upper Lip Slope
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementRightComparison.UpperLipSlope, decimals=2)) if str(np.round(self._MeasurementRightComparison.UpperLipSlope, decimals=2)) != '0' else '-')
        self.sideTable.setItem(6, 0, val)
        val = QtWidgets.QTableWidgetItem('-')
        self.sideTable.setItem(6, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementLeftComparison.UpperLipSlope, decimals=2)) if str(np.round(self._MeasurementLeftComparison.UpperLipSlope, decimals=2)) != '0' else '-')
        self.sideTable.setItem(6, 2, val)
        val = QtWidgets.QTableWidgetItem('-')
        self.sideTable.setItem(6, 3, val)
        
        #Commisure Height
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementRightComparison.CommisureHeight, decimals=2)) if str(np.round(self._MeasurementRightComparison.CommisureHeight, decimals=2)) != '0' else '-')
        self.sideTable.setItem(7, 0, val)
        val = QtWidgets.QTableWidgetItem('-')
        self.sideTable.setItem(7, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementLeftComparison.CommisureHeight, decimals=2)) if str(np.round(self._MeasurementLeftComparison.CommisureHeight, decimals=2)) != '0' else '-')
        self.sideTable.setItem(7, 2, val)
        val = QtWidgets.QTableWidgetItem('-')
        self.sideTable.setItem(7, 3, val)
        
        #Interlabial Distance
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementRightComparison.InterlabialDistance, decimals=2)) if str(np.round(self._MeasurementRightComparison.InterlabialDistance, decimals=2)) != '0' else '-')
        self.sideTable.setItem(8, 0, val)
        val = QtWidgets.QTableWidgetItem('-')
        self.sideTable.setItem(8, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementLeftComparison.InterlabialDistance, decimals=2)) if str(np.round(self._MeasurementLeftComparison.InterlabialDistance, decimals=2)) != '0' else '-')
        self.sideTable.setItem(8, 2, val)
        val = QtWidgets.QTableWidgetItem('-')
        self.sideTable.setItem(8, 3, val)
        
        #Interlabial Area of the Hemiface
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementRightComparison.InterlabialArea_of_the_Hemiface, decimals=2)) if str(np.round(self._MeasurementRightComparison.InterlabialArea_of_the_Hemiface, decimals=2)) != '0' else '-')
        self.sideTable.setItem(9, 0, val)
        val = QtWidgets.QTableWidgetItem('-')
        self.sideTable.setItem(9, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementLeftComparison.InterlabialArea_of_the_Hemiface, decimals=2)) if str(np.round(self._MeasurementLeftComparison.InterlabialArea_of_the_Hemiface, decimals=2)) != '0' else '-')
        self.sideTable.setItem(9, 2, val)
        val = QtWidgets.QTableWidgetItem('-')
        self.sideTable.setItem(9, 3, val)
        
        #Commissure Position
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementRightComparison.CommissurePosition, decimals=2)) if str(np.round(self._MeasurementRightComparison.CommissurePosition, decimals=2)) != '0' else '-')
        self.sideTable.setItem(10, 0, val)
        val = QtWidgets.QTableWidgetItem('-')
        self.sideTable.setItem(10, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementLeftComparison.CommissurePosition, decimals=2)) if str(np.round(self._MeasurementLeftComparison.CommissurePosition, decimals=2)) != '0' else '-')
        self.sideTable.setItem(10, 2, val)
        val = QtWidgets.QTableWidgetItem('-')
        self.sideTable.setItem(10, 3, val)
        
        #Lower Lip Height
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementRightComparison.LowerLipHeight, decimals=2)) if str(np.round(self._MeasurementRightComparison.LowerLipHeight, decimals=2)) != '0' else '-')
        self.sideTable.setItem(11, 0, val)
        val = QtWidgets.QTableWidgetItem('-')
        self.sideTable.setItem(11, 1, val)
        val = QtWidgets.QTableWidgetItem(str(np.round(self._MeasurementLeftComparison.LowerLipHeight, decimals=2)) if str(np.round(self._MeasurementLeftComparison.LowerLipHeight, decimals=2)) != '0' else '-')
        self.sideTable.setItem(11, 2, val)
        val = QtWidgets.QTableWidgetItem('-')
        self.sideTable.setItem(11, 3, val)
        
        #Set up Column headers to show which side is which
        if self._reference_side == 'Left':
            self.sideTable.horizontalHeaderItem(0).setText('"Affected" (Right) Side \nAbsolute Differences')
            self.sideTable.horizontalHeaderItem(1).setText('"Affected" (Right) Side \nPercentage Differences')
            self.sideTable.horizontalHeaderItem(2).setText('Normal (Left) Side \nAbsolute Differences')
            self.sideTable.horizontalHeaderItem(3).setText('Normal (Left) Side \nPercentage Differences')
        elif self._reference_side == 'Right':
            self.sideTable.horizontalHeaderItem(0).setText('Normal (Right) Side \nAbsolute Differences')
            self.sideTable.horizontalHeaderItem(1).setText('Normal (Right) Side \nPercentage Differences')
            self.sideTable.horizontalHeaderItem(2).setText('"Affected" (Left) Side \nAbsolute Differences')
            self.sideTable.horizontalHeaderItem(3).setText('"Affected" (Left) Side \nPercentage Differences')
        
        # Connecting the selection method to the show the example photos
        pixmap = QtGui.QPixmap('./Metrics/Default.jpg')
        self.metricsLabel3.setPhoto(pixmap)
        self.metricsLabel3.update_view()

        #Set up Table
        header = self.sideTable.horizontalHeader()       
        header.setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        header = self.sideTable.verticalHeader()       
        header.setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.sideTable.selectionModel().selectionChanged.connect(self.get_new_selection3)

    def headerClicked1(self):
        row = self.photo1Table.currentItem().row()
        selectedName = self.photo1Table.verticalHeaderItem(row)
        metricName = selectedName.text()
        print(f'metricName = {metricName}')
         
    def get_new_selection1(self, selected, deselected):
        """This function is for when the user selects a item on the table 
        which will show a picture of an example"""
        for i in selected.indexes():
            if i.row() == 0:
                pixmap = QtGui.QPixmap('./Metrics/Brow_Height.jpg')
                self.metricsLabel1.setPhoto(pixmap)
                self.metricsLabel1.update_view()
            elif i.row() == 1:
                pixmap = QtGui.QPixmap('./Metrics/Marginal_Reflex_Distance_1.jpg')
                self.metricsLabel1.setPhoto(pixmap)
                self.metricsLabel1.update_view()
            elif i.row() == 2:
                pixmap = QtGui.QPixmap('./Metrics/Marginal_Reflex_Distance_2.jpg')
                self.metricsLabel1.setPhoto(pixmap)
                self.metricsLabel1.update_view()
            elif i.row() == 3:
                pixmap = QtGui.QPixmap('./Metrics/palpebral_fissure_width.jpg')
                self.metricsLabel1.setPhoto(pixmap)
                self.metricsLabel1.update_view()
            elif i.row() == 4:
                pixmap = QtGui.QPixmap('./Metrics/Eye_Area.jpg')
                self.metricsLabel1.setPhoto(pixmap)
                self.metricsLabel1.update_view()
            elif i.row() == 5:
                pixmap = QtGui.QPixmap('./Metrics/Nasolabial_Fold_Angle.jpg')
                self.metricsLabel1.setPhoto(pixmap)
                self.metricsLabel1.update_view()
            elif i.row() == 6:
                pixmap = QtGui.QPixmap('./Metrics/upper_lip_slope.jpg')
                self.metricsLabel1.setPhoto(pixmap)
                self.metricsLabel1.update_view()
            elif i.row() == 7:
                pixmap = QtGui.QPixmap('./Metrics/commissure_height.jpg')
                self.metricsLabel1.setPhoto(pixmap)
                self.metricsLabel1.update_view()
            elif i.row() == 8:
                pixmap = QtGui.QPixmap('./Metrics/interlabial_distance.jpg')
                self.metricsLabel1.setPhoto(pixmap)
                self.metricsLabel1.update_view()
            elif i.row() == 9:
                pixmap = QtGui.QPixmap('./Metrics/interlabial_area_of_the_hemiface.jpg')
                self.metricsLabel1.setPhoto(pixmap)
                self.metricsLabel1.update_view()
            elif i.row() == 10:
                pixmap = QtGui.QPixmap('./Metrics/commissure_position.jpg')
                self.metricsLabel1.setPhoto(pixmap)
                self.metricsLabel1.update_view()
            elif i.row() == 11:
                pixmap = QtGui.QPixmap('./Metrics/lower_lip_height.jpg')
                self.metricsLabel1.setPhoto(pixmap)
                self.metricsLabel1.update_view()
            

    def get_new_selection2(self, selected, deselected):
        """This function is for when the user selects a item on the table 
        which will show a picture of an example"""
        for i in selected.indexes():
            if i.row() == 0:
                pixmap = QtGui.QPixmap('./Metrics/Brow_Height.jpg')
                self.metricsLabel2.setPhoto(pixmap)
                self.metricsLabel2.update_view()
            elif i.row() == 1:
                pixmap = QtGui.QPixmap('./Metrics/Marginal_Reflex_Distance_1.jpg')
                self.metricsLabel2.setPhoto(pixmap)
                self.metricsLabel2.update_view()
            elif i.row() == 2:
                pixmap = QtGui.QPixmap('./Metrics/Marginal_Reflex_Distance_2.jpg')
                self.metricsLabel2.setPhoto(pixmap)
                self.metricsLabel2.update_view()
            elif i.row() == 3:
                pixmap = QtGui.QPixmap('./Metrics/palpebral_fissure_width.jpg')
                self.metricsLabel2.setPhoto(pixmap)
                self.metricsLabel2.update_view()
            elif i.row() == 4:
                pixmap = QtGui.QPixmap('./Metrics/Eye_Area.jpg')
                self.metricsLabel2.setPhoto(pixmap)
                self.metricsLabel2.update_view()
            elif i.row() == 5:
                pixmap = QtGui.QPixmap('./Metrics/Nasolabial_Fold_Angle.jpg')
                self.metricsLabel2.setPhoto(pixmap)
                self.metricsLabel2.update_view()
            elif i.row() == 6:
                pixmap = QtGui.QPixmap('./Metrics/upper_lip_slope.jpg')
                self.metricsLabel2.setPhoto(pixmap)
                self.metricsLabel2.update_view()
            elif i.row() == 7:
                pixmap = QtGui.QPixmap('./Metrics/commissure_height.jpg')
                self.metricsLabel2.setPhoto(pixmap)
                self.metricsLabel2.update_view()
            elif i.row() == 8:
                pixmap = QtGui.QPixmap('./Metrics/interlabial_distance.jpg')
                self.metricsLabel2.setPhoto(pixmap)
                self.metricsLabel2.update_view()
            elif i.row() == 9:
                pixmap = QtGui.QPixmap('./Metrics/interlabial_area_of_the_hemiface.jpg')
                self.metricsLabel2.setPhoto(pixmap)
                self.metricsLabel2.update_view()
            elif i.row() == 10:
                pixmap = QtGui.QPixmap('./Metrics/commissure_position.jpg')
                self.metricsLabel2.setPhoto(pixmap)
                self.metricsLabel2.update_view()
            elif i.row() == 11:
                pixmap = QtGui.QPixmap('./Metrics/lower_lip_height.jpg')
                self.metricsLabel2.setPhoto(pixmap)
                self.metricsLabel2.update_view()
            
    
         
    def get_new_selection3(self, selected, deselected):
        """This function is for when the user selects a item on the table 
        which will show a picture of an example"""
        for i in selected.indexes():
            if i.row() == 0:
                pixmap = QtGui.QPixmap('./Metrics/Brow_Height.jpg')
                self.metricsLabel3.setPhoto(pixmap)
                self.metricsLabel3.update_view()
            elif i.row() == 1:
                pixmap = QtGui.QPixmap('./Metrics/Marginal_Reflex_Distance_1.jpg')
                self.metricsLabel3.setPhoto(pixmap)
                self.metricsLabel3.update_view()
            elif i.row() == 2:
                pixmap = QtGui.QPixmap('./Metrics/Marginal_Reflex_Distance_2.jpg')
                self.metricsLabel3.setPhoto(pixmap)
                self.metricsLabel3.update_view()
            elif i.row() == 3:
                pixmap = QtGui.QPixmap('./Metrics/palpebral_fissure_width.jpg')
                self.metricsLabel3.setPhoto(pixmap)
                self.metricsLabel3.update_view()
            elif i.row() == 4:
                pixmap = QtGui.QPixmap('./Metrics/Eye_Area.jpg')
                self.metricsLabel3.setPhoto(pixmap)
                self.metricsLabel3.update_view()
            elif i.row() == 5:
                pixmap = QtGui.QPixmap('./Metrics/Nasolabial_Fold_Angle.jpg')
                self.metricsLabel3.setPhoto(pixmap)
                self.metricsLabel3.update_view()
            elif i.row() == 6:
                pixmap = QtGui.QPixmap('./Metrics/upper_lip_slope.jpg')
                self.metricsLabel3.setPhoto(pixmap)
                self.metricsLabel3.update_view()
            elif i.row() == 7:
                pixmap = QtGui.QPixmap('./Metrics/commissure_height.jpg')
                self.metricsLabel3.setPhoto(pixmap)
                self.metricsLabel3.update_view()
            elif i.row() == 8:
                pixmap = QtGui.QPixmap('./Metrics/interlabial_distance.jpg')
                self.metricsLabel3.setPhoto(pixmap)
                self.metricsLabel3.update_view()
            elif i.row() == 9:
                pixmap = QtGui.QPixmap('./Metrics/interlabial_area_of_the_hemiface.jpg')
                self.metricsLabel3.setPhoto(pixmap)
                self.metricsLabel3.update_view()
            elif i.row() == 10:
                pixmap = QtGui.QPixmap('./Metrics/commissure_position.jpg')
                self.metricsLabel3.setPhoto(pixmap)
                self.metricsLabel3.update_view()
            elif i.row() == 11:
                pixmap = QtGui.QPixmap('./Metrics/lower_lip_height.jpg')
                self.metricsLabel3.setPhoto(pixmap)
                self.metricsLabel3.update_view()
            




    def getOneSideComparison(self):
        self._MeasurementLeftComparison = FaceMeasurementsSide()
        self._MeasurementRightComparison = FaceMeasurementsSide()
        self._MeasurementLeftPercentComparison = FaceMeasurementsSide()
        self._MeasurementRightPercentComparison = FaceMeasurementsSide()

        #Left Side Comparison
        self._MeasurementLeftComparison.BrowHeight = abs(self._MeasurementsLeft2.BrowHeight - self._MeasurementsLeft1.BrowHeight)
        self._MeasurementLeftComparison.MarginalReflexDistance1 = abs(self._MeasurementsLeft2.MarginalReflexDistance1 - self._MeasurementsLeft1.MarginalReflexDistance1)
        self._MeasurementLeftComparison.MarginalReflexDistance2 = abs(self._MeasurementsLeft2.MarginalReflexDistance2 - self._MeasurementsLeft1.MarginalReflexDistance2)
        self._MeasurementLeftComparison.PalpebralFissureHeight = abs(self._MeasurementsLeft2.PalpebralFissureHeight - self._MeasurementsLeft1.PalpebralFissureHeight)
        self._MeasurementLeftComparison.EyeArea = abs(self._MeasurementsLeft2.EyeArea - self._MeasurementsLeft1.EyeArea)
        self._MeasurementLeftComparison.NLF_angle = abs(self._MeasurementsLeft2.NLF_angle - self._MeasurementsLeft1.NLF_angle)
        self._MeasurementLeftComparison.UpperLipSlope = abs(self._MeasurementsLeft2.UpperLipSlope - self._MeasurementsLeft1.UpperLipSlope)
        self._MeasurementLeftComparison.CommisureHeight = abs(self._MeasurementsLeft2.CommisureHeight - self._MeasurementsLeft1.CommisureHeight)
        self._MeasurementLeftComparison.InterlabialDistance = abs(self._MeasurementsLeft2.InterlabialDistance - self._MeasurementsLeft1.InterlabialDistance)
        self._MeasurementLeftComparison.InterlabialArea_of_the_Hemiface = abs(self._MeasurementsLeft2.InterlabialArea_of_the_Hemiface - self._MeasurementsLeft1.InterlabialArea_of_the_Hemiface)
        self._MeasurementLeftComparison.CommissurePosition = abs(self._MeasurementsLeft2.CommissurePosition - self._MeasurementsLeft1.CommissurePosition)
        self._MeasurementLeftComparison.LowerLipHeight = abs(self._MeasurementsLeft2.LowerLipHeight - self._MeasurementsLeft1.LowerLipHeight)

        #Right Side Comparison
        self._MeasurementRightComparison.BrowHeight = abs(self._MeasurementsRight2.BrowHeight - self._MeasurementsRight1.BrowHeight)
        self._MeasurementRightComparison.MarginalReflexDistance1 = abs(self._MeasurementsRight2.MarginalReflexDistance1 - self._MeasurementsRight1.MarginalReflexDistance1)
        self._MeasurementRightComparison.MarginalReflexDistance2 = abs(self._MeasurementsRight2.MarginalReflexDistance2 - self._MeasurementsRight1.MarginalReflexDistance2)
        self._MeasurementRightComparison.PalpebralFissureHeight = abs(self._MeasurementsRight2.PalpebralFissureHeight - self._MeasurementsRight1.PalpebralFissureHeight)
        self._MeasurementRightComparison.EyeArea = abs(self._MeasurementsRight2.EyeArea - self._MeasurementsRight1.EyeArea)
        self._MeasurementRightComparison.NLF_angle = abs(self._MeasurementsRight2.NLF_angle - self._MeasurementsRight1.NLF_angle)
        self._MeasurementRightComparison.UpperLipSlope = abs(self._MeasurementsRight2.UpperLipSlope - self._MeasurementsRight1.UpperLipSlope)
        self._MeasurementRightComparison.CommisureHeight = abs(self._MeasurementsRight2.CommisureHeight - self._MeasurementsRight1.CommisureHeight)
        self._MeasurementRightComparison.InterlabialDistance = abs(self._MeasurementsRight2.InterlabialDistance - self._MeasurementsRight1.InterlabialDistance)
        self._MeasurementRightComparison.InterlabialArea_of_the_Hemiface = abs(self._MeasurementsRight2.InterlabialArea_of_the_Hemiface - self._MeasurementsRight1.InterlabialArea_of_the_Hemiface)
        self._MeasurementRightComparison.CommissurePosition = abs(self._MeasurementsRight2.CommissurePosition - self._MeasurementsRight1.CommissurePosition)
        self._MeasurementRightComparison.LowerLipHeight = abs(self._MeasurementsRight2.LowerLipHeight - self._MeasurementsRight1.LowerLipHeight)


        #Left Side Percent Comparison
        #BrowHeight
        self._MeasurementLeftPercentComparison.BrowHeight = abs(self._MeasurementsLeft2.BrowHeight - self._MeasurementsLeft1.BrowHeight)*100/self._MeasurementsLeft1.BrowHeight
        #MarginalReflexDistance1
        if self._MeasurementsLeft1.MarginalReflexDistance1 > 0:
            self._MeasurementLeftPercentComparison.MarginalReflexDistance1 = abs(self._MeasurementsLeft2.MarginalReflexDistance1 - self._MeasurementsLeft1.MarginalReflexDistance1)*100/self._MeasurementsLeft1.MarginalReflexDistance1
        else:
            self._MeasurementLeftPercentComparison.MarginalReflexDistance1 = 0
        #MarginalReflexDistance2
        if self._MeasurementsLeft1.MarginalReflexDistance2 > 0:
            self._MeasurementLeftPercentComparison.MarginalReflexDistance2 = abs(self._MeasurementsLeft2.MarginalReflexDistance2 - self._MeasurementsLeft1.MarginalReflexDistance2)*100/self._MeasurementsLeft1.MarginalReflexDistance2
        else:
            self._MeasurementLeftPercentComparison.MarginalReflexDistance2 = 0
        #PalpebralFissureHeight
        if self._MeasurementsLeft1.PalpebralFissureHeight > 0:
            self._MeasurementLeftPercentComparison.PalpebralFissureHeight = abs(self._MeasurementsLeft2.PalpebralFissureHeight - self._MeasurementsLeft1.PalpebralFissureHeight)*100/self._MeasurementsLeft1.PalpebralFissureHeight
        else:
            self._MeasurementLeftPercentComparison.PalpebralFissureHeight = 0
        #EyeArea
        if self._MeasurementsLeft1.EyeArea > 0:
            self._MeasurementLeftPercentComparison.EyeArea = abs(self._MeasurementsLeft2.EyeArea - self._MeasurementsLeft1.EyeArea)*100/self._MeasurementsLeft1.EyeArea
        else:
            self._MeasurementLeftPercentComparison.EyeArea = 0
        #NLF_angle
        if self._MeasurementsLeft1.NLF_angle > 0:
            self._MeasurementLeftPercentComparison.NLF_angle = abs(self._MeasurementsLeft2.NLF_angle - self._MeasurementsLeft1.NLF_angle)*100/self._MeasurementsLeft1.NLF_angle
        else:
            self._MeasurementLeftPercentComparison.NLF_angle = 0
        #UpperLipSlope
        if self._MeasurementsLeft1.UpperLipSlope > 0:
            self._MeasurementLeftPercentComparison.UpperLipSlope = abs(self._MeasurementsLeft2.UpperLipSlope - self._MeasurementsLeft1.UpperLipSlope)*100/self._MeasurementsLeft1.UpperLipSlope
        else:
            self._MeasurementLeftPercentComparison.UpperLipSlope = 0
        #CommisureHeight
        if self._MeasurementsLeft1.CommisureHeight > 0:    
            self._MeasurementLeftPercentComparison.CommisureHeight = abs(self._MeasurementsLeft2.CommisureHeight - self._MeasurementsLeft1.CommisureHeight)*100/self._MeasurementsLeft1.CommisureHeight
        else:
            self._MeasurementLeftPercentComparison.CommisureHeight = 0
        #InterlabialDistance
        if self._MeasurementsLeft1.InterlabialDistance > 0:
            self._MeasurementLeftPercentComparison.InterlabialDistance = abs(self._MeasurementsLeft2.InterlabialDistance - self._MeasurementsLeft1.InterlabialDistance)*100/self._MeasurementsLeft1.InterlabialDistance
        else:
            self._MeasurementLeftPercentComparison.InterlabialDistance = 0
        #InterlabialArea_of_the_Hemiface
        if self._MeasurementsLeft1.InterlabialArea_of_the_Hemiface > 0:
            self._MeasurementLeftPercentComparison.InterlabialArea_of_the_Hemiface = abs(self._MeasurementsLeft2.InterlabialArea_of_the_Hemiface - self._MeasurementsLeft1.InterlabialArea_of_the_Hemiface)*100/self._MeasurementsLeft1.InterlabialArea_of_the_Hemiface
        else:
            self._MeasurementLeftPercentComparison.InterlabialArea_of_the_Hemiface = 0
        #CommissurePosition
        self._MeasurementLeftPercentComparison.CommissurePosition = abs(self._MeasurementsLeft2.CommissurePosition - self._MeasurementsLeft1.CommissurePosition)*100/self._MeasurementsLeft1.CommissurePosition
        #LowerLipHeight
        self._MeasurementLeftPercentComparison.LowerLipHeight = abs(self._MeasurementsLeft2.LowerLipHeight - self._MeasurementsLeft1.LowerLipHeight)*100/self._MeasurementsLeft1.LowerLipHeight


        #Right Side Percent Comparison
        #BrowHeight
        self._MeasurementRightPercentComparison.BrowHeight = abs(self._MeasurementsRight2.BrowHeight - self._MeasurementsRight1.BrowHeight)*100/self._MeasurementsRight1.BrowHeight
        #MarginalReflexDistance1
        if self._MeasurementsRight1.MarginalReflexDistance1 > 0:
            self._MeasurementRightPercentComparison.MarginalReflexDistance1 = abs(self._MeasurementsRight2.MarginalReflexDistance1 - self._MeasurementsRight1.MarginalReflexDistance1)*100/self._MeasurementsRight1.MarginalReflexDistance1
        else:
            self._MeasurementRightPercentComparison.MarginalReflexDistance1 = 0
        #MarginalReflexDistance2
        if self._MeasurementsRight1.MarginalReflexDistance2 > 0:
            self._MeasurementRightPercentComparison.MarginalReflexDistance2 = abs(self._MeasurementsRight2.MarginalReflexDistance2 - self._MeasurementsRight1.MarginalReflexDistance2)*100/self._MeasurementsRight1.MarginalReflexDistance2
        else:
            self._MeasurementRightPercentComparison.MarginalReflexDistance2 = 0
        #PalpebralFissureHeight
        if self._MeasurementsRight1.PalpebralFissureHeight > 0:
            self._MeasurementRightPercentComparison.PalpebralFissureHeight = abs(self._MeasurementsRight2.PalpebralFissureHeight - self._MeasurementsRight1.PalpebralFissureHeight)*100/self._MeasurementsRight1.PalpebralFissureHeight
        else:
            self._MeasurementRightPercentComparison.PalpebralFissureHeight = 0
        #EyeArea
        if self._MeasurementsRight1.EyeArea > 0:
            self._MeasurementRightPercentComparison.EyeArea = abs(self._MeasurementsRight2.EyeArea - self._MeasurementsRight1.EyeArea)*100/self._MeasurementsRight1.EyeArea
        else:
            self._MeasurementRightPercentComparison.EyeArea = 0
        #NLF_angle
        if self._MeasurementsRight1.NLF_angle > 0:
            self._MeasurementRightPercentComparison.NLF_angle = abs(self._MeasurementsRight2.NLF_angle - self._MeasurementsRight1.NLF_angle)*100/self._MeasurementsRight1.NLF_angle
        else:
            self._MeasurementRightPercentComparison.NLF_angle = 0
        #UpperLipSlope
        if self._MeasurementsRight1.UpperLipSlope > 0:
            self._MeasurementRightPercentComparison.UpperLipSlope = abs(self._MeasurementsRight2.UpperLipSlope - self._MeasurementsRight1.UpperLipSlope)*100/self._MeasurementsRight1.UpperLipSlope
        else:
            self._MeasurementRightPercentComparison.UpperLipSlope = 0
        #CommisureHeight
        if self._MeasurementsRight1.CommisureHeight > 0:    
            self._MeasurementRightPercentComparison.CommisureHeight = abs(self._MeasurementsRight2.CommisureHeight - self._MeasurementsRight1.CommisureHeight)*100/self._MeasurementsRight1.CommisureHeight
        else:
            self._MeasurementRightPercentComparison.CommisureHeight = 0
        #InterlabialDistance
        if self._MeasurementsRight1.InterlabialDistance > 0:
            self._MeasurementRightPercentComparison.InterlabialDistance = abs(self._MeasurementsRight2.InterlabialDistance - self._MeasurementsRight1.InterlabialDistance)*100/self._MeasurementsRight1.InterlabialDistance
        else:
            self._MeasurementRightPercentComparison.InterlabialDistance = 0
        #InterlabialArea_of_the_Hemiface
        if self._MeasurementsRight1.InterlabialArea_of_the_Hemiface > 0:
            self._MeasurementRightPercentComparison.InterlabialArea_of_the_Hemiface = abs(self._MeasurementsRight2.InterlabialArea_of_the_Hemiface - self._MeasurementsRight1.InterlabialArea_of_the_Hemiface)*100/self._MeasurementsRight1.InterlabialArea_of_the_Hemiface
        else:
            self._MeasurementRightPercentComparison.InterlabialArea_of_the_Hemiface = 0
        #CommissurePosition
        self._MeasurementRightPercentComparison.CommissurePosition = abs(self._MeasurementsRight2.CommissurePosition - self._MeasurementsRight1.CommissurePosition)*100/self._MeasurementsRight1.CommissurePosition
        #LowerLipHeight
        self._MeasurementRightPercentComparison.LowerLipHeight = abs(self._MeasurementsRight2.LowerLipHeight - self._MeasurementsRight1.LowerLipHeight)*100/self._MeasurementsRight1.LowerLipHeight


    def getTwoSideComparison(self):
        self._MeasurementStateComparison = FaceMeasurementsDeviation()
        self._MeasurementStatePercentComparison = FaceMeasurementsDeviation()

        #Two Side Comparison
        self._MeasurementStateComparison.BrowHeight = abs(self._MeasurementsDeviation2.BrowHeight - self._MeasurementsDeviation1.BrowHeight)
        self._MeasurementStateComparison.MarginalReflexDistance1 = abs(self._MeasurementsDeviation2.MarginalReflexDistance1 - self._MeasurementsDeviation1.MarginalReflexDistance1)
        self._MeasurementStateComparison.MarginalReflexDistance2 = abs(self._MeasurementsDeviation2.MarginalReflexDistance2 - self._MeasurementsDeviation1.MarginalReflexDistance2)
        self._MeasurementStateComparison.PalpebralFissureHeight = abs(self._MeasurementsDeviation2.PalpebralFissureHeight - self._MeasurementsDeviation1.PalpebralFissureHeight)
        self._MeasurementStateComparison.EyeArea = abs(self._MeasurementsDeviation2.EyeArea - self._MeasurementsDeviation1.EyeArea)
        self._MeasurementStateComparison.NLF_angle = abs(self._MeasurementsDeviation2.NLF_angle - self._MeasurementsDeviation1.NLF_angle)
        self._MeasurementStateComparison.UpperLipSlope = abs(self._MeasurementsDeviation2.UpperLipSlope - self._MeasurementsDeviation1.UpperLipSlope)
        self._MeasurementStateComparison.CommisureHeight = abs(self._MeasurementsDeviation2.CommisureHeight - self._MeasurementsDeviation1.CommisureHeight)
        self._MeasurementStateComparison.InterlabialDistance = abs(self._MeasurementsDeviation2.InterlabialDistance - self._MeasurementsDeviation1.InterlabialDistance)
        self._MeasurementStateComparison.InterlabialArea_of_the_Hemiface = abs(self._MeasurementsDeviation2.InterlabialArea_of_the_Hemiface - self._MeasurementsDeviation1.InterlabialArea_of_the_Hemiface)
        self._MeasurementStateComparison.CommissurePosition = abs(self._MeasurementsDeviation2.CommissurePosition - self._MeasurementsDeviation1.CommissurePosition)
        self._MeasurementStateComparison.LowerLipHeight = abs(self._MeasurementsDeviation2.LowerLipHeight - self._MeasurementsDeviation1.LowerLipHeight)

        #Two Side Percent Comparison
        self._MeasurementStatePercentComparison.BrowHeight = abs(self._MeasurementsPercentual2.BrowHeight - self._MeasurementsPercentual1.BrowHeight)
        self._MeasurementStatePercentComparison.MarginalReflexDistance1 = abs(self._MeasurementsPercentual2.MarginalReflexDistance1 - self._MeasurementsPercentual1.MarginalReflexDistance1)
        self._MeasurementStatePercentComparison.MarginalReflexDistance2 = abs(self._MeasurementsPercentual2.MarginalReflexDistance2 - self._MeasurementsPercentual1.MarginalReflexDistance2)
        self._MeasurementStatePercentComparison.PalpebralFissureHeight = abs(self._MeasurementsPercentual2.PalpebralFissureHeight - self._MeasurementsPercentual1.PalpebralFissureHeight)
        self._MeasurementStatePercentComparison.EyeArea = abs(self._MeasurementsPercentual2.EyeArea - self._MeasurementsPercentual1.EyeArea)
        self._MeasurementStatePercentComparison.NLF_angle = abs(self._MeasurementsPercentual2.NLF_angle - self._MeasurementsPercentual1.NLF_angle)
        self._MeasurementStatePercentComparison.UpperLipSlope = abs(self._MeasurementsPercentual2.UpperLipSlope - self._MeasurementsPercentual1.UpperLipSlope)
        self._MeasurementStatePercentComparison.CommisureHeight = abs(self._MeasurementsPercentual2.CommisureHeight - self._MeasurementsPercentual1.CommisureHeight)
        self._MeasurementStatePercentComparison.InterlabialDistance = abs(self._MeasurementsPercentual2.InterlabialDistance - self._MeasurementsPercentual1.InterlabialDistance)
        self._MeasurementStatePercentComparison.InterlabialArea_of_the_Hemiface = abs(self._MeasurementsPercentual2.InterlabialArea_of_the_Hemiface - self._MeasurementsPercentual1.InterlabialArea_of_the_Hemiface)
        self._MeasurementStatePercentComparison.CommissurePosition = abs(self._MeasurementsPercentual2.CommissurePosition - self._MeasurementsPercentual1.CommissurePosition)
        self._MeasurementStatePercentComparison.LowerLipHeight = abs(self._MeasurementsPercentual2.LowerLipHeight - self._MeasurementsPercentual1.LowerLipHeight)


