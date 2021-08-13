from PyQt5 import QtWidgets, QtGui, uic, QtCore
from pathlib import Path

class DoubleSelectionWindow(QtWidgets.QMainWindow):
    finished = QtCore.pyqtSignal()
    canceled = QtCore.pyqtSignal()
    file1 = QtCore.pyqtSignal(object)
    file2 = QtCore.pyqtSignal(object)
    reference_Side = QtCore.pyqtSignal(object)
    task = QtCore.pyqtSignal(object)
    taskName = QtCore.pyqtSignal(object)

    def __init__(self):
        super() .__init__()
        self._file1 = None
        self._valid_File1 = False
        self._file1 = None
        self._valid_File2 = False
        self._reference_side = 'Right'
        self._task = 'Pre-Op vs Post-Op'
        self._taskName = 'Ocular'



        self.initUI()
        
        
    def initUI(self):
        self.ui = uic.loadUi('uis\Double_Select.ui', self)
        
        """Button Connection"""
        self.loadPhoto1Button.clicked.connect(self.load_file1)
        self.loadPhoto2Button.clicked.connect(self.load_file2)
        self.leftSideButton.toggled.connect(self.leftSideSelected)
        self.rightSideButton.toggled.connect(self.rightSideSelected)
        self.PrevsPostButton.clicked.connect(self.PrevsPostSelect)
        self.RestingvsExpressionButton.clicked.connect(self.RestingvsExpressionSelect)

        

        self.previousButton.clicked.connect(self.previous)
        self.nextButton.clicked.connect(self.next)

        #Setting up Combo boxes
        self.ManipulationComboBox.activated[str].connect(self.getNewTaskName)
        # self.ManipulationComboBox.addItem('')
        self.ManipulationComboBox.addItem('Ocular')
        self.ManipulationComboBox.addItem('Midface')
        self.ManipulationComboBox.addItem('Lips/Smile')
        self.ManipulationComboBox.addItem('Other')

        self.ExpressionComboBox.activated[str].connect(self.getNewTaskName)
        # self.ExpressionComboBox.addItem('')
        self.ExpressionComboBox.addItem('Brow Raise')
        self.ExpressionComboBox.addItem('Gentle Eye Closure')
        self.ExpressionComboBox.addItem('Tight Eye Closure')
        self.ExpressionComboBox.addItem('Gentle Smile')
        self.ExpressionComboBox.addItem('Big Smile')
        self.ExpressionComboBox.addItem('"eeeek"')
        self.ExpressionComboBox.addItem('"ooooo"')
        self.ExpressionComboBox.addItem('Other')
        #Since the default is Pre-op vs Post-op, This is disabled intialally
        self.ExpressionComboBox.setCurrentText('Gentle Smile')
        self.ExpressionComboBox.setEnabled(False)
        
        
        #Adding Icons
        pixmap = QtGui.QPixmap('./icons/upload.jpg')
        self.photo1Display.setPhoto(pixmap)
        self.photo1Display.fitInView()
        pixmap = QtGui.QPixmap('./icons/upload.jpg')
        self.photo2Display.setPhoto(pixmap)
        self.photo2Display.fitInView()


    def load_file1(self):
        #load a file using the widget
        name,_ = QtWidgets.QFileDialog.getOpenFileName(
                self,'Load Image',
                '',"Image files (*.png *.jpg *.jpeg *.jfif *.tif *.tiff *.PNG *.JPG *.JPEG *.TIF *.TIFF)")
        Pname = Path(name)
        if Pname.is_file():
            self._file1 = name
            self._valid_File1 = True
            pixmap = QtGui.QPixmap(name)
            self.photo1Display.setPhoto(pixmap)
        else:
            QtWidgets.QMessageBox.information(self, 'Error', 
                            'Valid file not selected', 
                            QtWidgets.QMessageBox.Ok)
    
    
    def load_file2(self):
        #load a file using the widget
        name,_ = QtWidgets.QFileDialog.getOpenFileName(
                self,'Load Image',
                '',"Image files (*.png *.jpg *.jpeg *.jfif *.tif *.tiff *.PNG *.JPG *.JPEG *.TIF *.TIFF)")
        Pname = Path(name)
        if Pname.is_file():
            self._file2 = name
            self._valid_File2 = True
            pixmap = QtGui.QPixmap(name)
            self.photo2Display.setPhoto(pixmap)
        else:
            QtWidgets.QMessageBox.information(self, 'Error', 
                            'Valid file not selected.', 
                            QtWidgets.QMessageBox.Ok)

       
    def leftSideSelected(self):
        self._reference_side = 'Left'
    
    def rightSideSelected(self):
        self._reference_side = 'Right'


    def PrevsPostSelect(self):
        self._task = 'Pre-Op vs Post-Op'
        self.loadPhoto1Button.setText('Click to Upload Pre-Op Photograph')
        self.loadPhoto2Button.setText('Click to Upload Post-Op Photograph')
        self.PrevsPostButton.setChecked(True)
        self.RestingvsExpressionButton.setChecked(False)
        self.manipulationsLabel.setStyleSheet("")
        self.expressionsLabel.setStyleSheet("color: rgb(204, 204, 204)")
        # self.ExpressionComboBox.setCurrentText('')
        self.ExpressionComboBox.setEnabled(False)
        self.ManipulationComboBox.setEnabled(True)
        self.getNewTaskName(self.ExpressionComboBox.currentText())


    def RestingvsExpressionSelect(self):
        self._task = 'Resting vs Expression'
        self.loadPhoto1Button.setText('Click to Upload Resting Photograph')
        self.loadPhoto2Button.setText('Click to Upload Expression Photograph')
        self.PrevsPostButton.setChecked(False)
        self.RestingvsExpressionButton.setChecked(True)
        self.manipulationsLabel.setStyleSheet("color: rgb(204, 204, 204)")
        self.expressionsLabel.setStyleSheet("")
        # self.ManipulationComboBox.setCurrentText('')
        self.ManipulationComboBox.setEnabled(False)
        self.ExpressionComboBox.setEnabled(True)
        self.getNewTaskName(self.ExpressionComboBox.currentText())

    def getNewTaskName(self, task_Name):
        self._taskName = task_Name


    def next(self):
        if self._valid_File1 == True and self._valid_File2 == True:
            self.file1.emit(self._file1)
            self.file2.emit(self._file2)
            self.reference_Side.emit(self._reference_side)
            self.task.emit(self._task)
            self.taskName.emit(self._taskName)
            self.finished.emit()
            self.close()
        elif self.photo1Display._hasImage == True and self.photo1Display._hasImage == True:
            self._file1 = self.photo1Display._ImageAddress
            self._file2 = self.photo2Display._ImageAddress
            self.file1.emit(self._file1)
            self.file2.emit(self._file2)
            self.reference_Side.emit(self._reference_side)
            self.task.emit(self._task)
            self.taskName.emit(self._taskName)
            self.finished.emit()
            self.close()
        else:
            QtWidgets.QMessageBox.information(self, 'Error', 
                            'Valid files not selected.\nPlease select two valid photos. ', 
                            QtWidgets.QMessageBox.Ok)
    
    def previous(self):
        self.canceled.emit()
        self.close()

    