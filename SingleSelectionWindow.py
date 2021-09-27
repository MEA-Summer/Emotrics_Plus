from PyQt5 import QtWidgets, QtGui, uic, QtCore
from pathlib import Path

class SingleSelectionWindow(QtWidgets.QMainWindow):
    finished = QtCore.pyqtSignal()
    canceled = QtCore.pyqtSignal()
    file = QtCore.pyqtSignal(object)
    patientID = QtCore.pyqtSignal(object)
    reference_Side = QtCore.pyqtSignal(object)
    taskName = QtCore.pyqtSignal(object)

    def __init__(self):
        super() .__init__()
        self._file1 = None
        self._valid_File = False
        self._patientID = ''
        self._reference_side = 'Right'
        self._taskName = 'Resting'



        self.initUI()
        
        
    def initUI(self):
        self.ui = uic.loadUi('uis\Single_Select.ui', self)
        
        """Button Connection"""
        self.loadPhotoButton.clicked.connect(self.load_file)
        self.leftSideButton.toggled.connect(self.leftSideSelected)
        self.rightSideButton.toggled.connect(self.rightSideSelected)

        self.previousButton.clicked.connect(self.previous)
        self.nextButton.clicked.connect(self.next)

        #Setting up Combo boxes
        self.ExpressionComboBox.activated[str].connect(self.getNewTaskName)
        self.ExpressionComboBox.addItem('Resting')
        self.ExpressionComboBox.addItem('Brow Raise')
        self.ExpressionComboBox.addItem('Gentle Eye Closure')
        self.ExpressionComboBox.addItem('Tight Eye Closure')
        self.ExpressionComboBox.addItem('Big Smile')
        self.ExpressionComboBox.addItem('"eeeek"')
        self.ExpressionComboBox.addItem('"ooooo"')
        self.ExpressionComboBox.addItem('Other')
        
        
        #Adding Icons
        pixmap = QtGui.QPixmap('./icons/upload.jpg')
        self.photoDisplay.setPhoto(pixmap)
        self.photoDisplay.fitInView()
        


    def load_file(self):
        #load a file using the widget
        name,_ = QtWidgets.QFileDialog.getOpenFileName(
                self,'Load Image',
                '',"Image files (*.png *.jpg *.jpeg *.jfif *.tif *.tiff *.PNG *.JPG *.JPEG *.TIF *.TIFF)")
        Pname = Path(name)
        if Pname.is_file():
            self._file = name
            self._valid_File = True
            pixmap = QtGui.QPixmap(name)
            self.photoDisplay.setPhoto(pixmap)
        else:
            QtWidgets.QMessageBox.information(self, 'Error', 
                'Valid file not selected', 
                QtWidgets.QMessageBox.Ok)


    def leftSideSelected(self):
        self._reference_side = 'Left'
    
    def rightSideSelected(self):
        self._reference_side = 'Right'

    def getNewTaskName(self, task_Name):
        self._taskName = task_Name
    
    def getPatientID(self):
        self._patientID = self.patientIDLineEdit.text()



    def next(self):
        self.getPatientID()
        if self._patientID == '':
            patientIDQuestion = QtWidgets.QMessageBox
            patientIDBox = patientIDQuestion.question(self, 'No Patient ID', 
                'There is currently no Patient ID entered. Would you still like to continue?', 
                patientIDQuestion.Yes | patientIDQuestion.No) 
            if patientIDBox == patientIDQuestion.Yes:
                if self._valid_File == True :
                    self.file.emit(self._file)
                    self.reference_Side.emit(self._reference_side)
                    self.taskName.emit(self._taskName)
                    self.patientID.emit(self._patientID)
                    self.finished.emit()
                    self.close()
                elif self.photoDisplay._hasImage == True :
                    self._file = self.photoDisplay._ImageAddress
                    self.file.emit(self._file)
                    self.reference_Side.emit(self._reference_side)
                    self.taskName.emit(self._taskName)
                    self.patientID.emit(self._patientID)
                    self.finished.emit()
                    self.close()
                else:
                    QtWidgets.QMessageBox.information(self, 'Error', 
                        'Valid files not selected.\nPlease select a valid photo. ', 
                        QtWidgets.QMessageBox.Ok)
        else:
            if self._valid_File == True :
                self.file.emit(self._file)
                self.reference_Side.emit(self._reference_side)
                self.taskName.emit(self._taskName)
                self.patientID.emit(self._patientID)
                self.finished.emit()
                self.close()
            elif self.photoDisplay._hasImage == True :
                self._file = self.photoDisplay._ImageAddress
                self.file.emit(self._file)
                self.reference_Side.emit(self._reference_side)
                self.taskName.emit(self._taskName)
                self.patientID.emit(self._patientID)
                self.finished.emit()
                self.close()
            else:
                QtWidgets.QMessageBox.information(self, 'Error', 
                    'Valid files not selected.\nPlease select a valid photo. ', 
                    QtWidgets.QMessageBox.Ok)
            
    
    def previous(self):
        self.canceled.emit()
        self.close()

    