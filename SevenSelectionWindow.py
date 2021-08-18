from PyQt5 import QtWidgets, QtGui, uic, QtCore
from pathlib import Path

class SevenSelectionWindow(QtWidgets.QMainWindow):
    finished = QtCore.pyqtSignal()
    canceled = QtCore.pyqtSignal()
    file_R = QtCore.pyqtSignal(object)
    file_BR = QtCore.pyqtSignal(object)
    file_GEC = QtCore.pyqtSignal(object)
    file_TEC = QtCore.pyqtSignal(object)
    file_BS = QtCore.pyqtSignal(object)
    file_eeeek = QtCore.pyqtSignal(object)
    file_ooooo = QtCore.pyqtSignal(object)
    reference_Side = QtCore.pyqtSignal(object)

    def __init__(self):
        super() .__init__()
        self._file_R = None
        self._file_BR = None
        self._file_GEC = None
        self._file_TEC = None
        self._file_BS = None
        self._file_eeeek = None
        self._file_ooooo = None
        self._valid_file_R = False
        self._valid_file_BR = False
        self._valid_file_GEC = False
        self._valid_file_TEC = False
        self._valid_file_BS = False
        self._valid_file_eeeek = False
        self._valid_file_ooooo = False
        self._reference_side = 'Right'



        self.initUI()
        
        
    def initUI(self):
        self.ui = uic.loadUi('uis\select_seven.ui', self)
        
        """Button Connection"""
        self.leftSideButton.toggled.connect(self.leftSideSelected)
        self.rightSideButton.toggled.connect(self.rightSideSelected)

        self.loadPhotoRButton.clicked.connect(self.load_R) 
        self.loadPhotoBRButton.clicked.connect(self.load_BR) 
        self.loadPhotoGECButton.clicked.connect(self.load_GEC) 
        self.loadPhotoTECButton.clicked.connect(self.load_TEC) 
        self.loadPhotoBSButton.clicked.connect(self.load_BS) 
        self.loadPhotoeeeekButton.clicked.connect(self.load_eeeek) 
        self.loadPhotooooooButton.clicked.connect(self.load_ooooo) 
           
        self.previousButton.clicked.connect(self.previous)
        self.nextButton.clicked.connect(self.next)
        
        #Adding Icons
        pixmap = QtGui.QPixmap('./icons/upload.jpg')
        self.restingDisplay.setPhoto(pixmap)
        self.restingDisplay.fitInView()
        pixmap = QtGui.QPixmap('./icons/upload.jpg')
        self.browRaiseDisplay.setPhoto(pixmap)
        self.browRaiseDisplay.fitInView()
        pixmap = QtGui.QPixmap('./icons/upload.jpg')
        self.gentleEyeClosureDisplay.setPhoto(pixmap)
        self.gentleEyeClosureDisplay.fitInView()
        pixmap = QtGui.QPixmap('./icons/upload.jpg')
        self.tightEyeClosureDisplay.setPhoto(pixmap)
        self.tightEyeClosureDisplay.fitInView()
        pixmap = QtGui.QPixmap('./icons/upload.jpg')
        self.bigSmileDisplay.setPhoto(pixmap)
        self.bigSmileDisplay.fitInView()
        pixmap = QtGui.QPixmap('./icons/upload.jpg')
        self.eeeekDisplay.setPhoto(pixmap)
        self.eeeekDisplay.fitInView()
        pixmap = QtGui.QPixmap('./icons/upload.jpg')
        self.oooooDisplay.setPhoto(pixmap)
        self.oooooDisplay.fitInView()
        
    ########################################################################################################################
    """Load Functions"""
    ########################################################################################################################
    
    def load_R(self):
        #load a file using the widget
        name,_ = QtWidgets.QFileDialog.getOpenFileName(
                self,'Load Image',
                '',"Image files (*.png *.jpg *.jpeg *.jfif *.tif *.tiff *.PNG *.JPG *.JPEG *.TIF *.TIFF)")
        Pname = Path(name)
        if Pname.is_file():
            self._file_R = name
            self._valid_file_R = True
            pixmap = QtGui.QPixmap(name)
            self.restingDisplay.setPhoto(pixmap)
        else:
            QtWidgets.QMessageBox.information(self, 'Error', 
                'Valid file not selected', 
                QtWidgets.QMessageBox.Ok)

    
    def load_BR(self):
        #load a file using the widget
        name,_ = QtWidgets.QFileDialog.getOpenFileName(
                self,'Load Image',
                '',"Image files (*.png *.jpg *.jpeg *.jfif *.tif *.tiff *.PNG *.JPG *.JPEG *.TIF *.TIFF)")
        Pname = Path(name)
        if Pname.is_file():
            self._file_BR = name
            self._valid_file_BR = True
            pixmap = QtGui.QPixmap(name)
            self.browRaiseDisplay.setPhoto(pixmap)
        else:
            QtWidgets.QMessageBox.information(self, 'Error', 
                'Valid file not selected', 
                QtWidgets.QMessageBox.Ok)
    
    def load_GEC(self):
        #load a file using the widget
        name,_ = QtWidgets.QFileDialog.getOpenFileName(
                self,'Load Image',
                '',"Image files (*.png *.jpg *.jpeg *.jfif *.tif *.tiff *.PNG *.JPG *.JPEG *.TIF *.TIFF)")
        Pname = Path(name)
        if Pname.is_file():
            self._file_GEC = name
            self._valid_file_GEC = True
            pixmap = QtGui.QPixmap(name)
            self.gentleEyeClosureDisplay.setPhoto(pixmap)
        else:
            QtWidgets.QMessageBox.information(self, 'Error', 
                'Valid file not selected', 
                QtWidgets.QMessageBox.Ok)
    
    def load_TEC(self):
        #load a file using the widget
        name,_ = QtWidgets.QFileDialog.getOpenFileName(
                self,'Load Image',
                '',"Image files (*.png *.jpg *.jpeg *.jfif *.tif *.tiff *.PNG *.JPG *.JPEG *.TIF *.TIFF)")
        Pname = Path(name)
        if Pname.is_file():
            self._file_TEC = name
            self._valid_file_TEC = True
            pixmap = QtGui.QPixmap(name)
            self.tightEyeClosureDisplay.setPhoto(pixmap)
        else:
            QtWidgets.QMessageBox.information(self, 'Error', 
                'Valid file not selected', 
                QtWidgets.QMessageBox.Ok)
    
    def load_BS(self):
        #load a file using the widget
        name,_ = QtWidgets.QFileDialog.getOpenFileName(
                self,'Load Image',
                '',"Image files (*.png *.jpg *.jpeg *.jfif *.tif *.tiff *.PNG *.JPG *.JPEG *.TIF *.TIFF)")
        Pname = Path(name)
        if Pname.is_file():
            self._file_BS = name
            self._valid_file_BS = True
            pixmap = QtGui.QPixmap(name)
            self.bigSmileDisplay.setPhoto(pixmap)
        else:
            QtWidgets.QMessageBox.information(self, 'Error', 
                'Valid file not selected', 
                QtWidgets.QMessageBox.Ok)
    
    def load_eeeek(self):
        #load a file using the widget
        name,_ = QtWidgets.QFileDialog.getOpenFileName(
                self,'Load Image',
                '',"Image files (*.png *.jpg *.jpeg *.jfif *.tif *.tiff *.PNG *.JPG *.JPEG *.TIF *.TIFF)")
        Pname = Path(name)
        if Pname.is_file():
            self._file_eeeek = name
            self._valid_file_eeeek = True
            pixmap = QtGui.QPixmap(name)
            self.eeeekDisplay.setPhoto(pixmap)
        else:
            QtWidgets.QMessageBox.information(self, 'Error', 
                'Valid file not selected', 
                QtWidgets.QMessageBox.Ok)
    
    def load_ooooo(self):
        #load a file using the widget
        name,_ = QtWidgets.QFileDialog.getOpenFileName(
                self,'Load Image',
                '',"Image files (*.png *.jpg *.jpeg *.jfif *.tif *.tiff *.PNG *.JPG *.JPEG *.TIF *.TIFF)")
        Pname = Path(name)
        if Pname.is_file():
            self._file_ooooo = name
            self._valid_file_ooooo = True
            pixmap = QtGui.QPixmap(name)
            self.oooooDisplay.setPhoto(pixmap)
        else:
            QtWidgets.QMessageBox.information(self, 'Error', 
                'Valid file not selected', 
                QtWidgets.QMessageBox.Ok)
    
        
    ########################################################################################################################
    """Patient Functions"""
    ########################################################################################################################

    def leftSideSelected(self):
        self._reference_side = 'Left'
    
    def rightSideSelected(self):
        self._reference_side = 'Right'

        
    ########################################################################################################################
    """Close Functions"""
    ########################################################################################################################
    
    def next(self):
        if (self._valid_file_R == True and self._valid_file_BR == True and 
        self._valid_file_GEC == True and self._valid_file_TEC == True and 
        self._valid_file_BS == True and self._valid_file_eeeek == True and 
        self._valid_file_ooooo == True):
            self.file_R.emit(self._file_R)
            self.file_BR.emit(self._file_BR)
            self.file_GEC.emit(self._file_GEC)
            self.file_TEC.emit(self._file_TEC)
            self.file_BS.emit(self._file_BS) 
            self.file_eeeek.emit(self._file_eeeek)
            self.file_ooooo.emit(self._file_ooooo)
            self.reference_Side.emit(self._reference_side)
            # self.patient_ID.emit(self._patient_ID)
            self.finished.emit()
            self.close()
        elif (self.restingDisplay._hasImage == True and self.browRaiseDisplay._hasImage == True and 
        self.gentleEyeClosureDisplay._hasImage == True and self.tightEyeClosureDisplay._hasImage == True and 
        self.bigSmileDisplay._hasImage == True and self.eeeekDisplay._hasImage == True and 
        self.oooooDisplay._hasImage == True):
            self._file_R = self.restingDisplay._ImageAddress
            self._file_BR = self.browRaiseDisplay._ImageAddress
            self._file_GEC = self.gentleEyeClosureDisplay._ImageAddress
            self._file_TEC = self.tightEyeClosureDisplay._ImageAddress
            self._file_BS = self.bigSmileDisplay._ImageAddress
            self._file_eeeek = self.eeeekDisplay._ImageAddress
            self._file_ooooo = self.oooooDisplay._ImageAddress
            self.file_R.emit(self._file_R)
            self.file_BR.emit(self._file_BR)
            self.file_GEC.emit(self._file_GEC)
            self.file_TEC.emit(self._file_TEC)
            self.file_BS.emit(self._file_BS) 
            self.file_eeeek.emit(self._file_eeeek)
            self.file_ooooo.emit(self._file_ooooo)
            self.reference_Side.emit(self._reference_side)
            # self.patient_ID.emit(self._patient_ID)
            self.finished.emit()
            self.close()
        else:
            QtWidgets.QMessageBox.information(self, 'Error', 
                'Valid files not selected.\nPlease select a valid photo. ', 
                QtWidgets.QMessageBox.Ok)
    
    def previous(self):
        self.canceled.emit()
        self.close()

    