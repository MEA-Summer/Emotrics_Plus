from PyQt5 import QtWidgets, QtGui, uic, QtCore
from pathlib import Path

class SelectionWindow(QtWidgets.QMainWindow):
    finished = QtCore.pyqtSignal()
    canceled = QtCore.pyqtSignal()
    file1 = QtCore.pyqtSignal(object)
    file2 = QtCore.pyqtSignal(object)
    reference_Side = QtCore.pyqtSignal(object)
    task = QtCore.pyqtSignal(object)

    def __init__(self):
        super() .__init__()
        self._file1 = None
        self._valid_File1 = False
        self._file1 = None
        self._valid_File2 = False
        self._reference_side = 'Right'
        self._task = 'Pre-Op vs Post-Op'



        self.initUI()
        
        
    def initUI(self):
        self.ui = uic.loadUi('uis\select.ui', self)
        
        """Button Connection"""
        self.loadPhoto1Button.clicked.connect(self.load_file1)
        self.loadPhoto2Button.clicked.connect(self.load_file2)
        self.leftSideButton.toggled.connect(self.leftSideSelected)
        self.rightSideButton.toggled.connect(self.rightSideSelected)
        self.PrevsPostButton.clicked.connect(self.PrevsPostSelect)
        self.RestingvsExpressionButton.clicked.connect(self.RestingvsExpressionSelect)
        self.previousButton.clicked.connect(self.previous)
        self.nextButton.clicked.connect(self.next)
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
            self.photo1Display.update_view()
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
            self.photo2Display.update_view()
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

    def RestingvsExpressionSelect(self):
        self._task = 'Resting vs Expression'
        self.loadPhoto1Button.setText('Click to Upload Resting Photograph')
        self.loadPhoto2Button.setText('Click to Upload Expression Photograph')
        self.PrevsPostButton.setChecked(False)
        self.RestingvsExpressionButton.setChecked(True)


    def next(self):
        if self._valid_File1 == True and self._valid_File2 == True:
            self.file1.emit(self._file1)
            self.file2.emit(self._file2)
            self.reference_Side.emit(self._reference_side)
            self.task.emit(self._task)
            self.finished.emit()
            self.close()
        elif self.photo1Display._hasImage == True and self.photo1Display._hasImage == True:
            self._file1 = self.photo1Display._ImageAddress
            self._file2 = self.photo2Display._ImageAddress
            self.file1.emit(self._file1)
            self.file2.emit(self._file2)
            self.reference_Side.emit(self._reference_side)
            self.task.emit(self._task)
            self.finished.emit()
            self.close()
        else:
            QtWidgets.QMessageBox.information(self, 'Error', 
                            'Valid files not selected.\nPlease select two valid photos. ', 
                            QtWidgets.QMessageBox.Ok)
    
    def previous(self):
        self.canceled.emit()
        self.close()

    