from Compute_eFace import Compute_eFace
from Patient import Patient
from SinglePhotoWindow import SinglePhotoWindow
from PyQt5 import QtWidgets, QtGui, uic, QtCore
from pathlib import Path
from PIL import Image, ImageOps
from ThumbNailDisplay import ThumbNailDisplay
from ImageDisplay import ImageDisplay
from MplWidget import MplWidget
from Save_eFace_Window import Save_eFace_Window


class SevenPhotoWindow(QtWidgets.QMainWindow):
    finished = QtCore.pyqtSignal()
    canceled = QtCore.pyqtSignal()
    file = QtCore.pyqtSignal(object)
    reference_Side = QtCore.pyqtSignal(object)
    taskName = QtCore.pyqtSignal(object)

    def __init__(self):
        super() .__init__()
        self._file_R = None
        self._file_BR = None
        self._file_GEC = None
        self._file_TEC = None
        self._file_BS = None
        self._file_eeeek = None
        self._file_ooooo = None
        self._finished_R = False
        self._finished_BR = False
        self._finished_GEC = False
        self._finished_TEC = False
        self._finished_BS = False
        self._finished_eeeek = False
        self._finished_ooooo = False
        
        self._Patient = Patient()
        self._patientID = None
        self._Patient._reference_side = 'Right'
        self._Patient._CalibrationType = 'Iris'
        self._Patient._CalibrationValue = 11.77
        self._Patient._ModelName = 'FAN_MEEE'


        self.initUI()
        
        
    def initUI(self):
        self.ui = uic.loadUi('uis\seven.ui', self)
        
        #Resting Window
        self.restingWindow = SinglePhotoWindow()
        self.restingDisplay.selected.connect(self.restingWindow.show)
        self.restingDisplay.selected.connect(self.hideWindow)
        self.restingWindow.finished.connect(self.restingWindow.hide)
        self.restingWindow.finished.connect(self.showWindow)
        self.restingWindow.busy.connect(self.setBusy)
        self.restingWindow.got_landmarks.connect(self.got_R)
        #Brow Raise Window
        self.browRaiseWindow = SinglePhotoWindow()
        self.browRaiseDisplay.selected.connect(self.browRaiseWindow.show)
        self.browRaiseDisplay.selected.connect(self.hideWindow)
        self.browRaiseWindow.finished.connect(self.browRaiseWindow.hide)
        self.browRaiseWindow.finished.connect(self.showWindow)
        self.browRaiseWindow.busy.connect(self.setBusy)
        self.browRaiseWindow.got_landmarks.connect(self.got_BR)
        #Gentle Eye Closure Window
        self.GentleEyeClosureWindow = SinglePhotoWindow()
        self.gentleEyeClosureDisplay.selected.connect(self.GentleEyeClosureWindow.show)
        self.gentleEyeClosureDisplay.selected.connect(self.hideWindow)
        self.GentleEyeClosureWindow.finished.connect(self.GentleEyeClosureWindow.hide)
        self.GentleEyeClosureWindow.finished.connect(self.showWindow)
        self.GentleEyeClosureWindow.busy.connect(self.setBusy)
        self.GentleEyeClosureWindow.got_landmarks.connect(self.got_GEC)
        #TightEyeClosureWindow Window
        self.TightEyeClosureWindow = SinglePhotoWindow()
        self.tightEyeClosureDisplay.selected.connect(self.TightEyeClosureWindow.show)
        self.tightEyeClosureDisplay.selected.connect(self.hideWindow)
        self.TightEyeClosureWindow.finished.connect(self.TightEyeClosureWindow.hide)
        self.TightEyeClosureWindow.finished.connect(self.showWindow)
        self.TightEyeClosureWindow.busy.connect(self.setBusy)
        self.TightEyeClosureWindow.got_landmarks.connect(self.got_TEC)
        #Big Smile Window
        self.BigSmileWindow = SinglePhotoWindow()
        self.bigSmileDisplay.selected.connect(self.BigSmileWindow.show)
        self.bigSmileDisplay.selected.connect(self.hideWindow)
        self.BigSmileWindow.finished.connect(self.BigSmileWindow.hide)
        self.BigSmileWindow.finished.connect(self.showWindow)
        self.BigSmileWindow.busy.connect(self.setBusy)
        self.BigSmileWindow.got_landmarks.connect(self.got_BS)
        #"eeeek" Window
        self.eeeekWindow = SinglePhotoWindow()
        self.eeeekDisplay.selected.connect(self.eeeekWindow.show)
        self.eeeekDisplay.selected.connect(self.hideWindow)
        self.eeeekWindow.finished.connect(self.eeeekWindow.hide)
        self.eeeekWindow.finished.connect(self.showWindow)
        self.eeeekWindow.busy.connect(self.setBusy)
        self.eeeekWindow.got_landmarks.connect(self.got_ek)
        #"ooooo" Window
        self.oooooWindow = SinglePhotoWindow()
        self.oooooDisplay.selected.connect(self.oooooWindow.show)
        self.oooooDisplay.selected.connect(self.hideWindow)
        self.oooooWindow.finished.connect(self.oooooWindow.hide)
        self.oooooWindow.finished.connect(self.showWindow)
        self.oooooWindow.busy.connect(self.setBusy)
        self.oooooWindow.got_landmarks.connect(self.got_oo)

        """Button Connection"""
        self.previousButton.clicked.connect(self.previous)
        self.matchIrisButton.clicked.connect(self.matchIris)
        self.saveButton.clicked.connect(self.save_eFace_Excel)


    ########################################################################################################################
    ########################################################################################################################
    """Set-up Functions"""
    ########################################################################################################################
    ########################################################################################################################
    
    
    def setPatientID(self, patientID):
        self._patientID = patientID
        self.setWindowTitle(f"Emotrics+ | {self._patientID}")


    def setPhoto_R(self, name):
        self._file_R = name
        pixmap = QtGui.QPixmap(name)
        self.restingDisplay.setPhoto(pixmap)
        self.restingWindow.setPhoto(name)
        self.restingWindow.setTaskName('Resting')

    def got_R(self):
        self._finished_R = True
        self.checkBusy()

    def setPhoto_BR(self, name):
        self._file_BR = name
        pixmap = QtGui.QPixmap(name)
        self.browRaiseDisplay.setPhoto(pixmap)
        self.browRaiseWindow.setPhoto(name)
        self.browRaiseWindow.setTaskName('Brow Raise')
        
    def got_BR(self):
        self._finished_BR = True
        self.checkBusy()
    
    def setPhoto_GEC(self, name):
        self._file_GEC = name
        pixmap = QtGui.QPixmap(name)
        self.gentleEyeClosureDisplay.setPhoto(pixmap)
        self.GentleEyeClosureWindow.setPhoto(name)
        self.GentleEyeClosureWindow.setTaskName('Gentle Eye Closure')
        
    def got_GEC(self):
        self._finished_GEC = True
        self.checkBusy()
    
    def setPhoto_TEC(self, name):
        self._file_TEC = name
        pixmap = QtGui.QPixmap(name)
        self.tightEyeClosureDisplay.setPhoto(pixmap)
        self.TightEyeClosureWindow.setPhoto(name)
        self.TightEyeClosureWindow.setTaskName('Tight Eye Closure')
        
    def got_TEC(self):
        self._finished_TEC = True
        self.checkBusy()

    def setPhoto_BS(self, name):
        self._file_BS = name
        pixmap = QtGui.QPixmap(name)
        self.bigSmileDisplay.setPhoto(pixmap)
        self.BigSmileWindow.setPhoto(name)
        self.BigSmileWindow.setTaskName('Big Smile')
    
    def got_BS(self):
        self._finished_BS = True
        self.checkBusy()

    def setPhoto_eeeek(self, name):
        self._file_eeeek = name
        pixmap = QtGui.QPixmap(name)
        self.eeeekDisplay.setPhoto(pixmap)
        self.eeeekWindow.setPhoto(name)
        self.eeeekWindow.setTaskName('"eeeek"')
        
    def got_ek(self):
        self._finished_eeeek = True
        self.checkBusy()

    def setPhoto_ooooo(self, name):
        self._file_ooooo = name
        pixmap = QtGui.QPixmap(name)
        self.oooooDisplay.setPhoto(pixmap)
        self.oooooWindow.setPhoto(name)
        self.oooooWindow.setTaskName('"ooooo"')
        
    def got_oo(self):
        self._finished_ooooo = True
        self.checkBusy()

    def setReferenceSide(self, side):
        if side == 'Left':
            self._Patient._reference_side = 'Left'
            self.restingWindow.setReferenceSide(self._Patient._reference_side)
            self.browRaiseWindow.setReferenceSide(self._Patient._reference_side)
            self.GentleEyeClosureWindow.setReferenceSide(self._Patient._reference_side)
            self.TightEyeClosureWindow.setReferenceSide(self._Patient._reference_side)
            self.BigSmileWindow.setReferenceSide(self._Patient._reference_side)
            self.eeeekWindow.setReferenceSide(self._Patient._reference_side)
            self.oooooWindow.setReferenceSide(self._Patient._reference_side)
        elif side == 'Right':
            self._Patient._reference_side = 'Right'
            self.restingWindow.setReferenceSide(self._Patient._reference_side)
            self.browRaiseWindow.setReferenceSide(self._Patient._reference_side)
            self.GentleEyeClosureWindow.setReferenceSide(self._Patient._reference_side)
            self.TightEyeClosureWindow.setReferenceSide(self._Patient._reference_side)
            self.BigSmileWindow.setReferenceSide(self._Patient._reference_side)
            self.eeeekWindow.setReferenceSide(self._Patient._reference_side)
            self.oooooWindow.setReferenceSide(self._Patient._reference_side)
        else:
            print('Invalid Reference Side')
    

    def setBusy(self):
        """This function is to show that the program is current working on something
        (most likely Landmark Thread). It shows this by set the cursor to the busy cursor"""
        # print('Busy\nBusy Cursor Set')
        self.setCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

    
    def checkBusy(self):
        """Checks if all the landmarks have been found so that the plot can be updated"""
        print('Checking if all done')
        if (self._finished_R == True and self._finished_BR == True and self._finished_GEC == True
        and self._finished_TEC == True and self._finished_BS == True and self._finished_eeeek == True
        and self._finished_ooooo == True):
            print('All threads finished')
            self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
            self.update_Plots()
        else:
            print(f'self._finished_R = {self._finished_R}')
            print(f'self._finished_BR = {self._finished_BR}')
            print(f'self._finished_GEC = {self._finished_GEC}')
            print(f'self._finished_TEC = {self._finished_TEC}')
            print(f'self._finished_BS = {self._finished_BS}')
            print(f'self._finished_eeeek = {self._finished_eeeek}')
            print(f'self._finished_ooooo = {self._finished_ooooo}')

    ########################################################################################################################
    ########################################################################################################################
    """Patient Functions"""
    ########################################################################################################################
    ########################################################################################################################
    

    def get_Patient(self):
        """This function collects all the info of the patient from the various SinglePhotoWindows"""
        #Resting
        self._Patient._Resting._shape = self.restingWindow.displayImage._shape
        self._Patient._Resting._lefteye = self.restingWindow.displayImage._lefteye
        self._Patient._Resting._righteye = self.restingWindow.displayImage._righteye
        if self.restingWindow.displayImage._points == None:
            self.restingWindow.displayImage.get_midline()
        self._Patient._Resting._points = self.restingWindow.displayImage._points
        self._Patient._Resting._boundingbox = self.restingWindow.displayImage._boundingbox
        
        #Brow Raise
        self._Patient._Brow_Raise._shape = self.browRaiseWindow.displayImage._shape
        self._Patient._Brow_Raise._lefteye = self.browRaiseWindow.displayImage._lefteye
        self._Patient._Brow_Raise._righteye = self.browRaiseWindow.displayImage._righteye
        if self.browRaiseWindow.displayImage._points == None:
            self.browRaiseWindow.displayImage.get_midline()
        self._Patient._Brow_Raise._points = self.browRaiseWindow.displayImage._points
        self._Patient._Brow_Raise._boundingbox = self.browRaiseWindow.displayImage._boundingbox
        
        #Gentle Eye Closure
        self._Patient._Gentle_Eye_Closure._shape = self.GentleEyeClosureWindow.displayImage._shape
        self._Patient._Gentle_Eye_Closure._lefteye = self.GentleEyeClosureWindow.displayImage._lefteye
        self._Patient._Gentle_Eye_Closure._righteye = self.GentleEyeClosureWindow.displayImage._righteye
        if self.GentleEyeClosureWindow.displayImage._points == None:
            self.GentleEyeClosureWindow.displayImage.get_midline()
        self._Patient._Gentle_Eye_Closure._points = self.GentleEyeClosureWindow.displayImage._points
        self._Patient._Gentle_Eye_Closure._boundingbox = self.GentleEyeClosureWindow.displayImage._boundingbox
        
        #Tight Eye Closure
        self._Patient._Tight_Eye_Closure._shape = self.TightEyeClosureWindow.displayImage._shape
        self._Patient._Tight_Eye_Closure._lefteye = self.TightEyeClosureWindow.displayImage._lefteye
        self._Patient._Tight_Eye_Closure._righteye = self.TightEyeClosureWindow.displayImage._righteye
        if self.TightEyeClosureWindow.displayImage._points == None:
            self.TightEyeClosureWindow.displayImage.get_midline()
        self._Patient._Tight_Eye_Closure._points = self.TightEyeClosureWindow.displayImage._points
        self._Patient._Tight_Eye_Closure._boundingbox = self.TightEyeClosureWindow.displayImage._boundingbox
        
        #Big Smile
        self._Patient._Big_Smile._shape = self.BigSmileWindow.displayImage._shape
        self._Patient._Big_Smile._lefteye = self.BigSmileWindow.displayImage._lefteye
        self._Patient._Big_Smile._righteye = self.BigSmileWindow.displayImage._righteye
        if self.BigSmileWindow.displayImage._points == None:
            self.BigSmileWindow.displayImage.get_midline()
        self._Patient._Big_Smile._points = self.BigSmileWindow.displayImage._points
        self._Patient._Big_Smile._boundingbox = self.BigSmileWindow.displayImage._boundingbox
        
        #"eeeek"
        self._Patient._eeeek._shape = self.eeeekWindow.displayImage._shape
        self._Patient._eeeek._lefteye = self.eeeekWindow.displayImage._lefteye
        self._Patient._eeeek._righteye = self.eeeekWindow.displayImage._righteye
        if self.eeeekWindow.displayImage._points == None:
            self.eeeekWindow.displayImage.get_midline()
        self._Patient._eeeek._points = self.eeeekWindow.displayImage._points
        self._Patient._eeeek._boundingbox = self.eeeekWindow.displayImage._boundingbox
        
        #"ooooo"
        self._Patient._ooooo._shape = self.oooooWindow.displayImage._shape
        self._Patient._ooooo._lefteye = self.oooooWindow.displayImage._lefteye
        self._Patient._ooooo._righteye = self.oooooWindow.displayImage._righteye
        if self.oooooWindow.displayImage._points == None:
            self.oooooWindow.displayImage.get_midline()
        self._Patient._ooooo._points = self.oooooWindow.displayImage._points
        self._Patient._ooooo._boundingbox = self.oooooWindow.displayImage._boundingbox
        


    ########################################################################################################################
    ########################################################################################################################
    """Plotting Functions"""
    ########################################################################################################################
    ########################################################################################################################


    def update_Plots(self):
        """This function will plot the data and make sure the plot is always based on the current landmarks"""
        try:
            self.get_Patient()
            (self._score_brow_rest, self._score_PalpebralFissure_rest, self._score_OralCommissure_rest, self._NLF_at_rest,
            self._BrowRaise, self._GentleEyeClosure, self._FullEyeClosure, self._OralCommissureWithSmile, self._LowerLipEEE,
            self._OcularSynkinesis, self._StaticScore, self._DynamicScore, self._SynkinesisScore, self._Total_Score) = Compute_eFace(self._Patient)

            #Total Scores Plot
            x = ['Static\nScore', 'Dynamic\nScore', 'Synkinesis\nScore', 'Total\nScore']
            y = [self._StaticScore, self._DynamicScore, self._SynkinesisScore, self._Total_Score]

            self.totalPlot.canvas.ax.clear()
            self.totalPlot.canvas.ax.bar(x, y, color='blue')
            self.totalPlot.canvas.ax.set_title('Total Score')
            self.totalPlot.canvas.ax.set_ylim(0,100)
            self.totalPlot.canvas.draw()

            #Static Scores Plot
            x = ['Brow Height', 'Palpebral Fissure', 'Oral Commissure', 'Nasolabial\nFold Angle']
            y = [self._score_brow_rest, self._score_PalpebralFissure_rest, self._score_OralCommissure_rest, self._NLF_at_rest]

            self.staticPlot.canvas.ax.clear()
            self.staticPlot.canvas.ax.bar(x, y, color='blue')
            self.staticPlot.canvas.ax.set_title('Static Parameters')
            self.staticPlot.canvas.ax.set_ylim(0,200)
            self.staticPlot.canvas.draw()

            #Dynamic Scores Plot
            x = ['Brow\nRaise', 'Gentle Eye\nClosure', 'Full Eye\nClosure', 'Oral Commissure\nMovement with Smile', 'Lower Lip\nMovement']
            y = [self._BrowRaise, self._GentleEyeClosure, self._FullEyeClosure, self._OralCommissureWithSmile, self._LowerLipEEE]

            self.dynamicPlot.canvas.ax.clear()
            self.dynamicPlot.canvas.ax.bar(x, y, color='blue')
            self.dynamicPlot.canvas.ax.set_title('Dynamic Parameters')
            self.dynamicPlot.canvas.ax.set_ylim(0,100)
            self.dynamicPlot.canvas.draw()

            #Synkinesis Scores Plot
            x = ['Ocular\nSynkinesis']
            y = [self._OcularSynkinesis]

            self.synkinesisPlot.canvas.ax.clear()
            self.synkinesisPlot.canvas.ax.bar(x, y, color='blue')
            self.synkinesisPlot.canvas.ax.set_title('Synkinesis Score')
            self.synkinesisPlot.canvas.ax.set_ylim(0,100)
            self.synkinesisPlot.canvas.draw()


            self._finished_R = True
            self._finished_BR = True
            self._finished_GEC = True
            self._finished_TEC = True
            self._finished_BS = True
            self._finished_eeeek = True
            self._finished_ooooo = True
        except:
            print('Error in updating plot')
            if (self._finished_R == True and self._finished_BR == True and self._finished_GEC == True
            and self._finished_TEC == True and self._finished_BS == True and self._finished_eeeek == True
            and self._finished_ooooo == True):
                print('Since all threads are finished, retrying self.updatePlots()')



    
    ########################################################################################################################
    ########################################################################################################################
    """Button Functions"""
    ########################################################################################################################
    ########################################################################################################################
    

    def matchIris(self):
        """This function matches all the eyes to the eye in the resting photo"""
        print('Matching Iris')
        self.browRaiseWindow.displayImage._lefteye = self.restingWindow.displayImage._lefteye
        self.browRaiseWindow.displayImage._righteye = self.restingWindow.displayImage._righteye
        self.browRaiseWindow.displayImage.update_shape()

        self.GentleEyeClosureWindow.displayImage._lefteye = self.restingWindow.displayImage._lefteye
        self.GentleEyeClosureWindow.displayImage._righteye = self.restingWindow.displayImage._righteye
        self.browRaiseWindow.displayImage.update_shape()

        self.TightEyeClosureWindow.displayImage._lefteye = self.restingWindow.displayImage._lefteye
        self.TightEyeClosureWindow.displayImage._righteye = self.restingWindow.displayImage._righteye
        self.browRaiseWindow.displayImage.update_shape()

        self.BigSmileWindow.displayImage._lefteye = self.restingWindow.displayImage._lefteye
        self.BigSmileWindow.displayImage._righteye = self.restingWindow.displayImage._righteye
        self.browRaiseWindow.displayImage.update_shape()

        self.eeeekWindow.displayImage._lefteye = self.restingWindow.displayImage._lefteye
        self.eeeekWindow.displayImage._righteye = self.restingWindow.displayImage._righteye
        self.browRaiseWindow.displayImage.update_shape()

        self.oooooWindow.displayImage._lefteye = self.restingWindow.displayImage._lefteye
        self.oooooWindow.displayImage._righteye = self.restingWindow.displayImage._righteye
        self.browRaiseWindow.displayImage.update_shape()
        self.update_Plots()

    ########################################################################################################################
    ########################################################################################################################
    """Saving Functions"""
    ########################################################################################################################
    ########################################################################################################################
    

    def save_eFace_Excel(self):
        """This function saves the eFace Scores as an xls file."""
        try:
                
            temp = Save_eFace_Window(self, self._file_R, self._patientID, self._score_brow_rest, self._score_PalpebralFissure_rest,
            self._score_OralCommissure_rest, self._NLF_at_rest, self._BrowRaise, self._GentleEyeClosure, 
            self._FullEyeClosure, self._OralCommissureWithSmile, self._LowerLipEEE, self._OcularSynkinesis, 
            self._StaticScore, self._DynamicScore, self._SynkinesisScore, self._Total_Score)
            temp.exec_()
        
        except Exception as e:
            QtWidgets.QMessageBox.information(self, 'Error', 
                    f'Error in creating metrics window.\n Error message: {e}', # ',#
                    QtWidgets.QMessageBox.Ok)
    
    ########################################################################################################################
    ########################################################################################################################
    """Close Functions"""
    ########################################################################################################################
    ########################################################################################################################
    

    def showWindow(self):
        self.update_Plots()
        self.setVisible(True)

    def hideWindow(self):
        self.setVisible(False)


    def previous(self):
        self.finished.emit()
        self.close()

    