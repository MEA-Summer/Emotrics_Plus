from PyQt5 import QtWidgets, QtCore, uic


class LandmarkSettingsWindow(QtWidgets.QMainWindow):
    
    models = QtCore.pyqtSignal(object, object)
    colors = QtCore.pyqtSignal(object, object, object, object)
    size = QtCore.pyqtSignal(object)
    
    def __init__(self, Model_name, color_landmark1, color_landmark2, color_eyes, color_midline, landmark_size):
        super() .__init__()
        #Input variables
        self._Model_name = Model_name
        self._color_landmark1 = color_landmark1
        self._color_landmark2 = color_landmark2
        self._color_eyes = color_eyes
        self._color_midline = color_midline
        self._landmark_size = landmark_size
        #Status variables
        self._new_Model_selected = False
        self._save_changes = False
        
        self.initUI()
        
        
    def initUI(self):
        self.ui = uic.loadUi('uis/landmark_settings.ui', self)
        
        #Filling in Colors based on current colors
        self.landmark1ColorLabel.setStyleSheet('QWidget {background-color:%s}' %self._color_landmark1.name())
        self.landmark2ColorLabel.setStyleSheet('QWidget {background-color:%s}' %self._color_landmark2.name())
        self.eyeColorLabel.setStyleSheet('QWidget {background-color:%s}' %self._color_eyes.name())
        self.midlineColorLabel.setStyleSheet('QWidget {background-color:%s}' %self._color_midline.name())
        
        #Add model names to combo box
        self.modelComboBox.addItem('FAN_MEEE')
        self.modelComboBox.addItem('FAN')
        self.modelComboBox.addItem('HRNet')
        self.modelComboBox.addItem('NLF_model')
        self.modelComboBox.setCurrentText(self._Model_name)
        self.modelComboBox.activated[str].connect(self.changeModelname)
        
        #Set landmark size to current size
        self.landmarkSizeSpinBox.setValue(int(self._landmark_size))
        
        #Connect Buttons
        self.landmark1ColorButton.clicked.connect(self.get_Landmark1Color)
        self.landmark2ColorButton.clicked.connect(self.get_Landmark2Color)
        self.eyeColorButton.clicked.connect(self.get_EyeColor)
        self.midlineColorButton.clicked.connect(self.get_MidlineColor)
        self.doneButton.clicked.connect(self.done)
        self.cancelButton.clicked.connect(self.cancel)
        
        
    def cancel(self):
        self.close()
        
        
    def done(self):
        self._save_changes = True
        
        self._landmark_size = self.landmarkSizeSpinBox.value()
        
        self.models.emit(self._Model_name, self._new_Model_selected)
        self.colors.emit(self._color_landmark1, self._color_landmark2, self._color_eyes, self._color_midline)
        self.size.emit(self._landmark_size)
        self.close()
        
        
    def changeModelname(self, modelname):
        self._new_Model_selected = True
        self._Model_name = modelname
        
        
    def get_Landmark1Color(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self._color_landmark1 = color
            # print('Color Selected: ', color.name())
            self.landmark1ColorLabel.setStyleSheet('QWidget {background-color:%s}' %self._color_landmark1.name())
        
        
    def get_Landmark2Color(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self._color_landmark2 = color
            # print('Color Selected: ', color.name())
            self.landmark2ColorLabel.setStyleSheet('QWidget {background-color:%s}' %self._color_landmark2.name())
            
            
    def get_EyeColor(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self._color_eyes = color
            # print('Color Selected: ', color.name())
            self.eyeColorLabel.setStyleSheet('QWidget {background-color:%s}' %self._color_eyes.name())
            
            
    def get_MidlineColor(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self._color_midline = color
            # print('Color Selected: ', color.name())
            self.midlineColorLabel.setStyleSheet('QWidget {background-color:%s}' %self._color_midline.name())