import numpy as np
from PyQt5 import QtWidgets, QtGui, uic
from Metrics import get_measurements_from_data, FaceMeasurementsSide, FaceMeasurementsDeviation
from ImageDisplay import ImageDisplay

class MetricsDoubleWindow(QtWidgets.QMainWindow):
    
    def __init__(self, shape1, left_pupil1, right_pupil1, points1, shape2, left_pupil2, right_pupil2, points2, CalibrationType, CalibrationValue, reference_state, reference_side, file_name1, file_name2):
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
        self._reference_state = reference_state
        self._fileName1 = file_name1
        self._fileName2 = file_name2
        
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
        self.ui = uic.loadUi('uis\Metrics_Double_Unapproved.ui', self)
        
        #Measurements
        self._MeasurementsLeft1, self._MeasurementsRight1, self._MeasurementsDeviation1, self._MeasurementsPercentual1 = get_measurements_from_data(self._shape1, self._lefteye1, self._righteye1, self._points1, self._CalibrationType, self._CalibrationValue, self._reference_side)
        self._MeasurementsLeft2, self._MeasurementsRight2, self._MeasurementsDeviation2, self._MeasurementsPercentual2 = get_measurements_from_data(self._shape2, self._lefteye2, self._righteye2, self._points2, self._CalibrationType, self._CalibrationValue, self._reference_side)
        
        #One Side Comparison
        self.getOneSideComparison

        #Two Side Comparison
        self.getTwoSideComparison

        #Filling in table
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


        if self._refefernce_state == 1:
            #Left Side Percent Comparison
            self._MeasurementLeftPercentComparison.BrowHeight = abs(self._MeasurementsLeft2.BrowHeight - self._MeasurementsLeft1.BrowHeight)*100/self._MeasurementsLeft1.BrowHeight
            self._MeasurementLeftPercentComparison.MarginalReflexDistance1 = abs(self._MeasurementsLeft2.MarginalReflexDistance1 - self._MeasurementsLeft1.MarginalReflexDistance1)*100/self._MeasurementsLeft1.MarginalReflexDistance1
            self._MeasurementLeftPercentComparison.MarginalReflexDistance2 = abs(self._MeasurementsLeft2.MarginalReflexDistance2 - self._MeasurementsLeft1.MarginalReflexDistance2)*100/self._MeasurementsLeft1.MarginalReflexDistance2
            self._MeasurementLeftPercentComparison.PalpebralFissureHeight = abs(self._MeasurementsLeft2.PalpebralFissureHeight - self._MeasurementsLeft1.PalpebralFissureHeight)*100/self._MeasurementsLeft1.PalpebralFissureHeight
            self._MeasurementLeftPercentComparison.EyeArea = abs(self._MeasurementsLeft2.EyeArea - self._MeasurementsLeft1.EyeArea)*100/self._MeasurementsLeft1.EyeArea
            self._MeasurementLeftPercentComparison.NLF_angle = abs(self._MeasurementsLeft2.NLF_angle - self._MeasurementsLeft1.NLF_angle)*100/self._MeasurementsLeft1.NLF_angle
            self._MeasurementLeftPercentComparison.UpperLipSlope = abs(self._MeasurementsLeft2.UpperLipSlope - self._MeasurementsLeft1.UpperLipSlope)*100/self._MeasurementsLeft1.UpperLipSlope
            self._MeasurementLeftPercentComparison.CommisureHeight = abs(self._MeasurementsLeft2.CommisureHeight - self._MeasurementsLeft1.CommisureHeight)*100/self._MeasurementsLeft1.CommisureHeight
            self._MeasurementLeftPercentComparison.InterlabialDistance = abs(self._MeasurementsLeft2.InterlabialDistance - self._MeasurementsLeft1.InterlabialDistance)*100/self._MeasurementsLeft1.InterlabialDistance
            self._MeasurementLeftPercentComparison.InterlabialArea_of_the_Hemiface = abs(self._MeasurementsLeft2.InterlabialArea_of_the_Hemiface - self._MeasurementsLeft1.InterlabialArea_of_the_Hemiface)*100/self._MeasurementsLeft1.InterlabialArea_of_the_Hemiface
            self._MeasurementLeftPercentComparison.CommissurePosition = abs(self._MeasurementsLeft2.CommissurePosition - self._MeasurementsLeft1.CommissurePosition)*100/self._MeasurementsLeft1.CommissurePosition
            self._MeasurementLeftPercentComparison.LowerLipHeight = abs(self._MeasurementsLeft2.LowerLipHeight - self._MeasurementsLeft1.LowerLipHeight)*100/self._MeasurementsLeft1.LowerLipHeight

            #Right Side Percent Comparison
            self._MeasurementRightPercentComparison.BrowHeight = abs(self._MeasurementsRight2.BrowHeight - self._MeasurementsRight1.BrowHeight)*100/self._MeasurementsRight1.BrowHeight
            self._MeasurementRightPercentComparison.MarginalReflexDistance1 = abs(self._MeasurementsRight2.MarginalReflexDistance1 - self._MeasurementsRight1.MarginalReflexDistance1)*100/self._MeasurementsRight1.MarginalReflexDistance1
            self._MeasurementRightPercentComparison.MarginalReflexDistance2 = abs(self._MeasurementsRight2.MarginalReflexDistance2 - self._MeasurementsRight1.MarginalReflexDistance2)*100/self._MeasurementsRight1.MarginalReflexDistance2
            self._MeasurementRightPercentComparison.PalpebralFissureHeight = abs(self._MeasurementsRight2.PalpebralFissureHeight - self._MeasurementsRight1.PalpebralFissureHeight)*100/self._MeasurementsRight1.EyeArea
            self._MeasurementRightPercentComparison.EyeArea = abs(self._MeasurementsRight2.EyeArea - self._MeasurementsRight1.EyeArea)*100/self._MeasurementsRight1.EyeArea
            self._MeasurementRightPercentComparison.NLF_angle = abs(self._MeasurementsRight2.NLF_angle - self._MeasurementsRight1.NLF_angle)*100/self._MeasurementsRight1.NLF_angle
            self._MeasurementRightPercentComparison.UpperLipSlope = abs(self._MeasurementsRight2.UpperLipSlope - self._MeasurementsRight1.UpperLipSlope)*100/self._MeasurementsRight1.UpperLipSlope
            self._MeasurementRightPercentComparison.CommisureHeight = abs(self._MeasurementsRight2.CommisureHeight - self._MeasurementsRight1.CommisureHeight)*100/self._MeasurementsRight1.CommisureHeight
            self._MeasurementRightPercentComparison.InterlabialDistance = abs(self._MeasurementsRight2.InterlabialDistance - self._MeasurementsRight1.InterlabialDistance)*100/self._MeasurementsRight1.InterlabialDistance
            self._MeasurementRightPercentComparison.InterlabialArea_of_the_Hemiface = abs(self._MeasurementsRight2.InterlabialArea_of_the_Hemiface - self._MeasurementsRight1.InterlabialArea_of_the_Hemiface)*100/self._MeasurementsRight1.InterlabialArea_of_the_Hemiface
            self._MeasurementRightPercentComparison.CommissurePosition = abs(self._MeasurementsRight2.CommissurePosition - self._MeasurementsRight1.CommissurePosition)*100/self._MeasurementsRight1.CommissurePosition
            self._MeasurementRightPercentComparison.LowerLipHeight = abs(self._MeasurementsRight2.LowerLipHeight - self._MeasurementsRight1.LowerLipHeight)*100/self._MeasurementsRight1.LowerLipHeight
        else:
            #Left Side Percent Comparison
            self._MeasurementLeftPercentComparison.BrowHeight = abs(self._MeasurementsLeft2.BrowHeight - self._MeasurementsLeft1.BrowHeight)*100/self._MeasurementsLeft2.BrowHeight
            self._MeasurementLeftPercentComparison.MarginalReflexDistance1 = abs(self._MeasurementsLeft2.MarginalReflexDistance1 - self._MeasurementsLeft1.MarginalReflexDistance1)*100/self._MeasurementsLeft2.MarginalReflexDistance1
            self._MeasurementLeftPercentComparison.MarginalReflexDistance2 = abs(self._MeasurementsLeft2.MarginalReflexDistance2 - self._MeasurementsLeft1.MarginalReflexDistance2)*100/self._MeasurementsLeft2.MarginalReflexDistance2
            self._MeasurementLeftPercentComparison.PalpebralFissureHeight = abs(self._MeasurementsLeft2.PalpebralFissureHeight - self._MeasurementsLeft1.PalpebralFissureHeight)*100/self._MeasurementsLeft2.PalpebralFissureHeight
            self._MeasurementLeftPercentComparison.EyeArea = abs(self._MeasurementsLeft2.EyeArea - self._MeasurementsLeft1.EyeArea)*100/self._MeasurementsLeft2.EyeArea
            self._MeasurementLeftPercentComparison.NLF_angle = abs(self._MeasurementsLeft2.NLF_angle - self._MeasurementsLeft1.NLF_angle)*100/self._MeasurementsLeft2.NLF_angle
            self._MeasurementLeftPercentComparison.UpperLipSlope = abs(self._MeasurementsLeft2.UpperLipSlope - self._MeasurementsLeft1.UpperLipSlope)*100/self._MeasurementsLeft2.UpperLipSlope
            self._MeasurementLeftPercentComparison.CommisureHeight = abs(self._MeasurementsLeft2.CommisureHeight - self._MeasurementsLeft1.CommisureHeight)*100/self._MeasurementsLeft2.CommisureHeight
            self._MeasurementLeftPercentComparison.InterlabialDistance = abs(self._MeasurementsLeft2.InterlabialDistance - self._MeasurementsLeft1.InterlabialDistance)*100/self._MeasurementsLeft2.InterlabialDistance
            self._MeasurementLeftPercentComparison.InterlabialArea_of_the_Hemiface = abs(self._MeasurementsLeft2.InterlabialArea_of_the_Hemiface - self._MeasurementsLeft1.InterlabialArea_of_the_Hemiface)*100/self._MeasurementsLeft2.InterlabialArea_of_the_Hemiface
            self._MeasurementLeftPercentComparison.CommissurePosition = abs(self._MeasurementsLeft2.CommissurePosition - self._MeasurementsLeft1.CommissurePosition)*100/self._MeasurementsLeft2.CommissurePosition
            self._MeasurementLeftPercentComparison.LowerLipHeight = abs(self._MeasurementsLeft2.LowerLipHeight - self._MeasurementsLeft1.LowerLipHeight)*100/self._MeasurementsLeft2.LowerLipHeight

            #Right Side Percent Comparison
            self._MeasurementRightPercentComparison.BrowHeight = abs(self._MeasurementsRight2.BrowHeight - self._MeasurementsRight1.BrowHeight)*100/self._MeasurementsRight2.BrowHeight
            self._MeasurementRightPercentComparison.MarginalReflexDistance1 = abs(self._MeasurementsRight2.MarginalReflexDistance1 - self._MeasurementsRight1.MarginalReflexDistance1)*100/self._MeasurementsRight2.MarginalReflexDistance1
            self._MeasurementRightPercentComparison.MarginalReflexDistance2 = abs(self._MeasurementsRight2.MarginalReflexDistance2 - self._MeasurementsRight1.MarginalReflexDistance2)*100/self._MeasurementsRight2.MarginalReflexDistance2
            self._MeasurementRightPercentComparison.PalpebralFissureHeight = abs(self._MeasurementsRight2.PalpebralFissureHeight - self._MeasurementsRight1.PalpebralFissureHeight)*100/self._MeasurementsRight2.EyeArea
            self._MeasurementRightPercentComparison.EyeArea = abs(self._MeasurementsRight2.EyeArea - self._MeasurementsRight1.EyeArea)*100/self._MeasurementsRight2.EyeArea
            self._MeasurementRightPercentComparison.NLF_angle = abs(self._MeasurementsRight2.NLF_angle - self._MeasurementsRight1.NLF_angle)*100/self._MeasurementsRight2.NLF_angle
            self._MeasurementRightPercentComparison.UpperLipSlope = abs(self._MeasurementsRight2.UpperLipSlope - self._MeasurementsRight1.UpperLipSlope)*100/self._MeasurementsRight2.UpperLipSlope
            self._MeasurementRightPercentComparison.CommisureHeight = abs(self._MeasurementsRight2.CommisureHeight - self._MeasurementsRight1.CommisureHeight)*100/self._MeasurementsRight2.CommisureHeight
            self._MeasurementRightPercentComparison.InterlabialDistance = abs(self._MeasurementsRight2.InterlabialDistance - self._MeasurementsRight1.InterlabialDistance)*100/self._MeasurementsRight2.InterlabialDistance
            self._MeasurementRightPercentComparison.InterlabialArea_of_the_Hemiface = abs(self._MeasurementsRight2.InterlabialArea_of_the_Hemiface - self._MeasurementsRight1.InterlabialArea_of_the_Hemiface)*100/self._MeasurementsRight2.InterlabialArea_of_the_Hemiface
            self._MeasurementRightPercentComparison.CommissurePosition = abs(self._MeasurementsRight2.CommissurePosition - self._MeasurementsRight1.CommissurePosition)*100/self._MeasurementsRight2.CommissurePosition
            self._MeasurementRightPercentComparison.LowerLipHeight = abs(self._MeasurementsRight2.LowerLipHeight - self._MeasurementsRight1.LowerLipHeight)*100/self._MeasurementsRight2.LowerLipHeight
            

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





        
            
        
        
        
        