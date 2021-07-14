import os
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap



class QHLine(QtWidgets.QFrame):

    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)


class SelectLandmarksTab(QtWidgets.QWidget):

    def __init__(self, ModelName, NLF_Model):
        super(SelectLandmarksTab, self).__init__()

        self._tab_name = 'Select Landmarks'
        self.Modelname = ModelName  # Default Model is FAN_MEEE
        self.NLF_Model = NLF_Model
        self.selectLandmarks = QtWidgets.QLabel()
        self.selectLandmarks.setText('Select Landmarks:\n Current Model:'+str(self.Modelname))

        
        self.selectModelComboBox = QtWidgets.QComboBox(self)
        self.selectModelComboBox.addItem('FAN_MEEE')
        self.selectModelComboBox.addItem('FAN')
        self.selectModelComboBox.addItem('HRNet')
        self.selectModelComboBox.addItem('NLF_model')
        self.selectModelComboBox.activated[str].connect(self.ChangeModels)

        self.NLFcheckbox = QtWidgets.QCheckBox(self)
        self.NLFcheckbox.stateChanged.connect(self.NLF_addition)
        self.NLFcheckbox.setText('NLF Landmarks')
        if self.NLF_Model == True:
            self.NLFcheckbox.setChecked(True)



        self.setLandmarkPicture = QtWidgets.QLabel(self)
        pixmap = QPixmap('SelectLandmarks.jpg')
        self.setLandmarkPicture.setPixmap(pixmap)
        
        

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.selectLandmarks)
        layout.addWidget(self.NLFcheckbox)
        layout.addWidget(self.setLandmarkPicture)
        layout.addWidget(self.selectModelComboBox)


        self.setLayout(layout)


    def ChangeModels(self, model):
        self.Modelname = model
        
    def NLF_addition(self, y_or_n):
        if y_or_n == 0:
            self.NLF_Model = False
        else:
            self.NLF_Model = True

class LandmarkOptionsTab(QtWidgets.QWidget):

    def __init__(self, Landmarks_size):
        super(LandmarkOptionsTab, self).__init__()

        if os.name == 'posix':  # is a mac or linux
            scriptDir = os.path.dirname(sys.argv[0])
        else:  # is a  windows
            scriptDir = os.getcwd()

        self._tab_name = 'Landmark Options'
        self.selectedColor = None
        self.selectSize = QtWidgets.QLabel()
        self.selectSize.setText('Size of Landmarks:')

        self._landmark_size = Landmarks_size
        
        self.selectLandmarkSize = QtWidgets.QLineEdit(self)
        onlyInt = QtGui.QIntValidator(1, 10000)
        self.selectLandmarkSize.setValidator(onlyInt)
        self.selectLandmarkSize.setText(str(self._landmark_size*100))
        self.SizeButton = QtWidgets.QPushButton('Select Size', self)
        #SizeButton.clicked.connect(lambda: window.landmarkSizeChanged(selectLandmarkSize.text()))

        self.selectColor = QtWidgets.QLabel()
        self.selectColor.setText('Color of Landmarks:')
        self.ColorButton = QtWidgets.QPushButton('Select Color', self)
        self.ColorButton.clicked.connect(self.openColorDialog)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.selectSize)
        layout.addWidget(self.selectLandmarkSize)
        layout.addWidget(self.SizeButton)
        layout.addWidget(QHLine())
        layout.addWidget(self.selectColor)
        layout.addWidget(self.ColorButton)

        self.setLayout(layout)

    def openColorDialog(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.selectedColor = color
            print('Color Selected: ', color.name())

class ShowSettings(QtWidgets.QDialog):

    def __init__(self, ModelName, NLF_Model, landmark_size):
        super(ShowSettings, self).__init__()

        self.setWindowTitle('Landmark Settings')
        if os.name == 'posix':  # is a mac or linux
            scriptDir = os.path.dirname(sys.argv[0])
        else:  # is a  windows
            scriptDir = os.getcwd()

        #self.setWindowIcon(QtGui.QIcon(
            #scriptDir + os.path.sep + 'include' + os.path.sep + 'icon_color' + os.path.sep + 'settings_icon.ico'))

        self.isCanceled = False
        self._NLF_Model = NLF_Model
        self._ModelName = ModelName
        self._Landmark_size = landmark_size
       # self._CalibrationType = CalibrationType
       # self._shape = shape

        self.tab1 = SelectLandmarksTab(self._ModelName, self._NLF_Model)
        self.tab2 = LandmarkOptionsTab(self._Landmark_size)

        self.main_Widget = QtWidgets.QTabWidget(self)
        self.tab1.setAutoFillBackground(True)
        self.tab2.setAutoFillBackground(True)
        self.main_Widget.addTab(self.tab1, self.tab1._tab_name)
        self.main_Widget.addTab(self.tab2, self.tab2._tab_name)


        # if tab2 is not None:
        #    tab2.setAutoFillBackground(True)
        #    self.main_Widget.addTab(tab2,tab2._tab_name)

        # if tab3 is not None:
        #    tab3.setAutoFillBackground(True)
        #    self.main_Widget.addTab(tab3,'Difference')

        #self.buttonDone = QtWidgets.QPushButton('Done', self)
        #self.buttonDone.clicked.connect(self.handleReturn)

        #self.buttonCancel = QtWidgets.QPushButton('Cancel', self)
        #self.buttonCancel.clicked.connect(self.pressCanceled)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.main_Widget)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.main_Widget, 0, 0, 2, 2)
        #layout.addWidget(self.buttonDone, 2, 0, 1, 1)
        #layout.addWidget(self.buttonCancel, 2, 1, 1, 1)

        self.setLayout(layout)